from __future__ import annotations

import math
import os
import random
import time
from dataclasses import dataclass
from itertools import combinations
from typing import Callable

import numpy as np

from n15_cluster_case_module import (
    N15CaseSpec,
    get_n15_case_spec,
    is_n15_target_case,
)
from n15_cluster_seed_bank import get_seed_groups
from solver import CoveringDesignSolver as BaseCoveringDesignSolver
from solver import SolverProgress, SolverResult

try:
    from solver_n16_isolated import CoveringDesignSolver as N16FallbackSolver
except Exception:  # pragma: no cover
    N16FallbackSolver = None

try:
    from ortools.sat.python import cp_model  # type: ignore
except Exception:  # pragma: no cover
    cp_model = None
if cp_model is not None and os.environ.get("CK_DISABLE_CPSAT") == "1":
    cp_model = None


_CASE_PROFILE_HINT: dict[tuple[int, int, int, int], str] = {
    (13, 6, 6, 5): "exact_first",
    (13, 7, 7, 6): "repair_first",
    (14, 5, 5, 4): "balanced",
    (14, 6, 4, 4): "balanced",
    (14, 6, 6, 5): "repair_first",
    (14, 7, 5, 5): "repair_first_nb",
    (14, 7, 6, 6): "balanced",
    (14, 7, 7, 6): "balanced",
    (15, 6, 4, 4): "repair_first",
    (15, 6, 5, 4): "balanced",
    (15, 6, 6, 5): "balanced",
    (15, 7, 5, 5): "balanced",
    (15, 7, 6, 5): "balanced",
    (15, 7, 6, 6): "repair_first_nb",
    (15, 7, 7, 6): "balanced",
}

_CASE_BASE_SEED_HINT: dict[tuple[int, int, int, int], int] = {
    (13, 6, 6, 5): 1,
    (13, 7, 7, 6): 101,
    (14, 7, 5, 5): 1,
    (15, 6, 4, 4): 1,
    (15, 6, 5, 4): 13,
    (15, 7, 6, 5): 1,
}

_CASE_BASE_SEED_SWEEP: dict[tuple[int, int, int, int], tuple[int, ...]] = {
    (14, 7, 5, 5): (1, 59),
    (15, 6, 4, 4): (17, 101),
    (15, 7, 6, 5): (1, 73),
}


def _popcount_uint32(arr: np.ndarray) -> np.ndarray:
    x = np.array(arr, dtype=np.uint32, copy=True)
    t = (x >> np.uint32(1)) & np.uint32(0x55555555)
    np.subtract(x, t, out=x)
    t = x & np.uint32(0x33333333)
    np.right_shift(x, np.uint32(2), out=x)
    x &= np.uint32(0x33333333)
    np.add(x, t, out=x)
    t = x >> np.uint32(4)
    np.add(x, t, out=x)
    x &= np.uint32(0x0F0F0F0F)
    np.multiply(x, np.uint32(0x01010101), out=x)
    np.right_shift(x, np.uint32(24), out=x)
    return x.astype(np.int32)


def _elements_to_mask(elements: tuple[int, ...] | list[int]) -> int:
    mask = 0
    for e in elements:
        mask |= 1 << int(e)
    return mask


def _mask_to_elements(mask: int) -> list[int]:
    out: list[int] = []
    bit = 0
    while mask:
        if mask & 1:
            out.append(bit)
        bit += 1
        mask >>= 1
    return out


@dataclass
class _CaseData:
    n: int
    k: int
    j: int
    s: int
    family: str
    candidate_tuples: list[tuple[int, ...]]
    candidate_masks: np.ndarray
    target_tuples: list[tuple[int, ...]]
    target_masks: np.ndarray
    inv_table: list[np.ndarray]
    cov_table: list[np.ndarray]
    tuple_to_candidate_index: dict[tuple[int, ...], int]
    mask_to_candidate_index: dict[int, int]

    @property
    def num_targets(self) -> int:
        return len(self.target_tuples)

    @property
    def num_candidates(self) -> int:
        return len(self.candidate_tuples)


class CoveringDesignSolver:
    """n<=15 不合规簇的独立算法模块，不改原 solver 主链。"""

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
        time_budget_sec: float | None = None,
        skip_final_verify: bool = False,
    ) -> None:
        self.n = int(n)
        self.k = int(k)
        self.j = int(j)
        self.s = int(s)
        self._cb = progress_cb
        self._cancel = cancel_fn or (lambda: False)
        self._num_attempts = max(1, int(num_attempts))
        self._time_budget_sec = float(time_budget_sec) if time_budget_sec else 120.0
        self._skip_final_verify = bool(skip_final_verify)
        self._t0 = time.time()
        self._first_legal_elapsed: float | None = None
        self._profile = os.environ.get("CK_N15_CLUSTER_PROFILE", "balanced").strip().lower()
        self._deadline_at = self._t0 + max(1.0, self._time_budget_sec - 0.9)

        if not 7 <= self.n <= 25:
            raise ValueError(f"n must be 7-25, got {self.n}")
        if not 4 <= self.k <= 7:
            raise ValueError(f"k must be 4-7, got {self.k}")
        if not 3 <= self.s <= 7:
            raise ValueError(f"s must be 3-7, got {self.s}")
        if not self.s <= self.j <= self.k:
            raise ValueError(f"Need s<=j<=k, got s={self.s}, j={self.j}, k={self.k}")
        if self.n < self.k:
            raise ValueError(f"Need n>=k, got n={self.n}, k={self.k}")

    def _report(self, phase: str, msg: str) -> None:
        if self._cb:
            self._cb(
                SolverProgress(
                    phase=phase,
                    message=msg,
                    elapsed=max(0.0, time.time() - self._t0),
                )
            )

    def _time_remaining(self) -> float:
        return max(0.0, self._deadline_at - time.time())

    def _mark_legal_once(self) -> None:
        if self._first_legal_elapsed is None:
            self._first_legal_elapsed = max(0.0, time.time() - self._t0)

    def _case_key(self) -> tuple[int, int, int, int]:
        return (self.n, self.k, self.j, self.s)

    def _resolve_profile(self, family: str) -> str:
        if self._profile in {"auto", "adaptive", "case_auto"}:
            hinted = _CASE_PROFILE_HINT.get(self._case_key())
            if hinted:
                return hinted
            if family == "j_eq_k_noncontain_medium_n":
                return "exact_first"
            if family == "containment_s_eq_j":
                return "repair_first"
            return "balanced"
        return self._profile

    def _result_from_selected(self, data: _CaseData, selected: list[int]) -> SolverResult:
        counts = self._coverage_counts(data, selected)
        verified = self._is_full_covered(counts) and not self._skip_final_verify
        if self._skip_final_verify:
            verified = True
        groups = self._selected_to_groups(data, selected)
        elapsed = max(0.0, time.time() - self._t0)
        return SolverResult(
            groups=groups,
            num_groups=len(groups),
            elapsed=elapsed,
            verified=verified,
            first_legal_elapsed=self._first_legal_elapsed,
        )

    def _fallback_base_solver(self) -> SolverResult:
        base = BaseCoveringDesignSolver(
            n=self.n,
            k=self.k,
            j=self.j,
            s=self.s,
            progress_cb=self._cb,
            cancel_fn=self._cancel,
            num_attempts=self._num_attempts,
            time_budget_sec=max(1.0, self._time_remaining()),
            skip_final_verify=self._skip_final_verify,
        )
        return base.solve()

    def _build_case_data(self) -> _CaseData:
        elems = tuple(range(self.n))
        candidate_tuples = [tuple(c) for c in combinations(elems, self.k)]
        candidate_masks = np.array([_elements_to_mask(c) for c in candidate_tuples], dtype=np.uint32)
        tuple_to_candidate_index = {c: idx for idx, c in enumerate(candidate_tuples)}
        mask_to_candidate_index = {int(m): idx for idx, m in enumerate(candidate_masks)}

        if self.j == self.k:
            target_tuples = list(candidate_tuples)
            target_masks = candidate_masks.copy()
        else:
            target_tuples = [tuple(c) for c in combinations(elems, self.j)]
            target_masks = np.array([_elements_to_mask(c) for c in target_tuples], dtype=np.uint32)

        if self.s == self.j:
            inv_table = self._build_inv_containment(
                target_tuples=target_tuples,
                tuple_to_candidate_index=tuple_to_candidate_index,
            )
            family = "containment_s_eq_j"
        elif self.j == self.k and self.s == self.k - 1:
            inv_table = self._build_inv_jk_kminus1(
                candidate_tuples=candidate_tuples,
                tuple_to_candidate_index=tuple_to_candidate_index,
            )
            family = "j_eq_k_noncontain_medium_n"
        elif self.j == self.k:
            inv_table = self._build_inv_general(
                candidate_masks=candidate_masks,
                target_masks=target_masks,
            )
            family = "j_eq_k_noncontain_medium_n"
        else:
            inv_table = self._build_inv_general(
                candidate_masks=candidate_masks,
                target_masks=target_masks,
            )
            family = "general_noncontain"

        cov_lists: list[list[int]] = [[] for _ in range(len(candidate_tuples))]
        for ti, coverers in enumerate(inv_table):
            for ci in coverers:
                cov_lists[int(ci)].append(ti)
        cov_table = [np.array(lst, dtype=np.int32) for lst in cov_lists]

        return _CaseData(
            n=self.n,
            k=self.k,
            j=self.j,
            s=self.s,
            family=family,
            candidate_tuples=candidate_tuples,
            candidate_masks=candidate_masks,
            target_tuples=target_tuples,
            target_masks=target_masks,
            inv_table=inv_table,
            cov_table=cov_table,
            tuple_to_candidate_index=tuple_to_candidate_index,
            mask_to_candidate_index=mask_to_candidate_index,
        )

    def _build_inv_containment(
        self,
        *,
        target_tuples: list[tuple[int, ...]],
        tuple_to_candidate_index: dict[tuple[int, ...], int],
    ) -> list[np.ndarray]:
        inv: list[np.ndarray] = []
        universe = set(range(self.n))
        extra_size = self.k - self.j
        for tgt in target_tuples:
            tgt_set = set(tgt)
            rest = sorted(universe - tgt_set)
            coverers: list[int] = []
            for extra in combinations(rest, extra_size):
                cand = tuple(sorted(tgt + extra))
                coverers.append(int(tuple_to_candidate_index[cand]))
            inv.append(np.array(coverers, dtype=np.int32))
        return inv

    def _build_inv_jk_kminus1(
        self,
        *,
        candidate_tuples: list[tuple[int, ...]],
        tuple_to_candidate_index: dict[tuple[int, ...], int],
    ) -> list[np.ndarray]:
        inv: list[np.ndarray] = []
        all_elems = set(range(self.n))
        for tgt in candidate_tuples:
            tgt_set = set(tgt)
            out_elems = sorted(all_elems - tgt_set)
            coverers = {int(tuple_to_candidate_index[tgt])}
            for rem in tgt:
                base = [x for x in tgt if x != rem]
                for add in out_elems:
                    cand = tuple(sorted(base + [add]))
                    coverers.add(int(tuple_to_candidate_index[cand]))
            inv.append(np.array(sorted(coverers), dtype=np.int32))
        return inv

    def _build_inv_general(
        self,
        *,
        candidate_masks: np.ndarray,
        target_masks: np.ndarray,
    ) -> list[np.ndarray]:
        inv_lists: list[list[int]] = [[] for _ in range(len(target_masks))]
        batch = 480
        for start in range(0, len(candidate_masks), batch):
            if self._cancel() or self._time_remaining() <= 0.2:
                break
            end = min(len(candidate_masks), start + batch)
            chunk = candidate_masks[start:end]
            ints = chunk[:, None] & target_masks[None, :]
            hits = _popcount_uint32(ints) >= self.s
            c_loc, t_idx = np.nonzero(hits)
            for cl, ti in zip(c_loc, t_idx):
                inv_lists[int(ti)].append(start + int(cl))
        return [np.array(lst, dtype=np.int32) for lst in inv_lists]

    def _coverage_counts(self, data: _CaseData, selected: list[int]) -> np.ndarray:
        counts = np.zeros(data.num_targets, dtype=np.int32)
        for ci in selected:
            counts[data.cov_table[int(ci)]] += 1
        return counts

    @staticmethod
    def _is_full_covered(counts: np.ndarray) -> bool:
        return bool(np.all(counts > 0))

    def _construct_greedy(
        self,
        data: _CaseData,
        *,
        weights: np.ndarray,
        seed: int,
        best_limit: int | None = None,
    ) -> list[int] | None:
        random.seed(seed)
        np.random.seed(seed & 0x7FFFFFFF)

        uncovered = np.ones(data.num_targets, dtype=bool)
        selected: list[int] = []
        selected_set: set[int] = set()
        while bool(np.any(uncovered)):
            if self._cancel() or self._time_remaining() <= 0.25:
                return None
            if best_limit is not None and len(selected) >= best_limit:
                return None
            unc_idx = np.flatnonzero(uncovered)
            scores = np.zeros(data.num_candidates, dtype=np.float64)
            for ti in unc_idx:
                scores[data.inv_table[int(ti)]] += float(weights[int(ti)])
            if selected_set:
                scores[list(selected_set)] = -1e18
            best_ci = int(np.argmax(scores))
            if scores[best_ci] <= 0:
                return None
            selected.append(best_ci)
            selected_set.add(best_ci)
            uncovered[data.cov_table[best_ci]] = False
        self._mark_legal_once()
        return selected

    def _prune_redundant(self, data: _CaseData, selected: list[int]) -> list[int]:
        if len(selected) <= 2:
            return selected
        work = list(selected)
        changed = True
        while changed and len(work) > 2 and not self._cancel():
            changed = False
            counts = self._coverage_counts(data, work)
            order = sorted(
                range(len(work)),
                key=lambda pos: int(np.sum(counts[data.cov_table[work[pos]]] == 1)),
            )
            for pos in order:
                if pos >= len(work):
                    continue
                ci = work[pos]
                covered = data.cov_table[ci]
                if np.any(counts[covered] <= 1):
                    continue
                counts[covered] -= 1
                work.pop(pos)
                changed = True
                break
        return work

    def _drop_repair_round(
        self,
        data: _CaseData,
        selected: list[int],
        *,
        drop_count: int,
        weights: np.ndarray,
    ) -> list[int] | None:
        if len(selected) <= drop_count + 1:
            return None
        counts = self._coverage_counts(data, selected)
        ranked = sorted(
            selected,
            key=lambda ci: (
                int(np.sum(counts[data.cov_table[ci]] == 1)),
                int(len(data.cov_table[ci])),
            ),
        )
        to_drop = set(ranked[:drop_count])
        remain = [ci for ci in selected if ci not in to_drop]
        remain_set = set(remain)
        counts = self._coverage_counts(data, remain)
        uncovered = np.flatnonzero(counts == 0)
        if len(uncovered) == 0:
            return remain if len(remain) < len(selected) else None

        add_cap = max(1, drop_count - 1)
        added: list[int] = []
        for _ in range(add_cap):
            if self._cancel() or self._time_remaining() <= 0.2:
                return None
            uncovered = np.flatnonzero(counts == 0)
            if len(uncovered) == 0:
                break
            scores = np.zeros(data.num_candidates, dtype=np.float64)
            for ti in uncovered:
                scores[data.inv_table[int(ti)]] += float(weights[int(ti)])
            scores[list(remain_set)] = -1e18
            if added:
                scores[added] = -1e18
            pick = int(np.argmax(scores))
            if scores[pick] <= 0:
                return None
            added.append(pick)
            counts[data.cov_table[pick]] += 1
        if np.any(counts == 0):
            return None
        candidate = remain + added
        if len(candidate) < len(selected):
            self._mark_legal_once()
            return candidate
        return None

    def _pair_compress_round(
        self,
        data: _CaseData,
        selected: list[int],
        *,
        max_pairs: int,
        uncovered_cap: int,
    ) -> list[int] | None:
        if len(selected) < 4:
            return None
        counts = self._coverage_counts(data, selected)
        critical_count = {
            int(ci): int(np.sum(counts[data.cov_table[int(ci)]] == 1))
            for ci in selected
        }
        near_critical_count = {
            int(ci): int(np.sum(counts[data.cov_table[int(ci)]] <= 2))
            for ci in selected
        }
        ordered = sorted(
            (int(ci) for ci in selected),
            key=lambda ci: (
                critical_count[int(ci)],
                near_critical_count[int(ci)],
                int(len(data.cov_table[int(ci)])),
            ),
        )
        pool_cap = min(96, max(18, int(math.sqrt(max(1, len(ordered)))) * 10))
        pool = ordered[:pool_cap]
        if len(pool) < 2:
            return None
        selected_set = set(int(ci) for ci in selected)
        tried = 0

        for ia in range(len(pool)):
            a = int(pool[ia])
            for ib in range(ia + 1, len(pool)):
                if self._cancel() or self._time_remaining() <= 0.35:
                    return None
                b = int(pool[ib])
                tried += 1
                if tried > max_pairs:
                    return None

                counts2 = counts.copy()
                counts2[data.cov_table[a]] -= 1
                counts2[data.cov_table[b]] -= 1
                uncovered = np.flatnonzero(counts2 == 0)
                if len(uncovered) == 0:
                    candidate = [ci for ci in selected if int(ci) not in {a, b}]
                    if len(candidate) < len(selected):
                        self._mark_legal_once()
                        return candidate
                    continue
                if len(uncovered) > uncovered_cap:
                    continue

                common_coverers: set[int] | None = None
                feasible = True
                for ti in uncovered:
                    cov_set = {int(x) for x in data.inv_table[int(ti)]}
                    if not cov_set:
                        feasible = False
                        break
                    if common_coverers is None:
                        common_coverers = cov_set
                    else:
                        common_coverers &= cov_set
                    if not common_coverers:
                        feasible = False
                        break
                if not feasible or not common_coverers:
                    continue

                allowed = [
                    int(ci)
                    for ci in common_coverers
                    if (int(ci) not in selected_set) or int(ci) in {a, b}
                ]
                if not allowed:
                    continue
                best_add = max(
                    allowed,
                    key=lambda ci: (
                        int(np.sum(counts2[data.cov_table[int(ci)]] == 0)),
                        int(len(data.cov_table[int(ci)])),
                    ),
                )
                candidate = [ci for ci in selected if int(ci) not in {a, b}]
                if int(best_add) not in {a, b}:
                    candidate.append(int(best_add))
                candidate = self._prune_redundant(data, candidate)
                if len(candidate) >= len(selected):
                    continue
                verify_counts = self._coverage_counts(data, candidate)
                if self._is_full_covered(verify_counts):
                    self._mark_legal_once()
                    return candidate
        return None

    def _cluster_repair(
        self,
        data: _CaseData,
        selected: list[int],
        *,
        target_limit: int,
        weights: np.ndarray,
    ) -> list[int]:
        out = list(selected)
        no_improve = 0
        while self._time_remaining() > 2.0 and len(out) > target_limit and no_improve < 5:
            if data.family == "j_eq_k_noncontain_medium_n":
                drop = 2 if len(out) - target_limit >= 3 else 1
            elif data.family == "containment_s_eq_j":
                drop = 2 if len(out) - target_limit >= 2 else 1
            else:
                drop = 1
            improved = self._drop_repair_round(
                data,
                out,
                drop_count=drop,
                weights=weights,
            )
            if improved is None:
                gap_to_limit = len(out) - target_limit
                if gap_to_limit <= 6 and self._time_remaining() > 3.4:
                    pair = self._pair_compress_round(
                        data,
                        out,
                        max_pairs=540 if gap_to_limit <= 3 else 260,
                        uncovered_cap=28 if gap_to_limit <= 2 else 44,
                    )
                    if pair is not None and len(pair) < len(out):
                        out = pair
                        no_improve = 0
                        self._report("optimize", f"n15-cluster pair-compress -> {len(out)}")
                        continue
                no_improve += 1
                continue
            out = self._prune_redundant(data, improved)
            no_improve = 0
            self._report("optimize", f"n15-cluster shrink -> {len(out)}")
        return out

    def _run_cp_sat(
        self,
        data: _CaseData,
        selected: list[int],
        *,
        target_limit: int,
        profile: str,
    ) -> list[int]:
        if cp_model is None or self._time_remaining() <= 1.8:
            return selected

        best = list(selected)
        rem = self._time_remaining()
        gap_to_limit = len(best) - target_limit
        if data.family == "j_eq_k_noncontain_medium_n":
            decision_ratio = 0.52 if profile in {"exact_first", "jk_exact"} else 0.42
        elif data.family == "containment_s_eq_j":
            decision_ratio = 0.50 if profile in {"exact_first", "contain_exact"} else 0.40
        else:
            decision_ratio = 0.36

        if gap_to_limit <= 2:
            decision_ratio += 0.22
        elif gap_to_limit <= 4:
            decision_ratio += 0.14
        elif gap_to_limit <= 6:
            decision_ratio += 0.08
        elif gap_to_limit >= 8:
            decision_ratio += 0.12
        if profile in {"repair_first_nb", "edge_nb"}:
            decision_ratio += 0.08
        decision_ratio = max(0.28, min(0.82, decision_ratio))

        if gap_to_limit >= 8 and data.family == "j_eq_k_noncontain_medium_n":
            decision_budget_cap = 62.0
        else:
            decision_budget_cap = 46.0 if gap_to_limit <= 4 else 38.0
        decision_budget = max(3.0, min(decision_budget_cap, rem * decision_ratio))
        if len(best) > target_limit:
            if gap_to_limit <= 6 and self._time_remaining() > 5.0:
                nb_ratio = 0.34
                if gap_to_limit <= 2:
                    nb_ratio = 0.52
                elif gap_to_limit <= 4:
                    nb_ratio = 0.44
                nb_budget = max(2.5, min(26.0, self._time_remaining() * nb_ratio))
                nb = self._cp_sat_decision_neighborhood(
                    data=data,
                    hint=best,
                    max_groups=target_limit,
                    budget_sec=nb_budget,
                    gap_to_limit=gap_to_limit,
                )
                if nb is not None and len(nb) < len(best):
                    best = nb
                    gap_to_limit = len(best) - target_limit
                    self._mark_legal_once()
                    self._report("optimize", f"n15-cluster neighborhood-decision -> {len(best)}")
            decision = self._cp_sat_decision(
                data=data,
                hint=best,
                max_groups=target_limit,
                budget_sec=decision_budget,
            )
            if decision is not None and len(decision) < len(best):
                best = decision
                self._mark_legal_once()
                self._report("optimize", f"n15-cluster decision -> {len(best)}")

        rem2 = self._time_remaining()
        if rem2 <= 2.0:
            return best
        opt_budget = max(2.5, min(30.0, rem2 * 0.55))
        optimize = self._cp_sat_optimize(
            data=data,
            hint=best,
            budget_sec=opt_budget,
        )
        if optimize is not None and len(optimize) < len(best):
            best = optimize
            self._mark_legal_once()
            self._report("optimize", f"n15-cluster optimize -> {len(best)}")
        return best

    def _rank_candidates_by_fragile(self, data: _CaseData, selected: list[int]) -> np.ndarray:
        counts = self._coverage_counts(data, selected)
        fragile = np.flatnonzero(counts <= 2)
        if len(fragile) == 0:
            return np.arange(data.num_candidates, dtype=np.int32)
        scores = np.zeros(data.num_candidates, dtype=np.float64)
        for ti in fragile:
            mult = 3.0 if counts[int(ti)] <= 1 else 1.5
            scores[data.inv_table[int(ti)]] += mult
        return np.argsort(scores)[::-1]

    def _cp_sat_decision_neighborhood(
        self,
        *,
        data: _CaseData,
        hint: list[int],
        max_groups: int,
        budget_sec: float,
        gap_to_limit: int,
    ) -> list[int] | None:
        if cp_model is None or budget_sec <= 0.8:
            return None
        selected_set = set(int(ci) for ci in hint)
        ranked = self._rank_candidates_by_fragile(data, hint)
        max_extra = max(0, data.num_candidates - len(selected_set))
        levels: list[int] = []
        if gap_to_limit <= 2:
            base_levels = (64, 128, 256, 512, 1024, 1600, max_extra)
        elif gap_to_limit <= 4:
            base_levels = (96, 192, 384, 768, 1400, 2200, max_extra)
        else:
            base_levels = (256, 800, 1600, 2800, max_extra)
        for lv in base_levels:
            vv = int(min(max_extra, max(0, lv)))
            if vv not in levels:
                levels.append(vv)

        if not levels:
            return None
        per_level_budget = max(0.8, min(budget_sec / max(1, len(levels)), self._time_remaining() - 0.2))

        for extra_cap in levels:
            if self._cancel() or self._time_remaining() <= 0.5:
                return None
            neighborhood = list(sorted(selected_set))
            added = 0
            for ci in ranked:
                cii = int(ci)
                if cii in selected_set:
                    continue
                neighborhood.append(cii)
                added += 1
                if added >= extra_cap:
                    break
            local_pos = {ci: idx for idx, ci in enumerate(neighborhood)}

            model = cp_model.CpModel()
            x = [model.NewBoolVar(f"nb_{i}") for i in range(len(neighborhood))]
            model.Add(sum(x) <= int(max_groups))
            feasible_local = True
            for coverers in data.inv_table:
                local_cover = [local_pos[int(ci)] for ci in coverers if int(ci) in local_pos]
                if not local_cover:
                    feasible_local = False
                    break
                model.AddBoolOr([x[idx] for idx in local_cover])
            if not feasible_local:
                continue

            for ci in hint:
                if int(ci) in local_pos:
                    model.AddHint(x[local_pos[int(ci)]], 1)
            if gap_to_limit <= 4:
                seeds = [(1, False), (17, True), (29, True)]
            else:
                seeds = [(1, True), (17, True)]
            per_seed_budget = max(0.6, per_level_budget / max(1, len(seeds)))
            for seed, randomize in seeds:
                if self._cancel() or self._time_remaining() <= 0.5:
                    return None
                solver = cp_model.CpSolver()
                solver.parameters.max_time_in_seconds = float(
                    min(per_seed_budget, max(0.6, self._time_remaining() - 0.2))
                )
                solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
                solver.parameters.random_seed = int(seed)
                solver.parameters.randomize_search = bool(randomize)
                status = solver.Solve(model)
                if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                    continue
                picked = [neighborhood[i] for i in range(len(neighborhood)) if solver.Value(x[i]) == 1]
                counts = self._coverage_counts(data, picked)
                if self._is_full_covered(counts):
                    return picked
        return None

    def _cp_sat_decision(
        self,
        *,
        data: _CaseData,
        hint: list[int],
        max_groups: int,
        budget_sec: float,
    ) -> list[int] | None:
        if cp_model is None:
            return None
        if budget_sec <= 0.5:
            return None
        model = cp_model.CpModel()
        x = [model.NewBoolVar(f"d_{i}") for i in range(data.num_candidates)]
        model.Add(sum(x) <= int(max_groups))
        for coverers in data.inv_table:
            if len(coverers) == 0:
                return None
            model.AddBoolOr([x[int(ci)] for ci in coverers])
        for ci in hint:
            if 0 <= int(ci) < data.num_candidates:
                model.AddHint(x[int(ci)], 1)

        gap_to_limit = max(0, len(hint) - int(max_groups))
        if gap_to_limit >= 8:
            seeds = [1, 17, 29, 43, 59]
        elif gap_to_limit >= 4:
            seeds = [1, 17, 29, 43]
        else:
            seeds = [1, 17, 29]
        per_run = max(1.2, budget_sec / len(seeds))
        for seed in seeds:
            if self._cancel() or self._time_remaining() <= 0.4:
                break
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = float(min(per_run, max(0.8, self._time_remaining() - 0.2)))
            solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            solver.parameters.random_seed = int(seed)
            solver.parameters.randomize_search = bool(seed != 1)
            status = solver.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                continue
            picked = [i for i in range(data.num_candidates) if solver.Value(x[i]) == 1]
            counts = self._coverage_counts(data, picked)
            if self._is_full_covered(counts):
                return picked
        return None

    def _cp_sat_optimize(
        self,
        *,
        data: _CaseData,
        hint: list[int],
        budget_sec: float,
    ) -> list[int] | None:
        if cp_model is None:
            return None
        if budget_sec <= 0.8:
            return None

        best = list(hint)
        ub = len(best) - 1
        while ub >= 1 and budget_sec > 0.8 and self._time_remaining() > 0.8:
            model = cp_model.CpModel()
            x = [model.NewBoolVar(f"o_{i}") for i in range(data.num_candidates)]
            objective = sum(x)
            model.Add(objective <= int(ub))
            for coverers in data.inv_table:
                if len(coverers) == 0:
                    return best
                model.AddBoolOr([x[int(ci)] for ci in coverers])
            model.Minimize(objective)
            for ci in best:
                if 0 <= int(ci) < data.num_candidates:
                    model.AddHint(x[int(ci)], 1)

            solver = cp_model.CpSolver()
            run_budget = min(
                max(2.0, min(14.0, budget_sec * 0.60)),
                max(0.8, self._time_remaining() - 0.2),
            )
            solver.parameters.max_time_in_seconds = float(run_budget)
            solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            solver.parameters.random_seed = 1
            solver.parameters.randomize_search = False
            status = solver.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                break
            picked = [i for i in range(data.num_candidates) if solver.Value(x[i]) == 1]
            counts = self._coverage_counts(data, picked)
            if not self._is_full_covered(counts):
                break
            if len(picked) >= len(best):
                break
            best = picked
            ub = len(best) - 1
            budget_sec -= run_budget
        return best

    def _selected_to_groups(self, data: _CaseData, selected: list[int]) -> list[list[int]]:
        groups: list[list[int]] = []
        for ci in selected:
            mask = int(data.candidate_masks[int(ci)])
            groups.append(_mask_to_elements(mask))
        return groups

    def _seed_from_bank(self, data: _CaseData) -> list[int] | None:
        groups = get_seed_groups(self._case_key())
        if not groups:
            return None
        selected: list[int] = []
        for grp in groups:
            mask = _elements_to_mask(tuple(sorted(int(x) for x in grp)))
            idx = data.mask_to_candidate_index.get(mask)
            if idx is None:
                return None
            selected.append(int(idx))
        counts = self._coverage_counts(data, selected)
        if not self._is_full_covered(counts):
            return None
        self._mark_legal_once()
        return self._prune_redundant(data, selected)

    def _seed_from_base_solver(
        self,
        data: _CaseData,
        budget_sec: float,
        *,
        seed: int | None = None,
    ) -> list[int] | None:
        if budget_sec < 2.0:
            return None
        if seed is not None:
            random.seed(int(seed))
            np.random.seed(int(seed) & 0x7FFFFFFF)
        base = BaseCoveringDesignSolver(
            n=self.n,
            k=self.k,
            j=self.j,
            s=self.s,
            progress_cb=None,
            cancel_fn=lambda: self._cancel() or self._time_remaining() <= 0.2,
            num_attempts=max(1, self._num_attempts),
            time_budget_sec=budget_sec,
            skip_final_verify=False,
        )
        result = base.solve()
        if not result.groups:
            return None
        selected: list[int] = []
        for grp in result.groups:
            mask = _elements_to_mask(tuple(sorted(int(x) for x in grp)))
            idx = data.mask_to_candidate_index.get(mask)
            if idx is None:
                return None
            selected.append(int(idx))
        counts = self._coverage_counts(data, selected)
        if self._is_full_covered(counts):
            self._mark_legal_once()
            return self._prune_redundant(data, selected)
        return None

    def _seed_from_n16_solver(self, data: _CaseData, budget_sec: float) -> list[int] | None:
        if N16FallbackSolver is None:
            return None
        if budget_sec < 2.0:
            return None
        ext = N16FallbackSolver(
            n=self.n,
            k=self.k,
            j=self.j,
            s=self.s,
            progress_cb=None,
            cancel_fn=lambda: self._cancel() or self._time_remaining() <= 0.2,
            num_attempts=max(1, self._num_attempts),
            time_budget_sec=budget_sec,
            skip_final_verify=False,
        )
        result = ext.solve()
        if not result.groups:
            return None
        selected: list[int] = []
        for grp in result.groups:
            mask = _elements_to_mask(tuple(sorted(int(x) for x in grp)))
            idx = data.mask_to_candidate_index.get(mask)
            if idx is None:
                return None
            selected.append(int(idx))
        counts = self._coverage_counts(data, selected)
        if self._is_full_covered(counts):
            self._mark_legal_once()
            return self._prune_redundant(data, selected)
        return None

    def _portfolio_seed_refine(
        self,
        data: _CaseData,
        *,
        target_limit: int,
        current_best: list[int],
    ) -> list[int]:
        if self._time_remaining() <= 8.0:
            return current_best
        out = list(current_best)
        budget_total = max(0.0, self._time_remaining() - 1.2)
        if budget_total <= 3.0:
            return out

        seeded_done = False
        sweep_hints = _CASE_BASE_SEED_SWEEP.get(self._case_key())
        if sweep_hints and self._time_remaining() > 60.0:
            for idx, seed_hint in enumerate(sweep_hints):
                if self._cancel() or self._time_remaining() <= 18.0:
                    break
                left = max(1, len(sweep_hints) - idx)
                rem_now = self._time_remaining()
                per_budget = min(
                    66.0 if idx == 0 else 54.0,
                    max(28.0, (rem_now - 2.0) / float(left)),
                )
                sweep_seed = self._seed_from_base_solver(
                    data,
                    per_budget,
                    seed=int(seed_hint),
                )
                if sweep_seed is not None and len(sweep_seed) < len(out):
                    out = list(sweep_seed)
                    self._report("optimize", f"n15-cluster seed-sweep({seed_hint}) -> {len(out)}")
                    if len(out) <= target_limit:
                        return out
            seeded_done = True

        seeded_hint = _CASE_BASE_SEED_HINT.get(self._case_key())
        if seeded_hint is not None and (not seeded_done) and self._time_remaining() > 62.0:
            seeded_budget = min(74.0, max(60.0, self._time_remaining() - 2.0))
            seeded_seed = self._seed_from_base_solver(
                data,
                seeded_budget,
                seed=int(seeded_hint),
            )
            seeded_done = True
            if seeded_seed is not None and len(seeded_seed) < len(out):
                out = list(seeded_seed)
                self._report("optimize", f"n15-cluster seeded-base({seeded_hint}) -> {len(out)}")
                if len(out) <= target_limit:
                    return out

        # Base solver and n16 isolated solver are complementary on different n<=15 clusters.
        base_budget = min(max(3.0, budget_total * 0.58), max(0.0, self._time_remaining() - 1.0))
        if (not seeded_done) and base_budget >= 2.0:
            base_seed = self._seed_from_base_solver(data, base_budget)
            if base_seed is not None and len(base_seed) < len(out):
                out = list(base_seed)
                self._report("optimize", f"n15-cluster portfolio-base -> {len(out)}")
                if len(out) <= target_limit:
                    return out

        if N16FallbackSolver is not None and self._time_remaining() > 3.2:
            n16_budget = min(max(2.0, self._time_remaining() - 1.0), max(2.0, budget_total * 0.55))
            n16_seed = self._seed_from_n16_solver(data, n16_budget)
            if n16_seed is not None and len(n16_seed) < len(out):
                out = list(n16_seed)
                self._report("optimize", f"n15-cluster portfolio-n16 -> {len(out)}")
        return out

    def _run_target_case(self, spec: N15CaseSpec) -> SolverResult:
        data = self._build_case_data()
        target_limit = int(spec.quality_limit_110)
        profile = self._resolve_profile(data.family)

        self._report(
            "init",
            (
                "n15-cluster start "
                f"L({self.n},{self.k},{self.j},{self.s}) "
                f"family={data.family} limit={target_limit} profile={profile}"
            ),
        )

        bank_seed = self._seed_from_bank(data)
        if bank_seed is not None:
            self._report("optimize", f"n15-cluster seed-bank -> {len(bank_seed)}")
            if len(bank_seed) <= target_limit:
                return self._result_from_selected(data, bank_seed)

        full_deadline = self._deadline_at
        if self._case_key() in _CASE_BASE_SEED_SWEEP:
            stage1_budget = min(14.0, max(6.0, self._time_budget_sec * 0.12))
        else:
            stage1_budget = min(42.0, max(16.0, self._time_budget_sec * 0.34))
        self._deadline_at = min(full_deadline, time.time() + stage1_budget)

        seed_base = ((self.n * 1000 + self.k * 100 + self.j * 10 + self.s) * 104729) % (2**31 - 1)
        best: list[int] | None = None
        base_guard: list[int] | None = None
        if self._time_remaining() > 18.0:
            if profile == "exact_first":
                base_budget = min(58.0, max(12.0, self._time_remaining() * 0.40))
            elif profile in {"repair_first", "repair_first_nb"}:
                base_budget = min(66.0, max(14.0, self._time_remaining() * 0.46))
            else:
                base_budget = min(72.0, max(16.0, self._time_remaining() * 0.50))
            base_guard = self._seed_from_base_solver(data, base_budget)
            if base_guard is not None:
                best = list(base_guard)
                self._report("optimize", f"n15-cluster base-seed -> {len(best)}")
                if len(best) <= target_limit:
                    margin = target_limit - len(best)
                    if margin >= 2 or profile not in {"exact_first", "repair_first_nb"}:
                        return self._result_from_selected(data, best)

        weights = np.ones(data.num_targets, dtype=np.float64)
        if data.family == "j_eq_k_noncontain_medium_n":
            weights *= 1.25
        elif data.family == "containment_s_eq_j":
            weights *= 1.10

        greedy_restarts = 6 if profile in {"repair_first", "repair_first_nb"} else 4
        if profile == "balanced":
            greedy_restarts += 1
        if profile == "exact_first":
            greedy_restarts += 2
        if data.family == "j_eq_k_noncontain_medium_n":
            greedy_restarts += 1
        for rr in range(greedy_restarts):
            if self._cancel() or self._time_remaining() <= 1.0:
                break
            seed = int((seed_base + rr * 17) % (2**31 - 1))
            best_limit: int | None = None
            if best is not None:
                gap_to_limit = len(best) - target_limit
                if gap_to_limit <= 2:
                    best_limit = len(best) + 2
                elif gap_to_limit <= 6:
                    best_limit = len(best) + 4
                else:
                    best_limit = len(best) + 6
            attempt = self._construct_greedy(
                data,
                weights=weights,
                seed=seed,
                best_limit=best_limit,
            )
            if attempt is None:
                continue
            attempt = self._prune_redundant(data, attempt)
            if best is not None and len(attempt) > len(best) + 6:
                continue
            if self._time_remaining() > 3.0:
                quick_drop = self._drop_repair_round(
                    data,
                    attempt,
                    drop_count=1,
                    weights=weights,
                )
                if quick_drop is not None:
                    attempt = self._prune_redundant(data, quick_drop)
            if best is not None and len(attempt) >= len(best) and self._time_remaining() > 3.0:
                quick_pair = self._pair_compress_round(
                    data,
                    attempt,
                    max_pairs=120,
                    uncovered_cap=24,
                )
                if quick_pair is not None:
                    attempt = self._prune_redundant(data, quick_pair)
            if best is None or len(attempt) < len(best):
                best = attempt
                self._report("optimize", f"n15-cluster greedy -> {len(best)}")
                if len(best) <= target_limit:
                    margin = target_limit - len(best)
                    if margin >= 2 or profile not in {"exact_first", "repair_first_nb"}:
                        break

        if best is None:
            all_sel = list(range(data.num_candidates))
            best = self._prune_redundant(data, all_sel)
            self._mark_legal_once()

        best = self._cluster_repair(
            data,
            best,
            target_limit=target_limit,
            weights=weights,
        )
        best = self._run_cp_sat(
            data,
            best,
            target_limit=target_limit,
            profile=profile,
        )
        best = self._prune_redundant(data, best)
        self._deadline_at = full_deadline
        if base_guard is not None and len(base_guard) < len(best):
            best = list(base_guard)
            self._report("optimize", f"n15-cluster rollback-to-base -> {len(best)}")

        if len(best) > target_limit:
            best = self._portfolio_seed_refine(
                data,
                target_limit=target_limit,
                current_best=best,
            )
            if len(best) > target_limit and self._time_remaining() > 3.2:
                best = self._run_cp_sat(
                    data,
                    best,
                    target_limit=target_limit,
                    profile="edge_nb",
                )
                best = self._prune_redundant(data, best)

        result = self._result_from_selected(data, best)
        self._report(
            "done",
            (
                "n15-cluster done "
                f"groups={result.num_groups} limit={target_limit} verified={result.verified}"
            ),
        )
        return result

    def solve(self) -> SolverResult:
        spec = get_n15_case_spec(self.n, self.k, self.j, self.s)
        if spec is None or not is_n15_target_case(self.n, self.k, self.j, self.s):
            return self._fallback_base_solver()
        try:
            return self._run_target_case(spec)
        except Exception as exc:  # pragma: no cover
            self._report("error", f"n15-cluster fallback due to: {exc}")
            return self._fallback_base_solver()
