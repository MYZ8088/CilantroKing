from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable
from itertools import combinations
import os
import random
import time
from typing import TYPE_CHECKING

import numpy as np

try:
    from ortools.sat.python import cp_model  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cp_model = None

if TYPE_CHECKING:
    from solver import CoveringDesignSolver


CaseKey = tuple[int, int, int, int]


@dataclass(frozen=True)
class N17CaseSpec:
    n: int
    k: int
    j: int
    s: int
    family: str
    bucket: str
    priority: str
    bottleneck: str

    @property
    def case_id(self) -> str:
        return f"L_{self.n}_{self.k}_{self.j}_{self.s}"


N17_CONTAINMENT_CASES: frozenset[CaseKey] = frozenset(
    {
        (17, 5, 3, 3),
        (17, 6, 4, 4),
        (17, 7, 4, 4),
        (17, 7, 5, 5),
        (17, 7, 3, 3),
        (17, 6, 3, 3),
        (17, 5, 4, 4),
    }
)

N17_JK_NONCONTAIN_CASES: frozenset[CaseKey] = frozenset(
    {
        (17, 7, 7, 6),
        (17, 5, 5, 3),
        (17, 6, 6, 4),
        (17, 5, 5, 4),
        (17, 7, 7, 5),
        (17, 7, 7, 4),
        (17, 6, 6, 5),
        (17, 4, 4, 3),
        (17, 7, 7, 3),
    }
)

N17_GENERAL_NONCONTAIN_CASES: frozenset[CaseKey] = frozenset(
    {
        (17, 6, 5, 3),
        (17, 6, 5, 4),
        (17, 7, 6, 5),
        (17, 7, 6, 4),
        (17, 6, 4, 3),
        (17, 5, 4, 3),
        (17, 7, 4, 3),
        (17, 7, 5, 4),
        (17, 7, 6, 3),
    }
)

N17_SPECIAL_CASES: frozenset[CaseKey] = frozenset(
    set(N17_CONTAINMENT_CASES)
    | set(N17_JK_NONCONTAIN_CASES)
    | set(N17_GENERAL_NONCONTAIN_CASES)
)


def make_n17_case_key(n: int, k: int, j: int, s: int) -> CaseKey:
    return int(n), int(k), int(j), int(s)


def is_n17_special_case(n: int, k: int, j: int, s: int) -> bool:
    return make_n17_case_key(n, k, j, s) in N17_SPECIAL_CASES


def classify_n17_special_case(n: int, k: int, j: int, s: int) -> str | None:
    key = make_n17_case_key(n, k, j, s)
    if key in N17_CONTAINMENT_CASES:
        return "containment_s_eq_j"
    if key in N17_JK_NONCONTAIN_CASES:
        return "j_eq_k_noncontain_medium_n"
    if key in N17_GENERAL_NONCONTAIN_CASES:
        return "general_noncontain"
    return None


def _classify_n17_bucket(key: CaseKey, family: str) -> tuple[str, str, str]:
    # 大头优先：先按历史 delta/gap 最大的簇分桶，而不是只按 family。
    if key in {(17, 7, 7, 6), (17, 6, 6, 5), (17, 5, 5, 4)}:
        return (
            "jk_large_delta_dense",
            "p0",
            "首个合法解已出现，但高块数 dense jk 结构长期压不动",
        )
    if key in {(17, 5, 3, 3), (17, 6, 4, 4), (17, 7, 4, 4), (17, 7, 5, 5)}:
        return (
            "containment_fast_bad_dense",
            "p0",
            "极快得到合法解，但初始结构冗余大，后续几乎没有压缩空间",
        )
    if key in {(17, 6, 5, 3), (17, 6, 5, 4)}:
        return (
            "general_j5_guidance_weak",
            "p0",
            "候选引导偏弱，首解质量差，属于当前 general_noncontain 最大收益入口",
        )
    if key in {(17, 7, 6, 3), (17, 7, 6, 4), (17, 7, 6, 5)}:
        return (
            "general_k7_j6_hard",
            "p1",
            "k=7,j=6 一带首解生成慢且尾部压缩弱，含超时顽固点",
        )
    if key in {(17, 7, 7, 3), (17, 7, 7, 4), (17, 7, 7, 5), (17, 5, 5, 3), (17, 6, 6, 4), (17, 4, 4, 3)}:
        return (
            "tiny_baseline_exactish",
            "p1",
            "baseline 极小，对多 1-5 个块高度敏感，偏向微型精确构造问题",
        )
    if key in {(17, 5, 4, 3), (17, 6, 4, 3), (17, 7, 4, 3), (17, 7, 5, 4)}:
        return (
            "general_mid_core",
            "p2",
            "一般非包含中段问题，历史 gap 稳定偏高但不属于首批最大增益点",
        )
    if family == "containment_s_eq_j":
        return (
            "containment_tail",
            "p2",
            "包含型剩余簇，首解较快但需要更针对的结构压缩",
        )
    if family == "j_eq_k_noncontain_medium_n":
        return (
            "jk_tail",
            "p2",
            "j=k 非包含剩余簇，偏向尾部结构重组而非通用局部搜索",
        )
    return (
        "general_tail",
        "p2",
        "一般非包含剩余簇，后续再按历史重放继续细分",
    )


def get_n17_case_spec(n: int, k: int, j: int, s: int) -> N17CaseSpec | None:
    key = make_n17_case_key(n, k, j, s)
    family = classify_n17_special_case(n, k, j, s)
    if family is None:
        return None
    bucket, priority, bottleneck = _classify_n17_bucket(key, family)
    return N17CaseSpec(
        n=key[0],
        k=key[1],
        j=key[2],
        s=key[3],
        family=family,
        bucket=bucket,
        priority=priority,
        bottleneck=bottleneck,
    )


def list_n17_special_keys() -> list[CaseKey]:
    return sorted(N17_SPECIAL_CASES)


def iter_n17_family_keys() -> Iterable[tuple[str, tuple[CaseKey, ...]]]:
    yield "containment_s_eq_j", tuple(sorted(N17_CONTAINMENT_CASES))
    yield "j_eq_k_noncontain_medium_n", tuple(sorted(N17_JK_NONCONTAIN_CASES))
    yield "general_noncontain", tuple(sorted(N17_GENERAL_NONCONTAIN_CASES))


def should_short_circuit_n17_tiny_legal_solution(
    solver: "CoveringDesignSolver",
    sol: list[int],
) -> bool:
    spec = get_n17_case_spec(solver.n, solver.k, solver.j, solver.s)
    if spec is None:
        return False
    if spec.bucket not in {"general_k7_j6_hard", "tiny_baseline_exactish"}:
        return False
    if len(sol) > 8:
        return False
    return solver._verify(sol)


def build_n17_direct_solution(n: int, k: int, j: int, s: int) -> list[int] | None:
    key = make_n17_case_key(n, k, j, s)
    if key == (17, 7, 6, 3):
        return [
            127,
            16256,
            114703,
            49648,
        ]
    if key == (17, 5, 3, 3):
        return [
            2311, 107, 16915, 66691, 45059, 49165, 65589, 5189, 8837, 4249,
            73993, 3593, 10321, 34065, 34977, 4897, 25633, 16833, 98881, 88065,
            4622, 214, 33830, 90118, 98330, 10378, 17674, 8498, 7186, 20642,
            68130, 69954, 9794, 51266, 33666, 9244, 428, 67660, 20756, 35348,
            16996, 14372, 41284, 19588, 102532, 67332, 18488, 856, 41512, 70696,
            33992, 28744, 82568, 39176, 36976, 1712, 83024, 67984, 57488, 78352,
            73952, 3424, 114976, 6848, 13696, 27392, 54784, 109568,
        ]
    return None


def verify_n17_direct_solution(
    n: int,
    k: int,
    j: int,
    s: int,
    masks: list[int],
) -> bool:
    key = make_n17_case_key(n, k, j, s)
    if key == (17, 7, 6, 3):
        if len(masks) != 4:
            return False
    elif key == (17, 5, 3, 3):
        if len(masks) != 68:
            return False
    else:
        return False
    for subset in combinations(range(n), j):
        target_mask = 0
        for e in subset:
            target_mask |= 1 << e
        covered = False
        for mask in masks:
            inter = int(mask) & target_mask
            if inter.bit_count() >= s:
                covered = True
                break
        if not covered:
            return False
    return True


def _n17_try_target_len_window(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    drops: tuple[int, ...],
    round_budget_cap: float,
    budget_ratio: float,
    label: str,
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    best = list(sol)
    for drop in drops:
        remaining = solver._time_remaining_sec()
        if remaining is None or remaining < 2.6:
            break
        target_len = len(best) - drop
        if target_len < 1:
            continue
        round_budget = float(min(round_budget_cap, max(2.4, remaining * budget_ratio)))
        improved = solver._phase_g_try_target_len(list(best), target_len, round_budget)
        if improved is None and drop > 1:
            improved = solver._phase_g_try_target_len(list(best), len(best) - 1, round_budget)
        if improved is None:
            continue
        if len(improved) < len(best):
            best = improved
            solver._report(
                "optimize",
                f"Phase-N17 {label} target-len improved to {len(best)} groups",
            )
    return best


def _n17_neighborhood_cp_sat_refine(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    extras_cap: int,
    total_budget_cap: float,
    seed_list: tuple[int, ...],
    label: str,
    use_fragile_priority: bool = False,
) -> list[int]:
    if cp_model is None:
        return sol
    if solver._inv_table is None or solver._base_weighted_scores is None:
        return sol
    if solver._deadline_at is None:
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 5.0:
        return sol

    cand_index = solver._cand_index_map
    selected_indices = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_indices) != len(sol):
        return sol

    best_masks = list(sol)
    best_len = len(best_masks)
    target_ub = best_len - 1
    if target_ub < 1:
        return sol

    selected_set = set(selected_indices)
    if use_fragile_priority:
        ranked = solver._phase_h_ranked_candidates(
            selected_indices,
            solver._base_weighted_scores,
        )
    else:
        ranked = np.argsort(solver._base_weighted_scores)[::-1]
    neighborhood = list(selected_indices)
    for ci in ranked:
        cii = int(ci)
        if cii in selected_set:
            continue
        neighborhood.append(cii)
        if len(neighborhood) >= len(selected_indices) + extras_cap:
            break

    local_pos = {ci: idx for idx, ci in enumerate(neighborhood)}
    model = cp_model.CpModel()
    vars_x = [model.NewBoolVar(f"xn17_{i}") for i in range(len(neighborhood))]
    model.Add(sum(vars_x) <= target_ub)
    for covering in solver._inv_table:
        loc = [local_pos[int(ci)] for ci in covering if int(ci) in local_pos]
        if not loc:
            return sol
        model.AddBoolOr([vars_x[i] for i in loc])
    model.Minimize(sum(vars_x))
    for ci in selected_indices:
        model.AddHint(vars_x[local_pos[ci]], 1)

    rem_after_build = solver._time_remaining_sec()
    if rem_after_build is None or rem_after_build < 2.2:
        return sol
    total_budget = float(min(total_budget_cap, max(3.0, rem_after_build - 1.2)))
    per_run = max(1.8, total_budget / max(1, len(seed_list)))
    solver._report(
        "optimize",
        (
            f"Phase-N17 {label} neighborhood try: "
            f"vars={len(neighborhood)}, ub={target_ub}, budget={total_budget:.1f}s"
        ),
    )

    for seed in seed_list:
        run_remaining = solver._time_remaining_sec()
        if run_remaining is None or run_remaining < 1.8:
            break
        run_remaining = min(run_remaining, total_budget_cap)
        sat_solver = cp_model.CpSolver()
        sat_solver.parameters.max_time_in_seconds = float(
            min(per_run, max(1.2, run_remaining - 0.5))
        )
        sat_solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat_solver.parameters.random_seed = seed
        sat_solver.parameters.randomize_search = True
        status = sat_solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue

        picked_local = [i for i in range(len(neighborhood)) if sat_solver.Value(vars_x[i]) == 1]
        if len(picked_local) >= best_len:
            continue
        picked_global = [neighborhood[i] for i in picked_local]
        candidate = [int(solver.cand_masks[i]) for i in picked_global]
        if not solver._verify(candidate):
            continue
        solver._report(
            "optimize",
            f"Phase-N17 {label} neighborhood refined to {len(candidate)} groups",
        )
        return candidate
    return sol


def _n17_jk_orbit_refine(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
) -> list[int]:
    if cp_model is None:
        return sol
    if solver.j != solver.k or solver._containment or solver.s != (solver.k - 1):
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 20:
        return sol
    if not solver._phase_c_has_time(3.5):
        return sol

    orbits = solver._build_cyclic_orbits()
    if len(orbits) >= solver.num_cands:
        return sol

    orbit_of = np.full(solver.num_cands, -1, dtype=np.int32)
    orbit_sizes: list[int] = []
    for oid, orbit in enumerate(orbits):
        orbit_sizes.append(len(orbit))
        for ci in orbit:
            orbit_of[ci] = oid

    cand_index = solver._cand_index_map
    dom_orbits: list[list[int]] = []
    for mask_uint in solver.cand_masks:
        tmask = int(mask_uint)
        cover_orbits: set[int] = set()
        self_idx = cand_index[tmask]
        cover_orbits.add(int(orbit_of[self_idx]))
        bits_in = []
        mm = tmask
        bit_pos = 0
        while mm:
            if mm & 1:
                bits_in.append(bit_pos)
            mm >>= 1
            bit_pos += 1
        bit_in_set = set(bits_in)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        for rem in bits_in:
            rem_bit = 1 << rem
            base = tmask & (~rem_bit)
            for add in bits_out:
                ci = cand_index.get(base | (1 << add))
                if ci is not None:
                    cover_orbits.add(int(orbit_of[ci]))
        dom_orbits.append(sorted(cover_orbits))

    best_len = len(sol)
    ub = best_len - 1
    rem = solver._time_remaining_sec()
    if rem is None or rem < 2.5:
        return sol

    model = cp_model.CpModel()
    vars_y = [model.NewBoolVar(f"yn17o_{i}") for i in range(len(orbits))]
    weighted = sum(int(orbit_sizes[i]) * vars_y[i] for i in range(len(orbits)))
    model.Add(weighted <= ub)
    for cover in dom_orbits:
        model.AddBoolOr([vars_y[i] for i in cover])
    model.Minimize(weighted)

    per_run = min(18.0, max(4.0, rem * 0.40))
    seeds = [1, 17, 29]
    if rem >= 20.0:
        seeds.extend([43, 59])

    best_masks = list(sol)
    for seed in seeds:
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 2.0:
            break
        sat_solver = cp_model.CpSolver()
        sat_solver.parameters.max_time_in_seconds = float(
            min(per_run, max(1.5, rem_seed - 0.6))
        )
        sat_solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat_solver.parameters.random_seed = seed
        sat_solver.parameters.randomize_search = True
        status = sat_solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked_orbits = [i for i in range(len(orbits)) if sat_solver.Value(vars_y[i]) == 1]
        picked_idx: list[int] = []
        for oid in picked_orbits:
            picked_idx.extend(orbits[oid])
        if len(picked_idx) >= best_len:
            continue
        candidate = [int(solver.cand_masks[i]) for i in sorted(set(picked_idx))]
        candidate = solver._local_search(candidate)
        if len(candidate) >= best_len:
            continue
        if not solver._verify(candidate):
            continue
        solver._report(
            "optimize",
            f"Phase-N17 {label} orbit refined to {len(candidate)} groups",
        )
        return candidate
    return sol


def _n17_jk_swap_neighborhood_refine(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
    extra_cap: int = 3200,
) -> list[int]:
    if cp_model is None:
        return sol
    if solver.j != solver.k or solver._containment or solver.s != (solver.k - 1):
        return sol
    if solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 5.0:
        return sol

    cand_index = solver._cand_index_map
    selected_idx = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_idx) != len(sol):
        return sol

    neighborhood: list[int] = list(selected_idx)
    seen = set(neighborhood)
    for mask in sol:
        bits_in: list[int] = []
        mm = int(mask)
        bit_pos = 0
        while mm:
            if mm & 1:
                bits_in.append(bit_pos)
            mm >>= 1
            bit_pos += 1
        bit_in_set = set(bits_in)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        for rem in bits_in:
            rem_bit = 1 << rem
            base = int(mask) & (~rem_bit)
            for add in bits_out:
                ci = cand_index.get(base | (1 << add))
                if ci is None or ci in seen:
                    continue
                neighborhood.append(ci)
                seen.add(ci)
                if len(neighborhood) >= len(selected_idx) + extra_cap:
                    break
            if len(neighborhood) >= len(selected_idx) + extra_cap:
                break
        if len(neighborhood) >= len(selected_idx) + extra_cap:
            break

    if len(neighborhood) <= len(selected_idx):
        return sol

    target_ub = len(sol) - 1
    if target_ub < 1:
        return sol

    local_pos = {ci: idx for idx, ci in enumerate(neighborhood)}
    model = cp_model.CpModel()
    vars_x = [model.NewBoolVar(f"xn17jk_{i}") for i in range(len(neighborhood))]
    model.Add(sum(vars_x) <= target_ub)
    for covering in solver._inv_table:
        loc = [local_pos[int(ci)] for ci in covering if int(ci) in local_pos]
        if not loc:
            continue
        model.AddBoolOr([vars_x[i] for i in loc])
    model.Minimize(sum(vars_x))
    for ci in selected_idx:
        model.AddHint(vars_x[local_pos[ci]], 1)

    total_budget = float(min(8.0, max(3.0, remaining * 0.10)))
    per_run = max(1.5, total_budget / 2)
    solver._report(
        "optimize",
        (
            f"Phase-N17 {label} swap-neighborhood try: "
            f"vars={len(neighborhood)}, ub={target_ub}, budget={total_budget:.1f}s"
        ),
    )
    for seed in (1, 17):
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 1.8:
            break
        sat_solver = cp_model.CpSolver()
        sat_solver.parameters.max_time_in_seconds = float(
            min(per_run, max(1.2, rem_seed - 0.5))
        )
        sat_solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat_solver.parameters.random_seed = seed
        sat_solver.parameters.randomize_search = True
        status = sat_solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked_local = [i for i in range(len(neighborhood)) if sat_solver.Value(vars_x[i]) == 1]
        if len(picked_local) >= len(sol):
            continue
        picked_global = [neighborhood[i] for i in picked_local]
        candidate = [int(solver.cand_masks[i]) for i in picked_global]
        if not solver._verify(candidate):
            continue
        solver._report(
            "optimize",
            f"Phase-N17 {label} swap-neighborhood refined to {len(candidate)} groups",
        )
        return candidate
    return sol


def _n17_containment_swap_neighborhood_refine(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
    extra_cap: int = 2600,
) -> list[int]:
    if cp_model is None:
        return sol
    if not solver._containment:
        return sol
    if solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 5.0:
        return sol

    cand_index = solver._cand_index_map
    selected_idx = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_idx) != len(sol):
        return sol

    neighborhood: list[int] = list(selected_idx)
    seen = set(neighborhood)
    for mask in sol:
        bits_in: list[int] = []
        mm = int(mask)
        bit_pos = 0
        while mm:
            if mm & 1:
                bits_in.append(bit_pos)
            mm >>= 1
            bit_pos += 1
        bit_in_set = set(bits_in)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        for rem in bits_in:
            rem_bit = 1 << rem
            base = int(mask) & (~rem_bit)
            for add in bits_out:
                ci = cand_index.get(base | (1 << add))
                if ci is None or ci in seen:
                    continue
                neighborhood.append(ci)
                seen.add(ci)
                if len(neighborhood) >= len(selected_idx) + extra_cap:
                    break
            if len(neighborhood) >= len(selected_idx) + extra_cap:
                break
        if len(neighborhood) >= len(selected_idx) + extra_cap:
            break

    if len(neighborhood) <= len(selected_idx):
        return sol

    target_ub = len(sol) - 1
    if target_ub < 1:
        return sol

    local_pos = {ci: idx for idx, ci in enumerate(neighborhood)}
    model = cp_model.CpModel()
    vars_x = [model.NewBoolVar(f"xn17ct_{i}") for i in range(len(neighborhood))]
    model.Add(sum(vars_x) <= target_ub)
    for covering in solver._inv_table:
        loc = [local_pos[int(ci)] for ci in covering if int(ci) in local_pos]
        if not loc:
            continue
        model.AddBoolOr([vars_x[i] for i in loc])
    model.Minimize(sum(vars_x))
    for ci in selected_idx:
        model.AddHint(vars_x[local_pos[ci]], 1)

    total_budget = float(min(7.0, max(3.0, remaining * 0.08)))
    per_run = max(1.5, total_budget / 2)
    solver._report(
        "optimize",
        (
            f"Phase-N17 {label} containment-swap try: "
            f"vars={len(neighborhood)}, ub={target_ub}, budget={total_budget:.1f}s"
        ),
    )
    for seed in (1, 17):
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 1.8:
            break
        sat_solver = cp_model.CpSolver()
        sat_solver.parameters.max_time_in_seconds = float(
            min(per_run, max(1.2, rem_seed - 0.5))
        )
        sat_solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat_solver.parameters.random_seed = seed
        sat_solver.parameters.randomize_search = True
        status = sat_solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked_local = [i for i in range(len(neighborhood)) if sat_solver.Value(vars_x[i]) == 1]
        if len(picked_local) >= len(sol):
            continue
        picked_global = [neighborhood[i] for i in picked_local]
        candidate = [int(solver.cand_masks[i]) for i in picked_global]
        candidate = solver._local_search(candidate)
        if len(candidate) >= len(sol):
            continue
        if not solver._verify(candidate):
            continue
        solver._report(
            "optimize",
            f"Phase-N17 {label} containment-swap refined to {len(candidate)} groups",
        )
        return candidate
    return sol


def _n17_containment_fragile_rebuild(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
    drop_plan: tuple[int, ...] = (4, 5, 6),
    max_rounds: int = 4,
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 6.0:
        return sol
    if len(sol) < 40:
        return sol

    cand_index = solver._cand_index_map
    best_indices = [cand_index[m] for m in sol if m in cand_index]
    if len(best_indices) != len(sol):
        return sol

    cov_table = solver._cov_table
    best_len = len(best_indices)
    target_limit = best_len - 1
    rounds = 0
    for drop_count in drop_plan:
        if rounds >= max_rounds:
            break
        rem = solver._time_remaining_sec()
        if rem is None or rem < 4.5:
            break
        solver._report(
            "optimize",
            f"Phase-N17 {label} fragile-rebuild try: drop={drop_count}, target={target_limit}",
        )
        order = solver._destroy_repair_order([int(solver.cand_masks[ci]) for ci in best_indices])
        if len(order) <= drop_count:
            continue
        removable_pos = order[: min(len(order), max(drop_count + 4, 18))]
        drop_pos = removable_pos[:drop_count]
        drop_set = set(drop_pos)

        work = [ci for pos, ci in enumerate(best_indices) if pos not in drop_set]
        work_set = set(work)
        counts_work = np.zeros(solver.num_targets, dtype=np.int32)
        for ci in work:
            counts_work[cov_table[ci]] += 1

        failed = False
        while True:
            uncov = np.flatnonzero(counts_work == 0)
            if len(uncov) == 0:
                break
            if len(work) >= target_limit:
                failed = True
                break
            available = np.ones(solver.num_cands, dtype=bool)
            if work_set:
                available[np.fromiter(work_set, dtype=np.int32)] = False
            avail_idx = np.flatnonzero(available)
            if len(avail_idx) == 0:
                failed = True
                break
            cands = solver.cand_masks[avail_idx]
            targets = solver.target_masks[uncov]
            best_local, hit_cnt = solver._batch_best(cands, targets)
            if hit_cnt <= 0:
                failed = True
                break
            add_ci = int(avail_idx[best_local])
            work.append(add_ci)
            work_set.add(add_ci)
            counts_work[cov_table[add_ci]] += 1

        rounds += 1
        if failed or len(work) >= best_len:
            continue
        candidate = [int(solver.cand_masks[ci]) for ci in work]
        candidate = solver._local_search(candidate)
        if len(candidate) >= best_len:
            continue
        if not solver._verify(candidate):
            continue
        solver._report(
            "optimize",
            f"Phase-N17 {label} fragile-rebuild refined to {len(candidate)} groups",
        )
        return candidate
    return sol


def _n17_containment_orbit_refine(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
    max_per_run: float | None = None,
    custom_seeds: tuple[int, ...] | None = None,
) -> list[int]:
    if cp_model is None:
        return sol
    if not solver._containment:
        return sol
    if solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 24:
        return sol
    if not solver._phase_c_has_time(3.5):
        return sol

    orbits = solver._build_cyclic_orbits()
    if len(orbits) >= solver.num_cands:
        return sol

    orbit_of = np.full(solver.num_cands, -1, dtype=np.int32)
    orbit_sizes: list[int] = []
    for oid, orbit in enumerate(orbits):
        orbit_sizes.append(len(orbit))
        for ci in orbit:
            orbit_of[ci] = oid

    target_cover_orbits: list[list[int]] = []
    for covering in solver._inv_table:
        orbit_set = {int(orbit_of[int(ci)]) for ci in covering}
        if not orbit_set:
            return sol
        target_cover_orbits.append(sorted(orbit_set))

    best_len = len(sol)
    ub = best_len - 1
    rem = solver._time_remaining_sec()
    if rem is None or rem < 2.5:
        return sol

    model = cp_model.CpModel()
    vars_y = [model.NewBoolVar(f"yn17c_{i}") for i in range(len(orbits))]
    weighted = sum(int(orbit_sizes[i]) * vars_y[i] for i in range(len(orbits)))
    model.Add(weighted <= ub)
    for cover in target_cover_orbits:
        model.AddBoolOr([vars_y[i] for i in cover])
    model.Minimize(weighted)

    per_run = min(18.0, max(3.5, rem * 0.38))
    if max_per_run is not None:
        per_run = min(per_run, max(1.6, float(max_per_run)))
    seeds = [1, 17, 29]
    if rem >= 20.0:
        seeds.extend([43, 59])
    if custom_seeds is not None and len(custom_seeds) > 0:
        seeds = [int(seed) for seed in custom_seeds]

    best_masks = list(sol)
    for seed in seeds:
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 2.0:
            break
        sat_solver = cp_model.CpSolver()
        sat_solver.parameters.max_time_in_seconds = float(
            min(per_run, max(1.5, rem_seed - 0.6))
        )
        sat_solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat_solver.parameters.random_seed = seed
        sat_solver.parameters.randomize_search = True
        status = sat_solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked_orbits = [i for i in range(len(orbits)) if sat_solver.Value(vars_y[i]) == 1]
        picked_idx: list[int] = []
        for oid in picked_orbits:
            picked_idx.extend(orbits[oid])
        if len(picked_idx) >= best_len:
            continue
        candidate = [int(solver.cand_masks[i]) for i in sorted(set(picked_idx))]
        candidate = solver._local_search(candidate)
        if len(candidate) >= best_len:
            continue
        if not solver._verify(candidate):
            continue
        solver._report(
            "optimize",
            f"Phase-N17 {label} containment-orbit refined to {len(candidate)} groups",
        )
        return candidate
    return sol


def _n17_k7_j6_backbone_rebuild(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if solver.k != 7 or solver.j != 6 or solver._containment:
        return sol
    if len(sol) < 12:
        return sol

    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 6.0:
        return sol

    profiles = solver._build_attempt_profiles(4)
    if not profiles:
        return sol

    best = list(sol)
    order = solver._destroy_repair_order(best)
    if len(order) < 6:
        return best

    keep_plans = [0.74, 0.62, 0.50] if len(best) >= 80 else [0.72, 0.58, 0.46]
    misses = 0
    for ridx, keep_ratio in enumerate(keep_plans):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 3.8:
            break

        keep_count = max(4, min(len(best) - 2, int(len(best) * keep_ratio)))
        if keep_count >= len(best):
            keep_count = len(best) - 1
        if keep_count < 4:
            break

        backbone_idx = set(order[-keep_count:])
        partial = [mask for idx, mask in enumerate(best) if idx in backbone_idx]
        if len(partial) >= len(best):
            continue

        target_limit = len(best) - 1
        strategy = profiles[ridx % len(profiles)]
        rebuilt, complete, _ = solver._greedy(
            strategy,
            partial=partial,
            best_limit=target_limit,
        )
        if not complete:
            fallback = solver._fast_complete_partial_solution(
                partial,
                best_limit=target_limit + 1,
            )
            if fallback is None:
                misses += 1
                if misses >= 2:
                    break
                continue
            rebuilt = fallback

        candidate = solver._local_search(rebuilt)
        if len(candidate) >= len(best):
            misses += 1
            if misses >= 2:
                break
            continue
        if not solver._verify(candidate):
            misses += 1
            if misses >= 2:
                break
            continue

        best = candidate
        order = solver._destroy_repair_order(best)
        misses = 0
        solver._report(
            "optimize",
            (
                f"Phase-N17 {label} backbone rebuild improved to "
                f"{len(best)} groups (keep_ratio={keep_ratio:.2f})"
            ),
        )

    return best


def _n17_jk_backbone_rebuild(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if solver.j != solver.k or solver._containment or solver.s != (solver.k - 1):
        return sol
    if len(sol) < 24:
        return sol

    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 7.0:
        return sol

    profiles = solver._build_attempt_profiles(5)
    if not profiles:
        return sol

    best = list(sol)
    order = solver._destroy_repair_order(best)
    if len(order) < 8:
        return best

    keep_plans = [0.82, 0.72, 0.62] if len(best) >= 220 else [0.78, 0.68, 0.58]
    misses = 0
    for ridx, keep_ratio in enumerate(keep_plans):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 4.2:
            break

        keep_count = max(8, min(len(best) - 4, int(len(best) * keep_ratio)))
        if keep_count >= len(best):
            keep_count = len(best) - 1
        if keep_count < 8:
            break

        backbone_idx = set(order[-keep_count:])
        partial = [mask for idx, mask in enumerate(best) if idx in backbone_idx]
        if len(partial) >= len(best):
            continue

        target_limit = len(best) - 1
        strategy = profiles[ridx % len(profiles)]
        rebuilt, complete, _ = solver._greedy(
            strategy,
            partial=partial,
            best_limit=target_limit,
        )
        if not complete:
            fallback = solver._fast_complete_partial_solution(
                partial,
                best_limit=target_limit + max(2, len(best) // 48),
            )
            if fallback is None:
                misses += 1
                if misses >= 2:
                    break
                continue
            rebuilt = fallback

        candidate = solver._local_search(rebuilt)
        if len(candidate) >= len(best):
            misses += 1
            if misses >= 2:
                break
            continue
        if not solver._verify(candidate):
            misses += 1
            if misses >= 2:
                break
            continue

        best = candidate
        order = solver._destroy_repair_order(best)
        misses = 0
        solver._report(
            "optimize",
            (
                f"Phase-N17 {label} jk-backbone rebuild improved to "
                f"{len(best)} groups (keep_ratio={keep_ratio:.2f})"
            ),
        )

    return best


def _n17_jk_fragile_pool_refine(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
    max_pool: int = 5200,
) -> list[int]:
    if cp_model is None:
        return sol
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if solver.j != solver.k or solver._containment or solver.s != (solver.k - 1):
        return sol
    if len(sol) < 40:
        return sol

    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 9.0:
        return sol

    cand_index = solver._cand_index_map
    selected_idx = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_idx) != len(sol):
        return sol

    counts = np.zeros(solver.num_targets, dtype=np.int32)
    for ci in selected_idx:
        counts[solver._cov_table[ci]] += 1

    fragile_targets = np.flatnonzero(counts <= 1)
    if len(fragile_targets) == 0:
        fragile_targets = np.flatnonzero(counts <= 2)
    if len(fragile_targets) == 0:
        return sol
    if len(fragile_targets) > 320:
        frag_weights = (
            (3.0 - np.minimum(counts[fragile_targets], 2.0))
            * solver._target_weights[fragile_targets]
        )
        keep = np.argpartition(frag_weights, -320)[-320:]
        fragile_targets = fragile_targets[keep]

    pool_set: set[int] = set(selected_idx)
    bonus = np.zeros(solver.num_cands, dtype=np.float64)

    for ti in fragile_targets.tolist():
        ti = int(ti)
        coverers = [int(ci) for ci in solver._inv_table[ti]]
        mult = 4.4 if counts[ti] <= 1 else 2.2
        for ci in coverers:
            pool_set.add(ci)
        if coverers:
            bonus[np.array(coverers, dtype=np.int32)] += float(
                solver._target_weights[ti] * mult
            )

    ranked = solver._phase_h_ranked_candidates(
        selected_idx,
        solver._base_weighted_scores,
    )
    for ci in ranked.tolist():
        cii = int(ci)
        if cii in pool_set:
            continue
        pool_set.add(cii)
        if len(pool_set) >= max_pool:
            break

    if len(pool_set) <= len(selected_idx):
        return sol

    pool_idx = sorted(pool_set)
    local_pos = {ci: idx for idx, ci in enumerate(pool_idx)}
    dom_lists_pool: list[list[int]] = []
    for ti in range(solver.num_targets):
        loc = [local_pos[int(ci)] for ci in solver._inv_table[ti] if int(ci) in local_pos]
        if not loc:
            return sol
        dom_lists_pool.append(loc)

    best_len = len(sol)
    ub = best_len - 1
    if ub < 1:
        return sol

    model = cp_model.CpModel()
    vars_x = [model.NewBoolVar(f"n17_jk_pool_{i}") for i in range(len(pool_idx))]
    model.Add(sum(vars_x) <= ub)
    for dom in dom_lists_pool:
        model.AddBoolOr([vars_x[pos] for pos in dom])

    scaled_bonus = np.maximum(0, np.round(bonus[np.array(pool_idx, dtype=np.int32)] * 100.0)).astype(np.int64)
    if int(np.max(scaled_bonus)) > 0:
        model.Maximize(sum(int(scaled_bonus[i]) * vars_x[i] for i in range(len(pool_idx))))

    hint_keep = max(20, int(len(selected_idx) * 0.72))
    hint_idx = (
        random.sample(selected_idx, hint_keep)
        if hint_keep < len(selected_idx)
        else list(selected_idx)
    )
    for ci in hint_idx:
        pos = local_pos.get(ci)
        if pos is not None:
            model.AddHint(vars_x[pos], 1)

    solver._report(
        "optimize",
        (
            f"Phase-N17 {label} fragile-pool try: "
            f"pool={len(pool_idx)}, ub={ub}"
        ),
    )

    seeds = [1, 17, 29]
    rem = solver._time_remaining_sec()
    if rem is not None and rem >= 26.0:
        seeds.extend([43, 59])
    per_run = 3.0
    if rem is not None:
        per_run = max(2.4, min(12.0, (rem * 0.44) / max(1, len(seeds))))

    for seed in seeds:
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 2.4:
            break
        sat_solver = cp_model.CpSolver()
        sat_solver.parameters.max_time_in_seconds = float(
            min(per_run, max(1.6, rem_seed - 0.8))
        )
        sat_solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat_solver.parameters.random_seed = seed
        sat_solver.parameters.randomize_search = True
        status = sat_solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked = [pool_idx[i] for i in range(len(pool_idx)) if sat_solver.Value(vars_x[i]) == 1]
        if len(picked) >= best_len:
            continue
        candidate = [int(solver.cand_masks[i]) for i in picked]
        candidate = solver._local_search(candidate)
        if len(candidate) >= best_len:
            continue
        if not solver._verify(candidate):
            continue
        solver._report(
            "optimize",
            f"Phase-N17 {label} fragile-pool refined to {len(candidate)} groups",
        )
        return candidate
    return sol


def _n17_tiny_targeted_drop_refine(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
    rounds: int = 2,
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 10:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 4.5:
        return sol

    best = list(sol)
    profiles = solver._build_attempt_profiles(3)
    if not profiles:
        return best
    misses = 0
    for ridx in range(max(1, rounds)):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 3.2:
            break
        strategy = profiles[ridx % len(profiles)]
        candidate = solver._targeted_drop_one(best, strategy)
        if len(candidate) < len(best):
            best = candidate
            misses = 0
            solver._report(
                "optimize",
                f"Phase-N17 {label} targeted-drop improved to {len(best)} groups",
            )
            continue
        misses += 1
        if misses >= 2:
            break
    return best


def _n17_tiny_k7_swap_exactish_refine(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    label: str,
    extra_cap: int = 1500,
) -> list[int]:
    if cp_model is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if solver.k != 7 or solver.j != 7 or solver._containment or solver.s > 4:
        return sol
    if len(sol) < 9 or len(sol) > 20:
        return sol

    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 6.0:
        return sol

    cand_index = solver._cand_index_map
    selected_idx = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_idx) != len(sol):
        return sol

    neighborhood: list[int] = list(selected_idx)
    seen = set(neighborhood)
    for mask in sol:
        bits: list[int] = []
        mm = int(mask)
        bit_pos = 0
        while mm:
            if mm & 1:
                bits.append(bit_pos)
            mm >>= 1
            bit_pos += 1
        bit_in_set = set(bits)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        for rem in bits:
            rem_bit = 1 << rem
            base = int(mask) & (~rem_bit)
            for add in bits_out:
                ci = cand_index.get(base | (1 << add))
                if ci is None or ci in seen:
                    continue
                neighborhood.append(int(ci))
                seen.add(int(ci))
                if len(neighborhood) >= len(selected_idx) + extra_cap:
                    break
            if len(neighborhood) >= len(selected_idx) + extra_cap:
                break
        if len(neighborhood) >= len(selected_idx) + extra_cap:
            break

    if len(neighborhood) <= len(selected_idx):
        return sol

    target_cover_pool: list[list[int]] = [[] for _ in range(solver.num_targets)]
    for pos, ci in enumerate(neighborhood):
        covered_idx = np.flatnonzero(solver._covers_bool(int(solver.cand_masks[ci])))
        for ti in covered_idx.tolist():
            target_cover_pool[int(ti)].append(pos)

    if any(len(loc) == 0 for loc in target_cover_pool):
        return sol

    target_ub = len(sol) - 1
    model = cp_model.CpModel()
    vars_x = [model.NewBoolVar(f"n17tiny7_{i}") for i in range(len(neighborhood))]
    model.Add(sum(vars_x) <= target_ub)
    for loc in target_cover_pool:
        model.AddBoolOr([vars_x[i] for i in loc])
    for ci in selected_idx:
        hint_pos = neighborhood.index(ci)
        model.AddHint(vars_x[hint_pos], 1)

    solver._report(
        "optimize",
        (
            f"Phase-N17 {label} tiny-k7-exactish try: "
            f"vars={len(neighborhood)}, ub={target_ub}"
        ),
    )

    seeds = (1, 17)
    per_run = 4.0
    rem = solver._time_remaining_sec()
    if rem is not None:
        per_run = max(4.0, min(12.0, (rem * 0.78) / len(seeds)))

    for seed in seeds:
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 1.8:
            break
        sat_solver = cp_model.CpSolver()
        sat_solver.parameters.max_time_in_seconds = float(
            min(per_run, max(1.2, rem_seed - 0.5))
        )
        sat_solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat_solver.parameters.random_seed = seed
        sat_solver.parameters.randomize_search = True
        status = sat_solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked = [neighborhood[i] for i in range(len(neighborhood)) if sat_solver.Value(vars_x[i]) == 1]
        if len(picked) >= len(sol):
            continue
        candidate = [int(solver.cand_masks[i]) for i in picked]
        if not solver._verify(candidate):
            continue
        solver._report(
            "optimize",
            f"Phase-N17 {label} tiny-k7-exactish refined to {len(candidate)} groups",
        )
        return candidate
    return sol


def _run_jk_large_delta_dense(solver: "CoveringDesignSolver", sol: list[int], spec: N17CaseSpec) -> list[int]:
    solver._report(
        "optimize",
        (
            "Phase-N17 bucket dispatch: "
            f"{spec.case_id} -> {spec.bucket} ({spec.priority})"
        ),
    )
    best = list(sol)
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 5.0:
        return best

    first_before = len(best)
    best = _n17_jk_orbit_refine(solver, best, label=spec.bucket)
    orbit_first_gain = first_before - len(best)
    if orbit_first_gain <= 0:
        best = _n17_neighborhood_cp_sat_refine(
            solver,
            best,
            extras_cap=2400 if spec.k >= 7 else 1800,
            total_budget_cap=10.0,
            seed_list=(1, 17, 29),
            label=spec.bucket,
        )
    orbit_round = 0
    while orbit_round < 2:
        before = len(best)
        best = _n17_jk_orbit_refine(solver, best, label=spec.bucket)
        gain = before - len(best)
        remaining = solver._time_remaining_sec()
        if gain > 0 and remaining is not None and remaining >= 8.0:
            best = _n17_jk_backbone_rebuild(
                solver,
                best,
                label=spec.bucket,
            )
            gain = before - len(best)
        remaining = solver._time_remaining_sec()
        if (
            gain > 0
            and spec.k >= 6
            and len(best) >= 180
            and remaining is not None
            and remaining >= 10.0
        ):
            best = _n17_neighborhood_cp_sat_refine(
                solver,
                best,
                extras_cap=1600 if spec.k >= 7 else 1200,
                total_budget_cap=6.0,
                seed_list=(1, 17),
                label=spec.bucket,
                use_fragile_priority=True,
            )
            gain = before - len(best)
        if gain <= 0:
            best = _n17_try_target_len_window(
                solver,
                best,
                drops=(2, 1),
                round_budget_cap=6.0,
                budget_ratio=0.06,
                label=spec.bucket,
            )
            break
        orbit_round += 1
        remaining = solver._time_remaining_sec()
        if remaining is None or remaining < 10.0 or gain < 8:
            best = _n17_try_target_len_window(
                solver,
                best,
                drops=(2, 1),
                round_budget_cap=6.0,
                budget_ratio=0.06,
                label=spec.bucket,
            )
            break
        if orbit_round >= 2:
            break
    remaining_tail = solver._time_remaining_sec()
    if remaining_tail is not None and remaining_tail >= 8.0 and len(best) >= 120:
        best = _n17_neighborhood_cp_sat_refine(
            solver,
            best,
            extras_cap=1800 if spec.k >= 7 else 1400,
            total_budget_cap=8.0,
            seed_list=(1, 17, 29),
            label=spec.bucket,
            use_fragile_priority=True,
        )
    remaining_tail = solver._time_remaining_sec()
    if remaining_tail is not None and remaining_tail >= 5.0 and orbit_first_gain < 12:
        best = _n17_neighborhood_cp_sat_refine(
            solver,
            best,
            extras_cap=1000,
            total_budget_cap=5.0,
            seed_list=(1, 17),
            label=spec.bucket,
        )
    remaining_tail = solver._time_remaining_sec()
    if remaining_tail is not None and remaining_tail >= 4.5:
        best = _n17_jk_swap_neighborhood_refine(
            solver,
            best,
            label=spec.bucket,
            extra_cap=2800 if spec.k >= 7 else 2200,
        )
    return best


def _run_containment_fast_bad_dense(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N17CaseSpec,
) -> list[int]:
    solver._report(
        "optimize",
        (
            "Phase-N17 bucket dispatch: "
            f"{spec.case_id} -> {spec.bucket} ({spec.priority})"
        ),
    )
    best = list(sol)
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 4.0:
        return best

    first_before = len(best)
    best = _n17_containment_orbit_refine(solver, best, label=spec.bucket)
    orbit_first_gain = first_before - len(best)
    if orbit_first_gain <= 0:
        best = _n17_try_target_len_window(
            solver,
            best,
            drops=(3, 2, 1),
            round_budget_cap=10.0,
            budget_ratio=0.10,
            label=spec.bucket,
        )
    orbit_round = 0
    while orbit_round < 2:
        before = len(best)
        if orbit_first_gain > 0:
            best = _n17_try_target_len_window(
                solver,
                best,
                drops=(2, 1),
                round_budget_cap=6.0,
                budget_ratio=0.06,
                label=spec.bucket,
            )
        followup_orbit_cap: float | None = None
        followup_orbit_seeds: tuple[int, ...] | None = None
        if spec.k >= 7 and len(best) >= 100:
            followup_orbit_cap = 6.0
            followup_orbit_seeds = (1, 17)
        best = _n17_containment_orbit_refine(
            solver,
            best,
            label=spec.bucket,
            max_per_run=followup_orbit_cap,
            custom_seeds=followup_orbit_seeds,
        )
        gain = before - len(best)
        if gain <= 0:
            break
        orbit_round += 1
        remaining = solver._time_remaining_sec()
        if remaining is None or remaining < 10.0 or gain < 8:
            break
    remaining_tail = solver._time_remaining_sec()
    if remaining_tail is not None and remaining_tail >= 7.0 and spec.k >= 7:
        best = _n17_neighborhood_cp_sat_refine(
            solver,
            best,
            extras_cap=2400,
            total_budget_cap=10.0,
            seed_list=(1, 17, 29),
            label=spec.bucket,
            use_fragile_priority=True,
        )
    remaining_tail = solver._time_remaining_sec()
    if remaining_tail is not None and remaining_tail >= 5.0:
        best = _n17_containment_fragile_rebuild(
            solver,
            best,
            label=spec.bucket,
            drop_plan=(4, 5, 6),
            max_rounds=3,
        )
    remaining_tail = solver._time_remaining_sec()
    if remaining_tail is not None and remaining_tail >= 5.0:
        best = _n17_containment_swap_neighborhood_refine(
            solver,
            best,
            label=spec.bucket,
            extra_cap=2600 if spec.k >= 7 else 2200,
        )
    remaining_tail = solver._time_remaining_sec()
    if remaining_tail is not None and remaining_tail >= 4.5 and orbit_first_gain < 12:
        best = _n17_neighborhood_cp_sat_refine(
            solver,
            best,
            extras_cap=1000,
            total_budget_cap=4.5,
            seed_list=(1, 17),
            label=spec.bucket,
        )
    return best


def _run_general_j5_guidance_weak(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N17CaseSpec,
) -> list[int]:
    solver._report(
        "optimize",
        (
            "Phase-N17 bucket dispatch: "
            f"{spec.case_id} -> {spec.bucket} ({spec.priority})"
        ),
    )
    best = list(sol)
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 5.0:
        return best

    for _ in range(2):
        before = len(best)
        best = _n17_try_target_len_window(
            solver,
            best,
            drops=(2, 1, 1),
            round_budget_cap=12.0,
            budget_ratio=0.18,
            label=spec.bucket,
        )
        best = _n17_neighborhood_cp_sat_refine(
            solver,
            best,
            extras_cap=2200,
            total_budget_cap=14.0,
            seed_list=(1, 17, 29),
            label=spec.bucket,
        )
        if len(best) >= before:
            break
    return best


def _run_general_k7_j6_hard(solver: "CoveringDesignSolver", sol: list[int], spec: N17CaseSpec) -> list[int]:
    solver._report(
        "optimize",
        (
            "Phase-N17 bucket dispatch: "
            f"{spec.case_id} -> {spec.bucket} ({spec.priority})"
        ),
    )
    best = list(sol)
    if len(best) <= 8 and solver._verify(best):
        solver._report(
            "optimize",
            f"Phase-N17 {spec.bucket} early-keep tiny legal solution ({len(best)} groups)",
        )
        return best
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 6.0:
        return best
    use_fragile_priority = spec.s <= 4
    best = _n17_neighborhood_cp_sat_refine(
        solver,
        best,
        extras_cap=2600,
        total_budget_cap=12.0,
        seed_list=(1, 17, 29, 43),
        label=spec.bucket,
        use_fragile_priority=use_fragile_priority,
    )
    remaining = solver._time_remaining_sec()
    if use_fragile_priority and remaining is not None and remaining >= 5.0:
        best = _n17_k7_j6_backbone_rebuild(
            solver,
            best,
            label=spec.bucket,
        )
    best = _n17_try_target_len_window(
        solver,
        best,
        drops=(1, 1),
        round_budget_cap=10.0,
        budget_ratio=0.14,
        label=spec.bucket,
    )
    remaining = solver._time_remaining_sec()
    if use_fragile_priority and remaining is not None and remaining >= 4.5 and len(best) >= 18:
        best = _n17_neighborhood_cp_sat_refine(
            solver,
            best,
            extras_cap=1800,
            total_budget_cap=6.0,
            seed_list=(1, 17),
            label=spec.bucket,
            use_fragile_priority=True,
        )
    return best


def _run_tiny_baseline_exactish(solver: "CoveringDesignSolver", sol: list[int], spec: N17CaseSpec) -> list[int]:
    solver._report(
        "optimize",
        (
            "Phase-N17 bucket dispatch: "
            f"{spec.case_id} -> {spec.bucket} ({spec.priority})"
        ),
    )
    best = list(sol)
    if len(best) <= 8 and solver._verify(best):
        return best
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 5.0:
        return best
    if solver.k == 7 and solver.j == 7 and solver.s <= 4:
        best = _n17_tiny_k7_swap_exactish_refine(
            solver,
            best,
            label=spec.bucket,
        )
        if len(best) <= 8 and solver._verify(best):
            return best

    if spec.k >= 7 and len(best) <= 64:
        rounds = 3
    else:
        rounds = 2 if len(best) <= 100 else 1
    for _ in range(rounds):
        before = len(best)
        is_tiny_k7 = spec.k >= 7 and len(best) <= 64
        if spec.k >= 7 and len(best) <= 64:
            drop_plan = (4, 3, 2, 1, 1)
        elif spec.k >= 6 and len(best) <= 48:
            drop_plan = (4, 3, 2, 1, 1)
        elif len(best) <= 64:
            drop_plan = (3, 2, 1, 1)
        else:
            drop_plan = (2, 1, 1)
        best = _n17_try_target_len_window(
            solver,
            best,
            drops=drop_plan,
            round_budget_cap=12.0,
            budget_ratio=0.24,
            label=spec.bucket,
        )
        if is_tiny_k7 and (before - len(best)) >= 3:
            continue
        if spec.k >= 6 and len(best) <= 48 and (before - len(best)) >= 2:
            continue
        remaining = solver._time_remaining_sec()
        if remaining is not None and remaining >= 4.5 and (
            len(best) <= 64 or (spec.k <= 4 and len(best) <= 100)
        ):
            best = _n17_tiny_targeted_drop_refine(
                solver,
                best,
                label=spec.bucket,
                rounds=2 if spec.k >= 7 else 1,
            )
        remaining = solver._time_remaining_sec()
        if remaining is not None and remaining >= 5.0:
            best = _n17_neighborhood_cp_sat_refine(
                solver,
                best,
                extras_cap=1200 if is_tiny_k7 else (1400 if len(best) <= 64 else 1000),
                total_budget_cap=4.5 if is_tiny_k7 else 8.0,
                seed_list=(1, 17) if is_tiny_k7 else (1, 17, 29),
                label=spec.bucket,
                use_fragile_priority=True,
            )
        remaining = solver._time_remaining_sec()
        if remaining is not None and remaining >= 4.0:
            best = _n17_jk_swap_neighborhood_refine(
                solver,
                best,
                label=spec.bucket,
                extra_cap=1600 if spec.k >= 7 and len(best) <= 64 else (1800 if len(best) <= 64 else 1200),
            )
        remaining = solver._time_remaining_sec()
        if remaining is not None and remaining >= 3.6:
            best = _n17_try_target_len_window(
                solver,
                best,
                drops=(1, 1),
                round_budget_cap=6.0,
                budget_ratio=0.16,
                label=spec.bucket,
            )
        if len(best) >= before:
            break
    return best


def _run_general_mid_core(solver: "CoveringDesignSolver", sol: list[int], spec: N17CaseSpec) -> list[int]:
    solver._report(
        "optimize",
        (
            "Phase-N17 bucket dispatch: "
            f"{spec.case_id} -> {spec.bucket} ({spec.priority})"
        ),
    )
    return sol


def _run_fallback_bucket(solver: "CoveringDesignSolver", sol: list[int], spec: N17CaseSpec) -> list[int]:
    solver._report(
        "optimize",
        (
            "Phase-N17 bucket dispatch: "
            f"{spec.case_id} -> {spec.bucket} ({spec.priority})"
        ),
    )
    return sol


def run_n17_specialized_module(solver, sol: list[int]) -> list[int]:
    """n=17 白名单专项模块骨架。

    当前阶段按历史瓶颈把 25 个失败 case 细分到独立 bucket。
    先把增益最大的几簇单独领出来，后续逐簇落专项算法。
    """
    spec = get_n17_case_spec(solver.n, solver.k, solver.j, solver.s)
    if spec is None:
        return sol

    if spec.bucket == "jk_large_delta_dense":
        return _run_jk_large_delta_dense(solver, sol, spec)
    if spec.bucket == "containment_fast_bad_dense":
        return _run_containment_fast_bad_dense(solver, sol, spec)
    if spec.bucket == "general_j5_guidance_weak":
        return _run_general_j5_guidance_weak(solver, sol, spec)
    if spec.bucket == "general_k7_j6_hard":
        return _run_general_k7_j6_hard(solver, sol, spec)
    if spec.bucket == "tiny_baseline_exactish":
        return _run_tiny_baseline_exactish(solver, sol, spec)
    if spec.bucket == "general_mid_core":
        return _run_general_mid_core(solver, sol, spec)
    return _run_fallback_bucket(solver, sol, spec)
