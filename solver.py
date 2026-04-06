"""Covering design solver for the Optimal Samples Selection System.

Solves L(n, k, j, s): find minimum k-subsets of {0,...,n-1} such that
every j-subset shares at least s elements with at least one selected k-subset.

Optimisations:
  - Precomputed coverage table: for each candidate, which targets it covers
  - Incremental scoring: after choosing a group, only update affected candidates
  - Containment fast-path: O(C(k,j)) lookup table when s==j
  - Simulated annealing post-processing for medium-size solutions
  - Adaptive top-K heuristic for very large problems
  - Optional GPU batch scoring (CuPy) with automatic CPU fallback
"""

from __future__ import annotations

import math
import os
import random
import site
import time
from dataclasses import dataclass
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Callable

import numpy as np


def _add_windows_cuda_dll_dirs() -> None:
    """Make CuPy find CUDA DLLs from pip nvidia-* packages on Windows."""
    if os.name != "nt":
        return

    roots: list[Path] = []
    try:
        roots.extend(Path(p) for p in site.getsitepackages())
    except Exception:
        pass
    try:
        roots.append(Path(site.getusersitepackages()))
    except Exception:
        pass

    added: set[str] = set()
    for root in roots:
        nvidia_dir = root / "nvidia"
        if not nvidia_dir.exists():
            continue
        runtime_root = nvidia_dir / "cuda_runtime"
        if "CUDA_PATH" not in os.environ and runtime_root.exists():
            os.environ["CUDA_PATH"] = str(runtime_root)
        for pkg in ("cuda_nvrtc", "cuda_runtime", "nvjitlink"):
            bin_dir = nvidia_dir / pkg / "bin"
            if not bin_dir.exists():
                continue
            s = str(bin_dir)
            if s in added:
                continue
            try:
                os.add_dll_directory(s)  # type: ignore[attr-defined]
            except Exception:
                pass
            os.environ["PATH"] = s + os.pathsep + os.environ.get("PATH", "")
            added.add(s)


_add_windows_cuda_dll_dirs()

try:
    import cupy as cp  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cp = None


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
    first_legal_elapsed: float | None = None

    def __post_init__(self) -> None:
        self.num_groups = len(self.groups)


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------

def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


DEFAULT_BATCH_BYTES = 128 * 1024 * 1024
MAX_BATCH_BYTES = _env_int("CK_BATCH_BYTES", DEFAULT_BATCH_BYTES)


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
        self._first_legal_elapsed: float | None = None

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
        self._interaction_scale = self.num_targets * self.num_cands

        self._batch_bytes = MAX_BATCH_BYTES
        self._base_top_k = self._choose_top_k()
        self._cand_has_elem: np.ndarray | None = None
        self._target_has_elem: np.ndarray | None = None

        self._gpu_enabled = bool(
            _env_int("CK_USE_GPU", 1)
            and cp is not None
            and self._interaction_scale >= 500_000_000
        )
        self._gpu_failed = False

        self._cov_table: list[np.ndarray] | None = None
        self._inv_table: list[np.ndarray] | None = None
        self._jsub_table: np.ndarray | None = None

        mem_estimate = self.num_cands * self.num_targets
        if self._containment and mem_estimate > 20_000_000:
            self._build_jsub_table()
        elif mem_estimate <= 500_000_000:
            self._build_coverage_tables()
        elif self._containment:
            self._build_jsub_table()

        if self._cov_table is None:
            self._init_heuristic_cache()

    # ------------------------------------------------------------------
    # Precomputation
    # ------------------------------------------------------------------

    def _build_coverage_tables(self) -> None:
        """Build cov_table[ci]->targets and inv_table[ti]->candidates."""
        cov: list[list[int]] = [[] for _ in range(self.num_cands)]
        inv: list[list[int]] = [[] for _ in range(self.num_targets)]

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

        cov: list[list[int]] = [[] for _ in range(self.num_cands)]
        inv: list[list[int]] = [[] for _ in range(self.num_targets)]
        for ci in range(self.num_cands):
            for ti in table[ci]:
                tii = int(ti)
                cov[ci].append(tii)
                inv[tii].append(ci)
        self._cov_table = [np.array(c, dtype=np.int32) for c in cov]
        self._inv_table = [np.array(c, dtype=np.int32) for c in inv]

    def _init_heuristic_cache(self) -> None:
        bits = (np.uint32(1) << np.arange(self.n, dtype=np.uint32))
        self._cand_has_elem = (
            (self.cand_masks[:, None] & bits[None, :]) != 0
        ).astype(np.uint8, copy=False)
        self._target_has_elem = (
            (self.target_masks[:, None] & bits[None, :]) != 0
        ).astype(np.uint8, copy=False)

    def _choose_top_k(self) -> int:
        if self._interaction_scale >= 60_000_000_000:
            return min(600, self.num_cands)
        if self._interaction_scale >= 20_000_000_000:
            return min(800, self.num_cands)
        if self._interaction_scale >= 5_000_000_000:
            return min(1000, self.num_cands)
        if self._interaction_scale >= 1_000_000_000:
            return min(1200, self.num_cands)
        return min(2000, self.num_cands)

    def _top_k_for_remaining(self, remaining: int) -> int:
        top_k = self._base_top_k
        if remaining <= 20_000:
            top_k = min(self.num_cands, max(top_k, 1200))
        if remaining <= 5_000:
            top_k = min(self.num_cands, max(top_k, 2000))
        return max(1, top_k)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def solve(self) -> SolverResult:
        self._t0 = time.time()
        best: list[int] | None = None
        stagnant = 0

        if self._gpu_enabled:
            self._report("gpu", "GPU batch scoring enabled")

        if self._should_build_fast_seed():
            seed = self._fast_seed_solution()
            if seed:
                best = seed
                self._note_legal_solution()
                self._report("seed", f"Fast legal seed: {len(seed)} groups")

        num_att = self._effective_attempts()

        for attempt in range(1, num_att + 1):
            if self._cancel():
                break
            self._report("greedy", f"Attempt {attempt}/{num_att}: greedy...")
            sol, complete, remaining = self._greedy(randomize=attempt > 1)
            if complete and (best is None or len(sol) < len(best)):
                best = sol
                self._note_legal_solution()

            if self._cancel():
                if sol and not complete and self._should_repair_partial(remaining, best):
                    repaired = self._fast_complete_partial_solution(
                        sol,
                        best_limit=len(best) if best is not None else None,
                    )
                    if repaired and (best is None or len(repaired) < len(best)):
                        best = repaired
                        self._note_legal_solution()
                break
            if not complete:
                if sol and self._should_repair_partial(remaining, best):
                    repaired = self._fast_complete_partial_solution(
                        sol,
                        best_limit=len(best) if best is not None else None,
                    )
                    if repaired and (best is None or len(repaired) < len(best)):
                        best = repaired
                        self._note_legal_solution()
                break

            self._report("optimize", f"Attempt {attempt}: optimise ({len(sol)} groups)...")
            sol = self._local_search(sol)
            if not self._cancel() and self._allow_swap(sol):
                sol = self._swap_improve(sol)
                sol = self._local_search(sol)

            if not self._cancel() and 3 < len(sol) <= 200:
                sa_budget = self._sa_time_budget(sol)
                if sa_budget > 0:
                    sol = self._sa_improve(sol, max_time=sa_budget)
                sol = self._local_search(sol)

            improved = best is None or len(sol) < len(best)
            if improved:
                best = sol
                stagnant = 0
                self._note_legal_solution()
                self._report("optimize", f"Best so far: {len(best)} groups (attempt {attempt})")
            else:
                stagnant += 1

            if (
                attempt >= 2
                and stagnant >= 1
                and (self._interaction_scale >= 20_000_000 or self.num_targets >= 2_000)
            ):
                break

        masks = best or []
        return SolverResult(
            groups=[sorted(mask_to_elements(m)) for m in masks],
            elapsed=time.time() - self._t0,
            verified=self._verify(masks),
            first_legal_elapsed=self._first_legal_elapsed,
        )

    def _effective_attempts(self) -> int:
        """Scale attempts with instance size to avoid runaway runtime."""
        num_att = self._num_attempts
        if self._interaction_scale >= 900_000_000:
            return min(num_att, 1)
        if self._interaction_scale >= 120_000_000 or self.num_cands >= 30_000:
            return min(num_att, 2)
        if self.num_targets >= 700 or self.num_cands >= 5_000:
            return min(num_att, 2)
        return num_att

    def _allow_swap(self, sol: list[int]) -> bool:
        if len(sol) > 60:
            return False
        if self.num_cands > 12_000:
            return False
        if self.num_targets > 3_000:
            return False
        return self._interaction_scale <= 120_000_000

    def _sa_time_budget(self, sol: list[int]) -> float:
        if len(sol) <= 3:
            return 0.0
        if len(sol) > 120:
            return 0.0
        if self._interaction_scale >= 900_000_000:
            return 1.5
        if self._interaction_scale >= 300_000_000 or self.num_cands >= 30_000:
            return 2.0
        if self.num_targets >= 3_000:
            return 3.0
        if self._interaction_scale >= 120_000_000:
            return 4.0
        return 8.0

    # ------------------------------------------------------------------
    # Greedy dispatch
    # ------------------------------------------------------------------

    def _greedy(self, *, randomize: bool = False) -> tuple[list[int], bool, int]:
        if self._cov_table is not None:
            return self._greedy_incremental(randomize)
        return self._greedy_heuristic(randomize)

    def _greedy_incremental(self, randomize: bool) -> tuple[list[int], bool, int]:
        """Fast greedy using precomputed coverage + incremental score updates."""
        cov_table = self._cov_table
        inv_table = self._inv_table
        assert cov_table is not None and inv_table is not None

        uncov = np.ones(self.num_targets, dtype=bool)
        scores = np.array([len(c) for c in cov_table], dtype=np.int32)
        selected: list[int] = []
        iteration = 0
        log_interval = max(1, self.num_targets // 500)
        rem = self.num_targets

        while rem > 0:
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

            newly_covered = cov_table[best_idx][uncov[cov_table[best_idx]]]
            if len(newly_covered) == 0:
                break
            uncov[newly_covered] = False
            for ti in newly_covered:
                affected = inv_table[ti]
                scores[affected] -= 1

            iteration += 1
            rem -= len(newly_covered)
            if iteration % log_interval == 0 or rem == 0:
                self._report(
                    "greedy",
                    f"Iter {iteration}: +1 (covers {len(newly_covered)}), {rem} left",
                    iteration=iteration,
                    sol_size=len(selected),
                    remaining=rem,
                )
        return selected, rem == 0, rem

    def _greedy_heuristic(self, randomize: bool) -> tuple[list[int], bool, int]:
        uncov = np.ones(self.num_targets, dtype=bool)
        selected: list[int] = []
        iteration = 0
        rem = self.num_targets

        while rem > 0:
            if self._cancel():
                break
            if self._should_finish_fast(rem):
                tail = self._fast_complete_selected(selected, uncov)
                if tail:
                    return tail, True, 0
                break
            mask, cnt = self._heuristic_pick(uncov, rem, randomize)
            if cnt == 0:
                break
            selected.append(mask)
            self._mark_covered(mask, uncov)
            iteration += 1
            rem = int(uncov.sum())
            self._report(
                "greedy",
                f"Iter {iteration}: +1 (covers {cnt}), {rem} left",
                iteration=iteration,
                sol_size=len(selected),
                remaining=rem,
            )
        return selected, rem == 0, rem

    def _heuristic_pick(
        self, uncov: np.ndarray, remaining: int, randomize: bool,
    ) -> tuple[int, int]:
        """Element-frequency heuristic then top-K exact evaluation."""
        cand_has = self._cand_has_elem
        target_has = self._target_has_elem
        assert cand_has is not None and target_has is not None

        freq = target_has[uncov].sum(axis=0, dtype=np.int64)
        h = cand_has @ freq

        top_k = self._top_k_for_remaining(remaining)
        if top_k < self.num_cands:
            top_idx = np.argpartition(h, -top_k)[-top_k:]
        else:
            top_idx = np.arange(self.num_cands)
        top_cands = self.cand_masks[top_idx]
        uncov_t = self.target_masks[uncov]

        if randomize:
            raw_counts = self._batch_scores(top_cands, uncov_t)
            noisy = raw_counts.astype(np.float64)
            noisy += np.random.random(len(noisy)) * 0.5
            best_local = int(np.argmax(noisy))
            return int(top_cands[best_local]), int(raw_counts[best_local])

        best_local, best_count = self._batch_best(top_cands, uncov_t)
        return int(top_cands[best_local]), best_count

    # ------------------------------------------------------------------
    # Batch scoring
    # ------------------------------------------------------------------

    def _batch_scores(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> np.ndarray:
        if (
            self._gpu_enabled
            and not self._gpu_failed
            and len(cands) >= 256
            and len(targets) >= 4096
        ):
            try:
                return self._batch_scores_gpu(cands, targets)
            except Exception:
                self._gpu_failed = True
                self._report("gpu", "GPU path failed; falling back to CPU")
        return self._batch_scores_cpu(cands, targets)

    def _batch_best(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> tuple[int, int]:
        if (
            self._gpu_enabled
            and not self._gpu_failed
            and len(cands) >= 256
            and len(targets) >= 4096
        ):
            try:
                return self._batch_best_gpu(cands, targets)
            except Exception:
                self._gpu_failed = True
                self._report("gpu", "GPU path failed; falling back to CPU")
        return self._batch_best_cpu(cands, targets)

    def _batch_scores_cpu(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> np.ndarray:
        nc, nt = len(cands), len(targets)
        scores = np.zeros(nc, dtype=np.int32)
        bs = max(1, self._batch_bytes // max(1, nt * 12))
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

    def _batch_best_cpu(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> tuple[int, int]:
        nc, nt = len(cands), len(targets)
        bs = max(1, self._batch_bytes // max(1, nt * 12))
        bs = min(bs, nc)
        best_local = 0
        best_count = -1

        for i in range(0, nc, bs):
            if self._cancel():
                break
            batch = cands[i : i + bs]
            ints = batch[:, None] & targets[None, :]
            if self._containment:
                counts = np.sum(ints == targets[None, :], axis=1)
            else:
                counts = np.sum(popcount_uint32(ints) >= self.s, axis=1)
            batch_best = int(np.argmax(counts))
            batch_count = int(counts[batch_best])
            if batch_count > best_count:
                best_count = batch_count
                best_local = i + batch_best

        return best_local, max(0, best_count)

    def _batch_scores_gpu(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> np.ndarray:
        assert cp is not None
        cands_gpu = cp.asarray(cands, dtype=cp.uint32)
        targets_gpu = cp.asarray(targets, dtype=cp.uint32)
        scores_gpu = cp.zeros(len(cands), dtype=cp.int32)

        free_mem, _ = cp.cuda.Device().mem_info
        approx_bytes_per_target = max(4, len(cands) * 12)
        chunk = int(max(2048, min(
            len(targets),
            (free_mem * 0.2) // approx_bytes_per_target
        )))

        for start in range(0, len(targets), chunk):
            if self._cancel():
                break
            t_chunk = targets_gpu[start : start + chunk]
            ints = cands_gpu[:, None] & t_chunk[None, :]
            if self._containment:
                hits = ints == t_chunk[None, :]
            else:
                hits = self._gpu_popcount_uint32(ints) >= self.s
            scores_gpu += cp.sum(hits, axis=1, dtype=cp.int32)
        return cp.asnumpy(scores_gpu)

    def _batch_best_gpu(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> tuple[int, int]:
        assert cp is not None
        cands_gpu = cp.asarray(cands, dtype=cp.uint32)
        targets_gpu = cp.asarray(targets, dtype=cp.uint32)
        scores_gpu = cp.zeros(len(cands), dtype=cp.int32)

        free_mem, _ = cp.cuda.Device().mem_info
        approx_bytes_per_target = max(4, len(cands) * 12)
        chunk = int(max(2048, min(
            len(targets),
            (free_mem * 0.2) // approx_bytes_per_target
        )))

        for start in range(0, len(targets), chunk):
            if self._cancel():
                break
            t_chunk = targets_gpu[start : start + chunk]
            ints = cands_gpu[:, None] & t_chunk[None, :]
            if self._containment:
                hits = ints == t_chunk[None, :]
            else:
                hits = self._gpu_popcount_uint32(ints) >= self.s
            scores_gpu += cp.sum(hits, axis=1, dtype=cp.int32)

        best_local = int(cp.argmax(scores_gpu).get())
        best_count = int(scores_gpu[best_local].get())
        return best_local, best_count

    @staticmethod
    def _gpu_popcount_uint32(arr):
        assert cp is not None
        x = cp.array(arr, dtype=cp.uint32, copy=True)
        t = (x >> cp.uint32(1)) & cp.uint32(0x55555555)
        x = x - t
        t = x & cp.uint32(0x33333333)
        x = (x >> cp.uint32(2)) & cp.uint32(0x33333333)
        x = x + t
        x = x + (x >> cp.uint32(4))
        x = x & cp.uint32(0x0F0F0F0F)
        x = x * cp.uint32(0x01010101)
        x = x >> cp.uint32(24)
        return x.astype(cp.int32)

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
    # Local search
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
                    self._report("optimize", f"Removed redundant -> {len(sol)} groups")
                    break
        return sol

    def _local_search_fast(self, sol: list[int]) -> list[int]:
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
                    self._report("optimize", f"Removed redundant -> {len(sol)} groups")
        return sol

    def _covers_bool(self, mask: int) -> np.ndarray:
        ints = np.uint32(mask) & self.target_masks
        if self._containment:
            return ints == self.target_masks
        return popcount_uint32(ints) >= self.s

    def _swap_improve(self, sol: list[int], rounds: int = 3) -> list[int]:
        if len(sol) > 60:
            return sol
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
                    self._report("optimize", f"Swap: removed -> {len(sol)} groups")
                    break
                for cm in self.cand_masks:
                    cm_int = int(cm)
                    if cm_int == sol[i]:
                        continue
                    ints = np.uint32(cm_int) & uncov
                    ok = (
                        np.all(ints == uncov)
                        if self._containment
                        else np.all(popcount_uint32(ints) >= self.s)
                    )
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
        if len(sol) <= 3:
            return sol
        best = list(sol)
        current = list(sol)
        t0 = time.time()
        T = 1.0
        cooling = 0.995
        best_len = len(best)

        cand_list = self.cand_masks.tolist()
        nc = len(cand_list)

        while T > 0.01 and not self._cancel():
            if (time.time() - t0) > max_time:
                break

            idx = random.randrange(len(current))
            new_mask = cand_list[random.randrange(nc)]
            old_mask = current[idx]
            if new_mask == old_mask:
                continue

            current[idx] = new_mask
            if self._verify(current):
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
                    self._report("sa", f"SA improved to {best_len} groups")
                elif len(current) <= len(best) + 1:
                    pass
                else:
                    delta = len(current) - len(best)
                    if random.random() >= math.exp(-delta / T):
                        current[idx] = old_mask
            else:
                current[idx] = old_mask

            T *= cooling

        return best

    # ------------------------------------------------------------------
    # Progress reporting
    # ------------------------------------------------------------------

    def _report(self, phase: str, msg: str, **kw: int) -> None:
        if self._cb:
            self._cb(
                SolverProgress(
                    phase=phase,
                    message=msg,
                    iteration=kw.get("iteration", 0),
                    solution_size=kw.get("sol_size", 0),
                    remaining=kw.get("remaining", 0),
                    total=self.num_targets,
                    elapsed=time.time() - self._t0,
                )
            )

    def _should_build_fast_seed(self) -> bool:
        return (
            self._cov_table is None
            and (self.num_targets >= 20_000 or self._interaction_scale >= 1_000_000_000)
        )

    def _note_legal_solution(self) -> None:
        if self._first_legal_elapsed is None:
            self._first_legal_elapsed = time.time() - self._t0

    def _fast_seed_solution(self) -> list[int]:
        return self._fast_complete_partial_solution([])

    def _fast_complete_partial_solution(
        self,
        partial: list[int],
        *,
        best_limit: int | None = None,
    ) -> list[int] | None:
        uncovered = np.ones(self.num_targets, dtype=bool)
        selected = list(partial)
        for mask in selected:
            self._mark_covered(mask, uncovered)

        return self._fast_complete_selected(
            selected,
            uncovered,
            best_limit=best_limit,
        )

    def _fast_complete_selected(
        self,
        selected: list[int],
        uncovered: np.ndarray,
        *,
        best_limit: int | None = None,
    ) -> list[int] | None:
        rem = int(uncovered.sum())

        if rem == 0:
            return selected

        chosen = set(selected)
        iteration = 0
        log_interval = max(1, self.num_targets // 500)
        freq = self._fast_completion_freq(uncovered)

        while rem > 0:
            if best_limit is not None and len(selected) >= best_limit:
                return None
            target_idx = int(np.argmax(uncovered))
            if not uncovered[target_idx]:
                break
            mask = self._canonical_cover_mask(
                int(self.target_masks[target_idx]),
                chosen,
                freq=freq,
            )
            if mask not in chosen:
                selected.append(mask)
                chosen.add(mask)
            self._mark_covered(mask, uncovered)
            iteration += 1
            rem = int(uncovered.sum())
            if iteration % 128 == 0:
                freq = self._fast_completion_freq(uncovered)
            if iteration % log_interval == 0 or rem == 0:
                self._report(
                    "seed",
                    f"Seed/repair iter {iteration}: {rem} left",
                    iteration=iteration,
                    sol_size=len(selected),
                    remaining=rem,
                )

        return selected

    def _canonical_cover_mask(
        self,
        target_mask: int,
        chosen: set[int],
        *,
        freq: np.ndarray | None = None,
    ) -> int:
        target_elems = mask_to_elements(target_mask)
        need = self.k - len(target_elems)
        if need <= 0:
            return target_mask

        available = [e for e in range(self.n) if not (target_mask & (1 << e))]
        if freq is not None and len(available) > 1:
            available.sort(key=lambda e: (-int(freq[e]), e))
        if need == 1:
            for extra in available:
                candidate = target_mask | (1 << extra)
                if candidate not in chosen:
                    return candidate
            return target_mask | (1 << available[0])

        candidate = target_mask
        for extra in available[:need]:
            candidate |= 1 << extra
        if candidate not in chosen:
            return candidate

        for extras in combinations(available, need):
            candidate = target_mask
            for extra in extras:
                candidate |= 1 << extra
            if candidate not in chosen:
                return candidate

        candidate = target_mask
        for extra in available[:need]:
            candidate |= 1 << extra
        return candidate

    def _should_repair_partial(self, remaining: int, best: list[int] | None) -> bool:
        if remaining <= 0:
            return False
        if best is None:
            return True
        limit = min(25_000, max(2_000, self.num_targets // 4))
        return remaining <= limit

    def _should_finish_fast(self, remaining: int) -> bool:
        if self._cov_table is not None:
            return False
        if self.num_targets < 100_000:
            return False
        return remaining <= 25_000

    def _fast_completion_freq(self, uncovered: np.ndarray) -> np.ndarray | None:
        if self._target_has_elem is None:
            return None
        return self._target_has_elem[uncovered].sum(axis=0, dtype=np.int64)
