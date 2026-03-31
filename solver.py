"""Covering design solver for the Optimal Samples Selection System.

Solves L(n, k, j, s): find minimum k-subsets of {0,...,n-1} such that
every j-subset shares at least s elements with at least one selected k-subset.

Optimisations:
  - Precomputed coverage table: for each candidate, which targets it covers
  - Incremental scoring: after choosing a group, only update affected candidates
  - Containment fast-path: O(C(k,j)) lookup table when s==j
  - Simulated annealing post-processing for medium-size solutions
  - Adaptive top-K heuristic for very large problems (n=25)
"""

from __future__ import annotations

import heapq
import math
import random
import time
from dataclasses import dataclass
from itertools import combinations
from math import comb
from typing import Callable

import numpy as np


# ---------------------------------------------------------------------------
# Bitmask utilities
# ---------------------------------------------------------------------------

def popcount_uint32(arr: np.ndarray) -> np.ndarray:
    """Vectorised Hamming-weight (popcount) for uint32 numpy arrays."""
    x = np.array(arr, dtype=np.uint32, copy=True)
    t = (x >> np.uint32(1)) & np.uint32(0x55555555)
    np.subtract(x, t, out=x)
    del t
    t = x & np.uint32(0x33333333)
    np.right_shift(x, np.uint32(2), out=x)
    x &= np.uint32(0x33333333)
    np.add(x, t, out=x)
    del t
    t = x >> np.uint32(4)
    np.add(x, t, out=x)
    del t
    x &= np.uint32(0x0F0F0F0F)
    np.multiply(x, np.uint32(0x01010101), out=x)
    np.right_shift(x, np.uint32(24), out=x)
    return x.astype(np.int32)


def mask_to_elements(mask: int) -> list[int]:
    """Bitmask -> sorted list of 0-based element indices."""
    elems: list[int] = []
    i = 0
    while mask:
        if mask & 1:
            elems.append(i)
        mask >>= 1
        i += 1
    return elems


def elements_to_mask(elements) -> int:
    mask = 0
    for e in elements:
        mask |= 1 << e
    return mask


def _extract_bits(mask: int) -> list[int]:
    """Return individual bit-positions as power-of-2 values."""
    bits: list[int] = []
    while mask:
        b = mask & (-mask)
        bits.append(b)
        mask &= mask - 1
    return bits


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SolverProgress:
    phase: str = ""
    message: str = ""
    iteration: int = 0
    solution_size: int = 0
    remaining: int = 0
    total: int = 0
    elapsed: float = 0.0


@dataclass
class SolverResult:
    groups: list[list[int]]
    num_groups: int = 0
    elapsed: float = 0.0
    verified: bool = False

    def __post_init__(self) -> None:
        self.num_groups = len(self.groups)


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------

MAX_BATCH_BYTES = 600 * 1024 * 1024  # 600 MiB ceiling per numpy batch


class CoveringDesignSolver:
    """Greedy + local-search + SA solver for covering designs."""

    def __init__(
        self,
        n: int,
        k: int,
        j: int,
        s: int,
        *,
        progress_cb: Callable[[SolverProgress], None] | None = None,
        cancel_fn: Callable[[], bool] | None = None,
        num_attempts: int = 3,
    ) -> None:
        self.n = n
        self.k = k
        self.j = j
        self.s = s
        self._cb = progress_cb
        self._cancel = cancel_fn or (lambda: False)
        self._num_attempts = max(1, num_attempts)
        self._t0 = 0.0

        # --- validate -------------------------------------------------
        if not 7 <= n <= 25:
            raise ValueError(f"n must be 7-25, got {n}")
        if not 4 <= k <= 7:
            raise ValueError(f"k must be 4-7, got {k}")
        if not 3 <= s <= 7:
            raise ValueError(f"s must be 3-7, got {s}")
        if not s <= j <= k:
            raise ValueError(f"Need s<=j<=k, got s={s} j={j} k={k}")
        if n < k:
            raise ValueError(f"Need n>=k, got n={n} k={k}")

        self._containment = s == j

        # --- generate bitmasks ----------------------------------------
        elems = list(range(n))
        self.target_masks = np.array(
            [elements_to_mask(c) for c in combinations(elems, j)],
            dtype=np.uint32,
        )
        self.cand_masks = np.array(
            [elements_to_mask(c) for c in combinations(elems, k)],
            dtype=np.uint32,
        )
        self.num_targets = len(self.target_masks)
        self.num_cands = len(self.cand_masks)

        # --- precompute coverage tables -------------------------------
        # _cov_table[ci] = array of target indices that candidate ci covers
        # _inv_table[ti] = array of candidate indices that cover target ti
        self._cov_table: list[np.ndarray] | None = None
        self._inv_table: list[np.ndarray] | None = None
        self._jsub_table: np.ndarray | None = None

        mem_estimate = self.num_cands * self.num_targets  # rough
        if mem_estimate <= 500_000_000:  # <500M interactions → build table
            self._build_coverage_tables()
        elif self._containment:
            self._build_jsub_table()

    # ------------------------------------------------------------------
    # Precomputation
    # ------------------------------------------------------------------

    def _build_coverage_tables(self) -> None:
        """Build cov_table[ci]->targets and inv_table[ti]->candidates."""
        cov: list[list[int]] = [[] for _ in range(self.num_cands)]
        inv: list[list[int]] = [[] for _ in range(self.num_targets)]

        # Process in batches to avoid huge 2D arrays
        bs = max(1, 400_000_000 // max(1, self.num_targets * 4))
        bs = min(bs, self.num_cands)

        for start in range(0, self.num_cands, bs):
            if self._cancel():
                return
            end = min(start + bs, self.num_cands)
            batch = self.cand_masks[start:end]
            ints = batch[:, None] & self.target_masks[None, :]
            if self._containment:
                hits = ints == self.target_masks[None, :]
            else:
                hits = popcount_uint32(ints) >= self.s
            ci_arr, ti_arr = np.nonzero(hits)
            for ci_local, ti in zip(ci_arr, ti_arr):
                ci = start + int(ci_local)
                ti = int(ti)
                cov[ci].append(ti)
                inv[ti].append(ci)

        self._cov_table = [np.array(c, dtype=np.int32) for c in cov]
        self._inv_table = [np.array(c, dtype=np.int32) for c in inv]

    def _build_jsub_table(self) -> None:
        """For each candidate, store indices of its j-subsets in target_masks."""
        cpj = comb(self.k, self.j)
        target_idx: dict[int, int] = {
            int(self.target_masks[i]): i for i in range(self.num_targets)
        }

        table = np.empty((self.num_cands, cpj), dtype=np.int32)
        for ci in range(self.num_cands):
            bits = _extract_bits(int(self.cand_masks[ci]))
            for ji, jsub_bits in enumerate(combinations(bits, self.j)):
                jmask = 0
                for b in jsub_bits:
                    jmask |= b
                table[ci, ji] = target_idx[jmask]
        self._jsub_table = table

        # Also derive cov/inv from jsub_table for unified fast-path
        cov: list[list[int]] = [[] for _ in range(self.num_cands)]
        inv: list[list[int]] = [[] for _ in range(self.num_targets)]
        for ci in range(self.num_cands):
            for ti in table[ci]:
                ti = int(ti)
                cov[ci].append(ti)
                inv[ti].append(ci)
        self._cov_table = [np.array(c, dtype=np.int32) for c in cov]
        self._inv_table = [np.array(c, dtype=np.int32) for c in inv]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def solve(self) -> SolverResult:
        self._t0 = time.time()
        best: list[int] | None = None

        # Fewer attempts for very large problems
        num_att = self._num_attempts
        if self.num_cands > 100_000:
            num_att = min(num_att, 2)
        elif self.num_cands > 30_000:
            num_att = min(num_att, 3)

        for attempt in range(1, num_att + 1):
            if self._cancel():
                break
            self._report("greedy",
                         f"Attempt {attempt}/{num_att}: greedy...")
            sol = self._greedy(randomize=attempt > 1)
            if self._cancel():
                if best is None or (sol and len(sol) < len(best)):
                    best = sol
                break

            self._report("optimize",
                         f"Attempt {attempt}: optimise ({len(sol)} groups)...")
            sol = self._local_search(sol)
            if not self._cancel():
                sol = self._swap_improve(sol)
                sol = self._local_search(sol)
            if not self._cancel() and 3 < len(sol) <= 200:
                sol = self._sa_improve(sol)
                sol = self._local_search(sol)

            if best is None or len(sol) < len(best):
                best = sol
                self._report("optimize",
                             f"Best so far: {len(best)} groups (attempt {attempt})")

        masks = best or []
        return SolverResult(
            groups=[sorted(mask_to_elements(m)) for m in masks],
            elapsed=time.time() - self._t0,
            verified=self._verify(masks),
        )

    # ------------------------------------------------------------------
    # Greedy dispatch
    # ------------------------------------------------------------------

    def _greedy(self, *, randomize: bool = False) -> list[int]:
        if self._cov_table is not None:
            return self._greedy_incremental(randomize)
        return self._greedy_heuristic(randomize)

    # --- strategy 1: incremental (precomputed tables available) -------

    def _greedy_incremental(self, randomize: bool) -> list[int]:
        """Fast greedy using precomputed coverage + incremental score updates."""
        cov_table = self._cov_table
        inv_table = self._inv_table
        assert cov_table is not None and inv_table is not None

        uncov = np.ones(self.num_targets, dtype=bool)
        # scores[ci] = number of currently-uncovered targets that ci covers
        scores = np.array([len(c) for c in cov_table], dtype=np.int32)
        selected: list[int] = []
        iteration = 0
        log_interval = max(1, self.num_targets // 500)

        while uncov.any():
            if self._cancel():
                break

            if randomize:
                fscores = scores.astype(np.float64)
                fscores += np.random.random(self.num_cands) * 0.5
                best_idx = int(fscores.argmax())
            else:
                best_idx = int(scores.argmax())

            cnt = int(scores[best_idx])
            if cnt == 0:
                break

            mask = int(self.cand_masks[best_idx])
            selected.append(mask)

            # Mark covered and decrementally update scores
            newly_covered = cov_table[best_idx][uncov[cov_table[best_idx]]]
            uncov[newly_covered] = False
            for ti in newly_covered:
                # All candidates that also cover ti lose 1 from their score
                affected = inv_table[ti]
                scores[affected] -= 1

            iteration += 1
            rem = int(uncov.sum())
            if iteration % log_interval == 0 or rem == 0:
                self._report("greedy",
                             f"Iter {iteration}: +1 (covers {len(newly_covered)}), "
                             f"{rem} left",
                             iteration=iteration, sol_size=len(selected),
                             remaining=rem)
        return selected

    # --- strategy 4: heuristic-guided (large) -------------------------

    def _greedy_heuristic(self, randomize: bool) -> list[int]:
        uncov = np.ones(self.num_targets, dtype=bool)
        selected: list[int] = []
        iteration = 0

        while uncov.any():
            if self._cancel():
                break
            uncov_t = self.target_masks[uncov]
            mask, cnt = self._heuristic_pick(uncov_t, randomize)
            if cnt == 0:
                break
            selected.append(mask)
            self._mark_covered(mask, uncov)
            iteration += 1
            rem = int(uncov.sum())
            self._report("greedy",
                         f"Iter {iteration}: +1 (covers {cnt}), {rem} left",
                         iteration=iteration, sol_size=len(selected),
                         remaining=rem)
        return selected

    def _heuristic_pick(
        self, uncov_t: np.ndarray, randomize: bool,
    ) -> tuple[int, int]:
        """Element-frequency heuristic → top-K exact evaluation."""
        # element frequencies in uncovered targets
        freq = np.zeros(self.n, dtype=np.int64)
        for e in range(self.n):
            freq[e] = int(np.sum((uncov_t & np.uint32(1 << e)) != 0))

        # heuristic score per candidate
        h = np.zeros(self.num_cands, dtype=np.int64)
        for e in range(self.n):
            bit = np.uint32(1 << e)
            has_e = (self.cand_masks & bit).astype(bool)
            h += has_e * freq[e]

        # top-K
        top_k = min(2000, self.num_cands)
        if top_k < self.num_cands:
            top_idx = np.argpartition(h, -top_k)[-top_k:]
        else:
            top_idx = np.arange(self.num_cands)
        top_cands = self.cand_masks[top_idx]

        # exact scoring of top-K
        counts = self._batch_scores(top_cands, uncov_t)
        if randomize:
            counts = counts.astype(np.float64)
            counts += np.random.random(len(counts)) * 0.5

        best_local = int(np.argmax(counts))
        return int(top_cands[best_local]), int(counts[best_local])

    # ------------------------------------------------------------------
    # Batch scoring
    # ------------------------------------------------------------------

    def _batch_scores(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> np.ndarray:
        nc, nt = len(cands), len(targets)
        scores = np.zeros(nc, dtype=np.int32)
        bs = max(1, MAX_BATCH_BYTES // max(1, nt * 12))
        bs = min(bs, nc)

        for i in range(0, nc, bs):
            if self._cancel():
                break
            batch = cands[i : i + bs]
            ints = batch[:, None] & targets[None, :]
            if self._containment:
                counts = np.sum(ints == targets[None, :], axis=1)
            else:
                counts = np.sum(popcount_uint32(ints) >= self.s, axis=1)
            scores[i : i + len(batch)] = counts
        return scores

    def _eval_one(self, mask: int, targets: np.ndarray) -> int:
        ints = np.uint32(mask) & targets
        if self._containment:
            return int(np.sum(ints == targets))
        return int(np.sum(popcount_uint32(ints) >= self.s))

    # ------------------------------------------------------------------
    # Coverage helpers
    # ------------------------------------------------------------------

    def _mark_covered(self, mask: int, uncovered: np.ndarray) -> None:
        ints = np.uint32(mask) & self.target_masks
        if self._containment:
            covered = ints == self.target_masks
        else:
            covered = popcount_uint32(ints) >= self.s
        uncovered &= ~covered

    def _verify(self, masks: list[int]) -> bool:
        if not masks:
            return self.num_targets == 0
        covered = np.zeros(self.num_targets, dtype=bool)
        for m in masks:
            ints = np.uint32(m) & self.target_masks
            if self._containment:
                covered |= ints == self.target_masks
            else:
                covered |= popcount_uint32(ints) >= self.s
        return bool(np.all(covered))

    def _uncovered_masks(self, masks: list[int]) -> np.ndarray:
        covered = np.zeros(self.num_targets, dtype=bool)
        for m in masks:
            ints = np.uint32(m) & self.target_masks
            if self._containment:
                covered |= ints == self.target_masks
            else:
                covered |= popcount_uint32(ints) >= self.s
        return self.target_masks[~covered]

    # ------------------------------------------------------------------
    # Local search (coverage-count based — fast for large solutions)
    # ------------------------------------------------------------------

    def _local_search(self, sol: list[int]) -> list[int]:
        if len(sol) <= 60:
            return self._local_search_brute(sol)
        return self._local_search_fast(sol)

    def _local_search_brute(self, sol: list[int]) -> list[int]:
        improved = True
        while improved and not self._cancel():
            improved = False
            for i in range(len(sol)):
                rest = sol[:i] + sol[i + 1:]
                if self._verify(rest):
                    sol = rest
                    improved = True
                    self._report("optimize",
                                 f"Removed redundant -> {len(sol)} groups")
                    break
        return sol

    def _local_search_fast(self, sol: list[int]) -> list[int]:
        """Remove redundant groups using per-target coverage counts."""
        cov_count = np.zeros(self.num_targets, dtype=np.int32)
        sol_cov: list[np.ndarray] = []
        for m in sol:
            c = self._covers_bool(m)
            sol_cov.append(c)
            cov_count += c.astype(np.int32)

        improved = True
        while improved and not self._cancel():
            improved = False
            for i in range(len(sol) - 1, -1, -1):
                c = sol_cov[i]
                if np.all(cov_count[c] >= 2):
                    cov_count -= c.astype(np.int32)
                    sol.pop(i)
                    sol_cov.pop(i)
                    improved = True
                    self._report("optimize",
                                 f"Removed redundant -> {len(sol)} groups")
        return sol

    def _covers_bool(self, mask: int) -> np.ndarray:
        ints = np.uint32(mask) & self.target_masks
        if self._containment:
            return ints == self.target_masks
        return popcount_uint32(ints) >= self.s

    def _swap_improve(self, sol: list[int], rounds: int = 3) -> list[int]:
        if len(sol) > 60:
            return sol  # skip expensive swap for large solutions
        for _ in range(rounds):
            if self._cancel():
                break
            improved = False
            order = list(range(len(sol)))
            random.shuffle(order)
            for i in order:
                if self._cancel():
                    break
                rest = sol[:i] + sol[i + 1:]
                uncov = self._uncovered_masks(rest)
                if len(uncov) == 0:
                    sol = rest
                    improved = True
                    self._report("optimize",
                                 f"Swap: removed -> {len(sol)} groups")
                    break
                # try to find single replacement covering ALL uncov
                for cm in self.cand_masks:
                    cm_int = int(cm)
                    if cm_int == sol[i]:
                        continue
                    ints = np.uint32(cm_int) & uncov
                    ok = (np.all(ints == uncov) if self._containment
                          else np.all(popcount_uint32(ints) >= self.s))
                    if ok:
                        sol = rest + [cm_int]
                        improved = True
                        break
                if improved:
                    break
            if not improved:
                break
        return sol

    # ------------------------------------------------------------------
    # Simulated annealing post-processing
    # ------------------------------------------------------------------

    def _sa_improve(self, sol: list[int], max_time: float = 10.0) -> list[int]:
        """Try to reduce solution size using simulated annealing swaps."""
        if len(sol) <= 3:
            return sol
        best = list(sol)
        current = list(sol)
        t0 = time.time()
        T = 1.0
        cooling = 0.995
        iters = 0
        best_len = len(best)

        cand_list = self.cand_masks.tolist()
        nc = len(cand_list)

        while T > 0.01 and not self._cancel():
            elapsed = time.time() - t0
            if elapsed > max_time:
                break

            # Random swap: replace one group with a random candidate
            idx = random.randrange(len(current))
            new_mask = cand_list[random.randrange(nc)]
            old_mask = current[idx]
            if new_mask == old_mask:
                continue

            current[idx] = new_mask
            if self._verify(current):
                # Try removing redundant groups
                trial = list(current)
                random.shuffle(trial)
                reduced = []
                rem_uncov = np.ones(self.num_targets, dtype=bool)
                for m in trial:
                    if not rem_uncov.any():
                        break
                    ints = np.uint32(m) & self.target_masks[rem_uncov]
                    if self._containment:
                        hits = np.any(ints == self.target_masks[rem_uncov])
                    else:
                        hits = np.any(popcount_uint32(ints) >= self.s)
                    if hits:
                        reduced.append(m)
                        self._mark_covered(m, rem_uncov)

                if self._verify(reduced) and len(reduced) < best_len:
                    best = reduced
                    best_len = len(best)
                    current = list(best)
                    self._report("sa",
                                 f"SA improved to {best_len} groups")
                elif len(current) <= len(best) + 1:
                    pass  # accept as current
                else:
                    # Accept worse with probability based on T
                    delta = len(current) - len(best)
                    if random.random() >= math.exp(-delta / T):
                        current[idx] = old_mask
            else:
                current[idx] = old_mask

            T *= cooling
            iters += 1

        return best

    # ------------------------------------------------------------------
    # Progress reporting
    # ------------------------------------------------------------------

    def _report(self, phase: str, msg: str, **kw: int) -> None:
        if self._cb:
            self._cb(SolverProgress(
                phase=phase,
                message=msg,
                iteration=kw.get("iteration", 0),
                solution_size=kw.get("sol_size", 0),
                remaining=kw.get("remaining", 0),
                total=self.num_targets,
                elapsed=time.time() - self._t0,
            ))
