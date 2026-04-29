from __future__ import annotations

from dataclasses import dataclass
from math import comb
import os
import random
from typing import TYPE_CHECKING

import numpy as np

try:
    from ortools.sat.python import cp_model  # type: ignore
except Exception:  # pragma: no cover
    cp_model = None

if TYPE_CHECKING:
    from solver import CoveringDesignSolver

from n17_specialized_module import _n17_containment_orbit_refine


@dataclass(frozen=True)
class N18FeatureProfile:
    candidate_count: int
    target_count: int
    one_block_hit_count: int
    target_density: str
    search_shape: str
    expected_bottleneck: str


@dataclass(frozen=True)
class N18StrategyProfile:
    strategy_key: str
    summary: str
    primary_pipeline: tuple[str, ...]
    fallback_pipeline: tuple[str, ...]
    expected_bottleneck: str


@dataclass(frozen=True)
class N18CaseSpec:
    n: int
    k: int
    j: int
    s: int
    family: str
    bucket: str
    feature_profile: N18FeatureProfile
    strategy_profile: N18StrategyProfile

    @property
    def case_id(self) -> str:
        return f"L_{self.n}_{self.k}_{self.j}_{self.s}"


def _classify_family(*, k: int, j: int, s: int) -> str:
    if s == j:
        return "containment_s_eq_j"
    if j == k:
        return "j_eq_k_noncontain_medium_n"
    return "general_noncontain"


def _classify_bucket(*, family: str, k: int, j: int, s: int) -> str:
    if family == "containment_s_eq_j":
        return "containment_dense" if k >= 6 else "containment_nearline"
    if family == "j_eq_k_noncontain_medium_n":
        return "jk_dense_compress" if s == k - 1 else "jk_small_target_exactish"
    if k == 7 and j == 6 and s == 4:
        return "general_k7_j6_local"
    if k == 7 and j >= 5:
        return "general_k7"
    if s == 3:
        return "general_s3"
    return "general_core"


def _build_feature_profile(*, n: int, k: int, j: int, s: int, family: str, bucket: str) -> N18FeatureProfile:
    candidate_count = comb(n, k)
    target_count = comb(n, j)
    one_block_hit_count = comb(k, s) * comb(n - k, k - s)

    if family == "j_eq_k_noncontain_medium_n" and s == k - 1:
        target_density = "sparse_hits"
        search_shape = "dense_solution"
        expected_bottleneck = "首解较早，但删块后重构困难，后半程容易长时间空转"
    elif family == "j_eq_k_noncontain_medium_n":
        target_density = "broad_hits"
        search_shape = "small_target_solution"
        expected_bottleneck = "目标块数很小，通用局部搜索容易在远处打转，需要强限域"
    elif family == "containment_s_eq_j":
        target_density = "containment"
        search_shape = "fast_seed_solution"
        expected_bottleneck = "秒级出合法解，但结构偏粗，缺少后续收缩能力"
    elif bucket == "general_s3":
        target_density = "broad_hits"
        search_shape = "constraint_light"
        expected_bottleneck = "单块命中面很宽，通用启发式容易产生高冗余覆盖"
    else:
        target_density = "mixed_hits"
        search_shape = "midrange_solution"
        expected_bottleneck = "中速出解后进入平台，需要更定向的 repair 与 polish"

    return N18FeatureProfile(
        candidate_count=candidate_count,
        target_count=target_count,
        one_block_hit_count=one_block_hit_count,
        target_density=target_density,
        search_shape=search_shape,
        expected_bottleneck=expected_bottleneck,
    )


def _resolve_strategy_profile(*, family: str, bucket: str, feature_profile: N18FeatureProfile) -> N18StrategyProfile:
    if bucket == "jk_dense_compress":
        if (
            feature_profile.candidate_count <= 4_000
            and feature_profile.target_count <= 4_000
        ):
            return N18StrategyProfile(
                strategy_key="n18_jk_dense_small_candidate_v1",
                summary="小候选 j=k dense 链：连续做 -1 定长下降，再补结构化精修。",
                primary_pipeline=(
                    "seed_reuse",
                    "fixed_size_descent_loop",
                    "domset_polish",
                ),
                fallback_pipeline=("seed_reuse", "bounded_cpsat"),
                expected_bottleneck=feature_profile.expected_bottleneck,
            )
        return N18StrategyProfile(
            strategy_key="n18_jk_dense_compress_v1",
            summary="高块数 j=k 压缩链：从已有合法解出发，做删块、重构与限域精修。",
            primary_pipeline=(
                "seed_reuse",
                "fragile_target_neighborhood",
                "fixed_size_compress",
                "bounded_cpsat",
            ),
            fallback_pipeline=("seed_reuse", "multi_drop_repair", "weighted_restart"),
            expected_bottleneck=feature_profile.expected_bottleneck,
        )
    if bucket == "jk_small_target_exactish":
        return N18StrategyProfile(
            strategy_key="n18_jk_small_target_exactish_v1",
            summary="小目标 j=k 限域链：先缩小候选，再做近精确搜索。",
            primary_pipeline=("orbit_seed", "candidate_shrink", "bounded_cpsat", "exactish_repair"),
            fallback_pipeline=("orbit_seed", "greedy_trim", "tabu_repair"),
            expected_bottleneck=feature_profile.expected_bottleneck,
        )
    if bucket == "containment_dense":
        return N18StrategyProfile(
            strategy_key="n18_containment_dense_v1",
            summary="containment 结构收缩链：围绕快解做权重重排与迭代收缩。",
            primary_pipeline=("containment_seed", "block_weight_reorder", "iterative_drop", "containment_cpsat_polish"),
            fallback_pipeline=("containment_seed", "iterative_sat"),
            expected_bottleneck=feature_profile.expected_bottleneck,
        )
    if bucket == "containment_nearline":
        return N18StrategyProfile(
            strategy_key="n18_containment_nearline_v1",
            summary="containment 近线冲刺链：小步删块加快速验证。",
            primary_pipeline=("containment_seed", "single_drop", "fast_verify"),
            fallback_pipeline=("containment_seed", "iterative_sat"),
            expected_bottleneck=feature_profile.expected_bottleneck,
        )
    if bucket == "general_k7_j6_local":
        return N18StrategyProfile(
            strategy_key="n18_general_k7_j6_local_v1",
            summary="k=7,j=6,s=4 局部邻域链：一换一候选池上做轻量定长下降。",
            primary_pipeline=("general_seed", "one_swap_pool", "local_target_drop"),
            fallback_pipeline=("general_seed", "two_stage_local_search"),
            expected_bottleneck="全量覆盖表构建成本过高，需改走局部候选池而非全局表",
        )
    if bucket == "general_k7":
        return N18StrategyProfile(
            strategy_key="n18_general_k7_v1",
            summary="k=7 通用非包含链：两阶段局部搜索加限域 polish。",
            primary_pipeline=("general_seed", "two_stage_local_search", "targeted_repair", "bounded_cpsat"),
            fallback_pipeline=("general_seed", "weighted_restart", "fast_polish"),
            expected_bottleneck=feature_profile.expected_bottleneck,
        )
    if bucket == "general_s3":
        return N18StrategyProfile(
            strategy_key="n18_general_s3_v1",
            summary="s=3 宽命中链：优先压冗余覆盖，再做快速抛光。",
            primary_pipeline=("general_seed", "coverage_entropy_filter", "multi_drop_repair", "fast_polish"),
            fallback_pipeline=("general_seed", "bounded_cpsat"),
            expected_bottleneck=feature_profile.expected_bottleneck,
        )
    return N18StrategyProfile(
        strategy_key="n18_general_core_v1",
        summary="通用非包含核心链：定向 repair 加小范围 polish。",
        primary_pipeline=("general_seed", "targeted_repair", "bounded_cpsat"),
        fallback_pipeline=("general_seed", "weighted_restart"),
        expected_bottleneck=feature_profile.expected_bottleneck,
    )


def is_n18_special_case(n: int, k: int, j: int, s: int) -> bool:
    return int(n) == 18 and 4 <= int(k) <= 7 and 3 <= int(s) <= int(j) <= int(k)


def get_n18_case_spec(n: int, k: int, j: int, s: int) -> N18CaseSpec | None:
    if not is_n18_special_case(n, k, j, s):
        return None
    family = _classify_family(k=int(k), j=int(j), s=int(s))
    bucket = _classify_bucket(family=family, k=int(k), j=int(j), s=int(s))
    feature_profile = _build_feature_profile(
        n=int(n),
        k=int(k),
        j=int(j),
        s=int(s),
        family=family,
        bucket=bucket,
    )
    strategy_profile = _resolve_strategy_profile(
        family=family,
        bucket=bucket,
        feature_profile=feature_profile,
    )
    return N18CaseSpec(
        n=int(n),
        k=int(k),
        j=int(j),
        s=int(s),
        family=family,
        bucket=bucket,
        feature_profile=feature_profile,
        strategy_profile=strategy_profile,
    )


def run_n18_specialized_module(solver: "CoveringDesignSolver", sol: list[int]) -> list[int]:
    spec = get_n18_case_spec(solver.n, solver.k, solver.j, solver.s)
    if spec is None:
        return sol

    remaining = solver._time_remaining_sec()
    solver._report(
        "optimize",
        (
            "Phase-N18 specialized dispatch: "
            f"{spec.case_id} -> family={spec.family}, bucket={spec.bucket}, "
            f"strategy={spec.strategy_profile.strategy_key}, "
            f"remaining={None if remaining is None else round(remaining, 3)}"
        ),
    )
    if spec.strategy_profile.strategy_key == "n18_jk_dense_compress_v1":
        return _run_jk_dense_compress_v1(solver, sol, spec)
    if spec.strategy_profile.strategy_key == "n18_jk_dense_small_candidate_v1":
        return _run_jk_dense_small_candidate_v1(solver, sol, spec)
    if spec.strategy_profile.strategy_key == "n18_containment_dense_v1":
        return _run_containment_dense_v1(solver, sol, spec)
    if spec.strategy_profile.strategy_key == "n18_containment_nearline_v1":
        return _run_containment_nearline_v1(solver, sol, spec)
    if spec.strategy_profile.strategy_key == "n18_general_core_v1":
        return _run_general_core_v1(solver, sol, spec)
    if spec.strategy_profile.strategy_key == "n18_general_s3_v1":
        return _run_general_s3_v1(solver, sol, spec)
    if spec.strategy_profile.strategy_key == "n18_general_k7_j6_local_v1":
        return _run_general_k7_j6_local_v1(solver, sol, spec)
    if spec.strategy_profile.strategy_key == "n18_general_k7_v1":
        return _run_general_k7_v1(solver, sol, spec)
    return sol


def _run_jk_dense_compress_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    if len(sol) < 16:
        return sol

    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 1.0:
        return sol

    best = list(sol)
    hard_case = spec.s == spec.k - 1
    is_ultra_large = (
        spec.feature_profile.candidate_count >= 30_000
        or spec.feature_profile.target_count >= 30_000
        or len(best) >= 700
    )
    solver._report(
        "optimize",
        (
            "Phase-N18 jk-dense start: "
            f"len={len(best)}, one_block_hits={spec.feature_profile.one_block_hit_count}, "
            f"ultra={is_ultra_large}"
        ),
    )

    improved_once = False
    remaining = solver._time_remaining_sec()
    if is_ultra_large and remaining is not None and remaining >= 3.0:
        solver._report(
            "optimize",
            "Phase-N18 jk-dense ultra-neighborhood: try before fixed-size compression",
        )
        refined = _run_jk_dense_ultra_neighborhood(solver, best)
        if len(refined) < len(best):
            best = refined
            improved_once = True
            solver._report(
                "optimize",
                f"Phase-N18 jk-dense ultra-neighborhood refined to {len(best)} groups",
            )

    rounds = 1 if is_ultra_large else (4 if hard_case else 3)
    for round_idx in range(rounds):
        remaining = solver._time_remaining_sec()
        if remaining is None or remaining < 3.0:
            break
        target_drop = 2 if (hard_case and len(best) >= 180 and remaining >= 16.0) else 1
        target_len = len(best) - target_drop
        if target_len < 1:
            break
        round_budget = min(
            5.0 if is_ultra_large else (18.0 if hard_case else 12.0),
            max(2.0, remaining * (0.08 if is_ultra_large else (0.26 if hard_case else 0.22))),
        )
        start_masks = list(best)
        random.shuffle(start_masks)
        improved = solver._phase_g_try_target_len(start_masks, target_len, float(round_budget))
        if improved is None and target_drop == 2:
            improved = solver._phase_g_try_target_len(start_masks, len(best) - 1, float(round_budget))
        if improved is None:
            continue
        if len(improved) < len(best):
            best = improved
            improved_once = True
            solver._report(
                "optimize",
                f"Phase-N18 jk-dense round {round_idx + 1}: improved to {len(best)} groups",
            )

    remaining = solver._time_remaining_sec()
    if improved_once and (not is_ultra_large):
        if hard_case and remaining is not None and remaining >= 5.0:
            best = _run_jk_dense_hard_tail_descent_v1(solver, best)
            remaining = solver._time_remaining_sec()
        if remaining is not None and remaining >= 5.0:
            refined = solver._phase_i_full_cp_sat_module(best, hard_case=True)
            if len(refined) < len(best):
                best = refined
                solver._report(
                    "optimize",
                    f"Phase-N18 jk-dense CP-SAT refined to {len(best)} groups",
                )
        best = _run_jk_dense_post_refine_v1(solver, best, spec)

    if len(best) < len(sol) and solver._verify(best):
        return best
    return sol


def _run_jk_dense_post_refine_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    best = list(sol)
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 2.5:
        return best

    if (
        spec.feature_profile.candidate_count <= 12_000
        and remaining is not None
        and remaining >= 3.5
        and hasattr(solver, "_phase_k_jk_kminus1_domset_refine")
    ):
        refined = solver._phase_k_jk_kminus1_domset_refine(best)
        if len(refined) < len(best) and solver._verify(refined):
            best = refined
            solver._report(
                "optimize",
                f"Phase-N18 jk-dense domset refined to {len(best)} groups",
            )

    remaining = solver._time_remaining_sec()
    if len(best) >= 24 and remaining is not None and remaining >= 2.2 and hasattr(solver, "_local_search"):
        refined = solver._local_search(list(best))
        if len(refined) < len(best) and solver._verify(refined):
            best = refined
            solver._report(
                "optimize",
                f"Phase-N18 jk-dense local-search refined to {len(best)} groups",
            )

    remaining = solver._time_remaining_sec()
    if (
        remaining is None
        or remaining < 3.0
        or len(best) < 80
        or not hasattr(solver, "_phase_g_try_target_len")
    ):
        return best

    sweep_count = 2 if remaining >= 7.0 else 1
    for sweep_idx in range(sweep_count):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 2.8:
            break
        start_masks = list(best)
        random.shuffle(start_masks)
        target_len = len(best) - 1
        if target_len < 1:
            break
        budget = min(6.0, max(2.0, rem * 0.16))
        improved = solver._phase_g_try_target_len(start_masks, target_len, float(budget))
        if improved is None or len(improved) >= len(best):
            continue
        if not solver._verify(improved):
            continue
        best = improved
        solver._report(
            "optimize",
            f"Phase-N18 jk-dense post-sweep {sweep_idx + 1}: improved to {len(best)} groups",
        )

    if spec.s == spec.k - 1:
        best = _run_jk_dense_hard_tail_descent_v1(solver, best)

    return best


def _run_jk_dense_hard_tail_descent_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if len(sol) < 180:
        return sol
    if not hasattr(solver, "_phase_g_try_target_len"):
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 5.0:
        return sol

    best = list(sol)
    drop_plan = (1, 1, 1) if len(best) <= 320 else (1, 1)
    for step_idx, drop in enumerate(drop_plan):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 3.2:
            break
        target_len = len(best) - drop
        if target_len < 1:
            break
        budget = float(min(10.0, max(2.8, rem * 0.20)))
        improved = solver._phase_g_try_target_len(list(best), target_len, budget)
        if improved is None or len(improved) >= len(best):
            continue
        if not solver._verify(improved):
            continue
        best = improved
        solver._report(
            "optimize",
            f"Phase-N18 jk-dense hard-tail step {step_idx + 1}: improved to {len(best)} groups",
        )
    return best


def _run_jk_dense_small_candidate_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    if len(sol) < 16:
        return sol

    if (
        (not hasattr(solver, "_cov_table"))
        or (not hasattr(solver, "_inv_table"))
        or solver._cov_table is None
        or solver._inv_table is None
    ):
        if hasattr(solver, "_build_coverage_tables"):
            solver._build_coverage_tables()

    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 2.5:
        return sol

    best = list(sol)
    solver._report(
        "optimize",
        (
            "Phase-N18 jk-dense-small start: "
            f"len={len(best)}, candidates={spec.feature_profile.candidate_count}, "
            f"targets={spec.feature_profile.target_count}"
        ),
    )

    miss_count = 0
    round_idx = 0
    while True:
        remaining = solver._time_remaining_sec()
        if remaining is None or remaining < 2.6:
            break
        target_len = len(best) - 1
        if target_len < 1:
            break
        round_idx += 1
        budget = min(8.0, max(2.6, remaining * 0.24))
        start_masks = list(best)
        random.shuffle(start_masks)
        improved = solver._phase_g_try_target_len(start_masks, target_len, float(budget))
        miss_limit = 2
        if improved is None or len(improved) >= len(best):
            miss_count += 1
            if miss_count >= miss_limit:
                break
            continue
        if not solver._verify(improved):
            miss_count += 1
            if miss_count >= miss_limit:
                break
            continue
        best = improved
        miss_count = 0
        solver._report(
            "optimize",
            f"Phase-N18 jk-dense-small round {round_idx}: improved to {len(best)} groups",
        )

    remaining = solver._time_remaining_sec()
    if (
        remaining is not None
        and remaining >= 3.5
        and hasattr(solver, "_phase_k_jk_kminus1_domset_refine")
    ):
        refined = solver._phase_k_jk_kminus1_domset_refine(best)
        if len(refined) < len(best) and solver._verify(refined):
            best = refined
            solver._report(
                "optimize",
                f"Phase-N18 jk-dense-small domset refined to {len(best)} groups",
            )

    if len(best) < len(sol) and solver._verify(best):
        return best
    return sol


def _run_jk_dense_ultra_neighborhood(
    solver: "CoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if cp_model is None:
        return sol
    if not hasattr(solver, "_cov_table") or not hasattr(solver, "_inv_table"):
        return sol
    if solver._cov_table is None or solver._inv_table is None:
        if not hasattr(solver, "_build_coverage_tables"):
            return sol
        solver._report(
            "optimize",
            "Phase-N18 jk-dense ultra-neighborhood: build coverage tables on demand",
        )
        solver._build_coverage_tables()
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if not hasattr(solver, "_cand_index_map") or not hasattr(solver, "_build_cyclic_orbits"):
        return sol

    cand_index = solver._cand_index_map
    selected_idx = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_idx) != len(sol):
        return sol

    cov_table = solver._cov_table
    inv_table = solver._inv_table
    counts = np.zeros(solver.num_targets, dtype=np.int32)
    for ci in selected_idx:
        counts[cov_table[ci]] += 1

    fragile_targets = np.flatnonzero(counts <= 2)
    if len(fragile_targets) == 0:
        fragile_targets = np.flatnonzero(counts <= 3)
    if len(fragile_targets) == 0:
        return sol

    scores = np.zeros(solver.num_cands, dtype=np.float64)
    for ti in fragile_targets:
        weight = 3.0 if counts[int(ti)] <= 1 else 1.5
        scores[inv_table[int(ti)]] += weight

    orbits = solver._build_cyclic_orbits()
    orbit_of = np.full(solver.num_cands, -1, dtype=np.int32)
    for oid, orbit in enumerate(orbits):
        for ci in orbit:
            orbit_of[ci] = oid

    selected_set = set(selected_idx)
    ranked = np.argsort(scores)[::-1]
    neighborhood = list(selected_idx)
    per_orbit_extra: dict[int, int] = {}
    extras_cap = 900
    orbit_cap = 3
    for ci in ranked:
        cii = int(ci)
        if cii in selected_set:
            continue
        if scores[cii] <= 0:
            break
        oid = int(orbit_of[cii])
        used = per_orbit_extra.get(oid, 0)
        if used >= orbit_cap:
            continue
        neighborhood.append(cii)
        per_orbit_extra[oid] = used + 1
        if len(neighborhood) >= len(selected_idx) + extras_cap:
            break

    local_pos = {ci: idx for idx, ci in enumerate(neighborhood)}
    if len(local_pos) == len(selected_idx):
        return sol

    solver._report(
        "optimize",
        (
            "Phase-N18 jk-dense ultra-neighborhood: "
            f"fragile_targets={len(fragile_targets)}, vars={len(neighborhood)}"
        ),
    )

    model = cp_model.CpModel()
    vars_x = [model.NewBoolVar(f"xn18_{i}") for i in range(len(neighborhood))]
    model.Add(sum(vars_x) <= len(sol) - 1)
    for covering in inv_table:
        loc = [local_pos[int(ci)] for ci in covering if int(ci) in local_pos]
        if not loc:
            return sol
        model.AddBoolOr([vars_x[i] for i in loc])
    model.Minimize(sum(vars_x))

    for ci in selected_idx:
        model.AddHint(vars_x[local_pos[ci]], 1)

    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 3.0:
        return sol

    per_run = min(10.0, max(2.0, remaining * 0.22))
    seeds = [1, 17]
    best_masks = list(sol)
    best_len = len(sol)
    for seed in seeds:
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 2.0:
            break
        sat = cp_model.CpSolver()
        sat.parameters.max_time_in_seconds = float(min(per_run, max(1.5, rem_seed - 0.8)))
        sat.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat.parameters.random_seed = seed
        sat.parameters.randomize_search = True
        status = sat.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked_local = [i for i in range(len(neighborhood)) if sat.Value(vars_x[i]) == 1]
        if len(picked_local) >= best_len:
            continue
        picked_global = [neighborhood[i] for i in picked_local]
        candidate = [int(solver.cand_masks[i]) for i in picked_global]
        candidate = solver._local_search(candidate)
        if len(candidate) >= best_len:
            continue
        if not solver._verify(candidate):
            continue
        best_masks = candidate
        best_len = len(candidate)
        break

    return best_masks


def _run_containment_dense_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    return _run_containment_core_v1(solver, sol, spec, aggressive=True)


def _run_containment_nearline_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    return _run_containment_core_v1(solver, sol, spec, aggressive=False)


def _run_containment_core_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
    *,
    aggressive: bool,
) -> list[int]:
    if len(sol) < 12:
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 2.5:
        return sol

    best = list(sol)
    solver._report(
        "optimize",
        (
            "Phase-N18 containment start: "
            f"len={len(best)}, bucket={spec.bucket}, aggressive={aggressive}"
        ),
    )

    if (
        (not hasattr(solver, "_cov_table"))
        or (not hasattr(solver, "_inv_table"))
        or solver._cov_table is None
        or solver._inv_table is None
    ) and hasattr(solver, "_build_coverage_tables"):
        solver._build_coverage_tables()

    best = _run_containment_target_drop_v1(solver, best, aggressive=aggressive)

    remaining = solver._time_remaining_sec()
    if remaining is not None and remaining >= 3.8:
        best = _run_containment_orbit_refine_v1(
            solver,
            best,
            aggressive=aggressive,
            extended=False,
        )

    remaining = solver._time_remaining_sec()
    if (
        aggressive
        and spec.k >= 7
        and len(best) >= 400
        and remaining is not None
        and remaining >= 3.0
    ):
        best = _n17_containment_orbit_refine(
            solver,
            best,
            label="n18_containment_dense_followup",
        )

    remaining = solver._time_remaining_sec()
    if (
        remaining is not None
        and remaining >= 3.5
        and hasattr(solver, "_phase_k_containment_iterative_sat_refine")
    ):
        refined = solver._phase_k_containment_iterative_sat_refine(best)
        if len(refined) < len(best) and solver._verify(refined):
            best = refined
            solver._report(
                "optimize",
                f"Phase-N18 containment SAT refined to {len(best)} groups",
            )

    if len(best) < len(sol) and solver._verify(best):
        return best
    return sol


def _run_containment_target_drop_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    aggressive: bool,
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 12:
        return sol

    best = list(sol)
    rounds = 6 if aggressive else 4
    misses = 0
    for _ in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 2.2:
            break
        target_drop = 2 if aggressive and len(best) <= 180 else 1
        target_len = len(best) - target_drop
        if target_len < 1:
            break
        budget = float(min(10.0 if aggressive else 7.0, max(2.0, rem * (0.22 if aggressive else 0.16))))
        start_masks = list(best)
        if misses > 0:
            random.shuffle(start_masks)
        improved = solver._phase_g_try_target_len(start_masks, target_len, budget)
        if improved is None and target_drop == 2:
            improved = solver._phase_g_try_target_len(start_masks, len(best) - 1, budget)
        if improved is None or len(improved) >= len(best):
            misses += 1
            if misses >= 3:
                break
            continue
        if not solver._verify(improved):
            misses += 1
            if misses >= 3:
                break
            continue
        best = improved
        misses = 0
        solver._report(
            "optimize",
            f"Phase-N18 containment target-drop refined to {len(best)} groups",
        )
    return best


def _run_containment_orbit_refine_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    aggressive: bool,
    extended: bool = False,
) -> list[int]:
    if cp_model is None:
        return sol
    if not solver._containment:
        return sol
    if solver._inv_table is None or solver._deadline_at is None:
        return sol
    if len(sol) < 20:
        return sol
    if not hasattr(solver, "_build_cyclic_orbits"):
        return sol
    if not solver._phase_c_has_time(3.2):
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

    best_masks = list(sol)
    best_len = len(best_masks)
    ub = best_len - 1
    rem = solver._time_remaining_sec()
    if rem is None or rem < 2.4:
        return sol

    model = cp_model.CpModel()
    vars_y = [model.NewBoolVar(f"n18_yc_{i}") for i in range(len(orbits))]
    weighted = sum(int(orbit_sizes[i]) * vars_y[i] for i in range(len(orbits)))
    model.Add(weighted <= ub)
    for cover in target_cover_orbits:
        model.AddBoolOr([vars_y[i] for i in cover])
    model.Minimize(weighted)

    if extended:
        seeds = [1, 17, 29]
        if rem >= 10.0:
            seeds.extend([43, 59])
        per_run = min(14.0, max(3.5, rem * 0.34))
    else:
        seeds = [1, 17] if aggressive else [1]
        per_run = min(
            10.0 if aggressive else 7.0,
            max(2.5, rem * (0.24 if aggressive else 0.18)),
        )
    for seed in seeds:
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 2.0:
            break
        sat = cp_model.CpSolver()
        sat.parameters.max_time_in_seconds = float(
            min(per_run, max(1.5, rem_seed - (0.6 if extended else 0.5)))
        )
        sat.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        sat.parameters.random_seed = seed
        sat.parameters.randomize_search = True
        status = sat.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked_orbits = [i for i in range(len(orbits)) if sat.Value(vars_y[i]) == 1]
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
        best_masks = candidate
        best_len = len(best_masks)
        solver._report(
            "optimize",
            (
                "Phase-N18 containment orbit refined to "
                f"{best_len} groups"
                f"{' (extended)' if extended else ''}"
            ),
        )
        break

    return best_masks


def _run_general_core_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    return _run_general_target_drop_core_v1(
        solver,
        sol,
        spec,
        rounds=4,
        budget_cap=8.0,
        budget_ratio=0.18,
    )


def _run_general_s3_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    return _run_general_target_drop_core_v1(
        solver,
        sol,
        spec,
        rounds=5,
        budget_cap=8.0,
        budget_ratio=0.20,
    )


def _run_general_k7_j6_local_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    if len(sol) < 12 or len(sol) > 48:
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 2.0:
        return sol

    solver._report(
        "optimize",
        (
            "Phase-N18 general-k7-j6-local start: "
            f"len={len(sol)}, bucket={spec.bucket}"
        ),
    )
    best = _run_general_k7_j6_local_target_drop_v1(solver, list(sol))
    if len(best) < len(sol) and solver._verify(best):
        solver._report(
            "optimize",
            f"Phase-N18 general-k7-j6-local refined to {len(best)} groups",
        )
        return best
    return sol


def _run_general_k7_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
) -> list[int]:
    if spec.j == 6 and spec.s >= 5 and len(sol) >= 120:
        best = _run_general_k7_j6_focused_local_drop_v1(
            solver,
            sol,
            top_blocks=28,
            round_budget=4.0,
        )
        if len(best) < len(sol):
            return best
    return _run_general_target_drop_core_v1(
        solver,
        sol,
        spec,
        rounds=5,
        budget_cap=9.0,
        budget_ratio=0.20,
    )


def _mask_to_elements(mask: int) -> list[int]:
    elems: list[int] = []
    pos = 0
    mm = int(mask)
    while mm:
        if mm & 1:
            elems.append(pos)
        mm >>= 1
        pos += 1
    return elems


def _popcount_uint32_local(arr: np.ndarray) -> np.ndarray:
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


def _build_general_k7_j6_one_swap_pool(
    solver: "CoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    pool: set[int] = {int(mask) for mask in sol}
    for mask in sol:
        bits_in = _mask_to_elements(int(mask))
        bit_in_set = set(bits_in)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        for rem in bits_in:
            base = int(mask) & (~(1 << rem))
            for add in bits_out:
                cand = base | (1 << add)
                if cand in solver._cand_index_map:
                    pool.add(cand)
    return sorted(pool)


def _rank_solution_fragile_block_indices(
    solver: "CoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if not sol:
        return []
    sel_arr = np.asarray(sol, dtype=np.uint32)
    hits = _popcount_uint32_local(
        sel_arr[:, None] & solver.target_masks[None, :]
    ) >= solver.s
    counts = hits.sum(axis=0)
    scored: list[tuple[int, int]] = []
    for idx in range(hits.shape[0]):
        unique = int(np.sum(counts[hits[idx]] == 1))
        fragile = int(np.sum(counts[hits[idx]] == 2))
        scored.append((unique * 10 + fragile, idx))
    scored.sort(reverse=True)
    return [idx for _, idx in scored]


def _build_general_k7_j6_focused_pool(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    top_blocks: int,
) -> list[int]:
    ranked = _rank_solution_fragile_block_indices(solver, sol)
    focus_masks = [sol[idx] for idx in ranked[:top_blocks]]
    pool: set[int] = {int(mask) for mask in sol}
    for mask in focus_masks:
        bits_in = _mask_to_elements(int(mask))
        bit_in_set = set(bits_in)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        for rem in bits_in:
            base = int(mask) & (~(1 << rem))
            for add in bits_out:
                cand = base | (1 << add)
                if cand in solver._cand_index_map:
                    pool.add(cand)
    return sorted(pool)


def _build_local_cov_inv_tables(
    solver: "CoveringDesignSolver",
    pool_masks: list[int],
) -> tuple[np.ndarray, list[np.ndarray], list[np.ndarray]]:
    pool_arr = np.asarray(pool_masks, dtype=np.uint32)
    local_cov: list[np.ndarray] = []
    local_inv_lists: list[list[int]] = [[] for _ in range(solver.num_targets)]
    chunk = 256
    for start in range(0, len(pool_arr), chunk):
        cand_chunk = pool_arr[start : start + chunk]
        hits = _popcount_uint32_local(
            cand_chunk[:, None] & solver.target_masks[None, :]
        ) >= solver.s
        for local_idx in range(hits.shape[0]):
            cov = np.flatnonzero(hits[local_idx]).astype(np.int32)
            local_cov.append(cov)
            ci = start + local_idx
            for ti in cov.tolist():
                local_inv_lists[ti].append(ci)
    local_inv = [np.asarray(items, dtype=np.int32) for items in local_inv_lists]
    return pool_arr, local_cov, local_inv


def _run_general_k7_j6_local_target_drop_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if len(sol) < 12 or len(sol) > 48:
        return sol
    if solver._deadline_at is None:
        return sol

    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 2.0:
        return sol

    best = list(sol)
    for stage_idx in range(2):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 1.5:
            break

        pool_masks = _build_general_k7_j6_one_swap_pool(solver, best)
        if len(pool_masks) <= len(best):
            break

        build_started = solver._time_remaining_sec()
        pool_arr, local_cov, local_inv = _build_local_cov_inv_tables(solver, pool_masks)
        build_finished = solver._time_remaining_sec()
        build_cost = None
        if build_started is not None and build_finished is not None:
            build_cost = max(0.0, build_started - build_finished)
        solver._report(
            "optimize",
            (
                "Phase-N18 general-k7-j6-local pool built: "
                f"stage={stage_idx + 1}, pool={len(pool_masks)}, build_cost="
                f"{None if build_cost is None else round(build_cost, 3)}s"
            ),
        )

        original_cand_masks = solver.cand_masks
        original_cand_index_map = solver._cand_index_map
        original_cov_table = solver._cov_table
        original_inv_table = solver._inv_table
        original_num_cands = solver.num_cands
        try:
            solver.cand_masks = pool_arr
            solver._cand_index_map = {int(mask): idx for idx, mask in enumerate(pool_masks)}
            solver._cov_table = local_cov
            solver._inv_table = local_inv
            solver.num_cands = len(pool_masks)

            target_len = len(best) - 1
            if target_len < 1:
                break
            budget = float(min(8.0, max(1.4, rem * 0.42)))
            improved = solver._phase_g_try_target_len(list(best), target_len, budget)
            if improved is None or len(improved) >= len(best):
                break
            if not solver._verify(improved):
                break
            best = improved
            solver._report(
                "optimize",
                f"Phase-N18 general-k7-j6-local round improved to {len(best)} groups",
            )
        finally:
            solver.cand_masks = original_cand_masks
            solver._cand_index_map = original_cand_index_map
            solver._cov_table = original_cov_table
            solver._inv_table = original_inv_table
            solver.num_cands = original_num_cands
    return best


def _run_general_k7_j6_focused_local_drop_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    *,
    top_blocks: int,
    round_budget: float,
) -> list[int]:
    if len(sol) < 80 or solver._deadline_at is None:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 0.9:
        return sol

    pool_masks = _build_general_k7_j6_focused_pool(
        solver,
        sol,
        top_blocks=top_blocks,
    )
    if len(pool_masks) <= len(sol):
        return sol

    build_started = solver._time_remaining_sec()
    pool_arr, local_cov, local_inv = _build_local_cov_inv_tables(solver, pool_masks)
    build_finished = solver._time_remaining_sec()
    build_cost = None
    if build_started is not None and build_finished is not None:
        build_cost = max(0.0, build_started - build_finished)
    solver._report(
        "optimize",
        (
            "Phase-N18 general-k7 focused pool built: "
            f"pool={len(pool_masks)}, build_cost="
            f"{None if build_cost is None else round(build_cost, 3)}s"
        ),
    )

    original_cand_masks = solver.cand_masks
    original_cand_index_map = solver._cand_index_map
    original_cov_table = solver._cov_table
    original_inv_table = solver._inv_table
    original_num_cands = solver.num_cands
    try:
        solver.cand_masks = pool_arr
        solver._cand_index_map = {int(mask): idx for idx, mask in enumerate(pool_masks)}
        solver._cov_table = local_cov
        solver._inv_table = local_inv
        solver.num_cands = len(pool_masks)
        budget = float(
            min(
                round_budget,
                max(0.6, (solver._time_remaining_sec() or round_budget) * 0.45),
            )
        )
        improved = solver._phase_g_try_target_len(list(sol), len(sol) - 1, budget)
        if improved is None or len(improved) >= len(sol):
            return sol
        if not solver._verify(improved):
            return sol
        solver._report(
            "optimize",
            f"Phase-N18 general-k7 focused local drop refined to {len(improved)} groups",
        )
        return improved
    finally:
        solver.cand_masks = original_cand_masks
        solver._cand_index_map = original_cand_index_map
        solver._cov_table = original_cov_table
        solver._inv_table = original_inv_table
        solver.num_cands = original_num_cands


def _run_general_target_drop_core_v1(
    solver: "CoveringDesignSolver",
    sol: list[int],
    spec: N18CaseSpec,
    *,
    rounds: int,
    budget_cap: float,
    budget_ratio: float,
) -> list[int]:
    if len(sol) < 10:
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 2.5:
        return sol

    best = list(sol)
    solver._report(
        "optimize",
        (
            "Phase-N18 general start: "
            f"len={len(best)}, bucket={spec.bucket}, rounds={rounds}"
        ),
    )

    if (
        (not hasattr(solver, "_cov_table"))
        or (not hasattr(solver, "_inv_table"))
        or solver._cov_table is None
        or solver._inv_table is None
    ) and hasattr(solver, "_build_coverage_tables"):
        solver._build_coverage_tables()

    misses = 0
    for round_idx in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 2.2:
            break
        target_len = len(best) - 1
        if target_len < 1:
            break
        budget = float(min(budget_cap, max(2.0, rem * budget_ratio)))
        start_masks = list(best)
        if misses > 0:
            random.shuffle(start_masks)
        improved = solver._phase_g_try_target_len(start_masks, target_len, budget)
        if improved is None or len(improved) >= len(best):
            misses += 1
            if misses >= 3:
                break
            continue
        if not solver._verify(improved):
            misses += 1
            if misses >= 3:
                break
            continue
        best = improved
        misses = 0
        solver._report(
            "optimize",
            f"Phase-N18 general round {round_idx + 1}: improved to {len(best)} groups",
        )

    remaining = solver._time_remaining_sec()
    if (
        remaining is not None
        and remaining >= 3.0
        and hasattr(solver, "_phase_k_general_iterative_sat_refine")
    ):
        refined = solver._phase_k_general_iterative_sat_refine(best)
        if len(refined) < len(best) and solver._verify(refined):
            best = refined
            solver._report(
                "optimize",
                f"Phase-N18 general SAT refined to {len(best)} groups",
            )

    if len(best) < len(sol) and solver._verify(best):
        return best
    return sol
