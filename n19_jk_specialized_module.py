from __future__ import annotations

import os
import random
from dataclasses import replace
from itertools import combinations
from typing import TYPE_CHECKING

import numpy as np

from solver import cp_model
from solver import mask_to_elements
from solver import popcount_uint32

if TYPE_CHECKING:
    from solver import CoveringDesignSolver as BaseCoveringDesignSolver


def is_n19_jk_target_case(*, n: int, k: int, j: int, s: int) -> bool:
    return int(n) == 19 and int(j) == int(k) and int(s) == (int(k) - 1)


def is_n19_jk_small_s_case(*, n: int, k: int, j: int, s: int) -> bool:
    return (int(n), int(k), int(j), int(s)) in {
        (19, 4, 4, 3),
        (19, 5, 5, 3),
        (19, 6, 6, 4),
    }


def is_n19_jk_small_s_direct_case(*, n: int, k: int, j: int, s: int) -> bool:
    return (int(n), int(k), int(j), int(s)) in {
        (19, 4, 4, 3),
        (19, 5, 5, 3),
    }


def should_use_n19_jk_direct_lane(
    solver: "BaseCoveringDesignSolver",
) -> bool:
    return (
        is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s)
        and solver._deadline_at is not None
        and solver.k == 6
        and solver.num_targets >= 20_000
    )


def should_use_n19_jk_kminus1_sparse_tables(
    solver: "BaseCoveringDesignSolver",
) -> bool:
    return (
        is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s)
        and solver._deadline_at is not None
        and solver.k >= 7
        and solver.num_targets >= 50_000
    )


def should_use_n19_jk_small_s_direct_lane(
    solver: "BaseCoveringDesignSolver",
) -> bool:
    return (
        is_n19_jk_small_s_direct_case(
            n=solver.n,
            k=solver.k,
            j=solver.j,
            s=solver.s,
        )
        and solver._deadline_at is not None
        and (solver._time_remaining_sec() or 0.0) >= 18.0
    )


def solve_n19_jk_direct_lane(
    solver: "BaseCoveringDesignSolver",
) -> list[int] | None:
    if not should_use_n19_jk_direct_lane(solver):
        return None

    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 12.0:
        return None

    anchors = _build_n19_jk_progression_anchor_indices(solver)
    if not anchors:
        return None

    solver._report(
        "optimize",
        (
            "N19 jk direct lane: "
            f"targets={solver.num_targets}, cands={solver.num_cands}, "
            f"anchors={len(anchors)}"
        ),
    )

    best: list[int] | None = None
    best_len: int | None = None
    attempts: list[tuple[int, int]] = []
    primary_seed_lengths = [1, 2, 3]
    if solver.k >= 7:
        primary_seed_lengths = [1, 2]
    anchor_cap = min(len(anchors), 4 if solver.k >= 7 else 5)
    for seed_len in primary_seed_lengths:
        for anchor_idx in anchors[:anchor_cap]:
            attempts.append((anchor_idx, seed_len))

    for anchor_idx, seed_len in attempts:
        rem = solver._time_remaining_sec()
        if rem is None or rem < 6.0:
            break

        partial = _build_n19_jk_seed_partial(solver, anchor_idx, seed_len)
        candidate = solver._fast_complete_partial_solution(
            partial,
            best_limit=best_len,
        )
        if candidate is None:
            continue

        if (not should_use_n19_jk_direct_lane(solver)) and (
            best_len is None or len(candidate) <= best_len + 8
        ):
            candidate = solver._local_search(candidate)
        if not solver._verify(candidate):
            continue

        if best is None or len(candidate) < best_len:
            best = candidate
            best_len = len(candidate)
            solver._note_legal_solution()
            solver._report(
                "optimize",
                (
                    "N19 jk direct lane improved to "
                    f"{best_len} groups (seed_len={seed_len})"
                ),
            )

    return best


def ensure_n19_jk_kminus1_sparse_tables(
    solver: "BaseCoveringDesignSolver",
) -> bool:
    if not should_use_n19_jk_kminus1_sparse_tables(solver):
        return False
    if getattr(solver, "_n19_jk_kminus1_sparse_ready", False):
        return True

    cand_index = solver._cand_index_map
    shared: list[np.ndarray] = []
    for ci in range(solver.num_cands):
        dom = np.array(
            _dominating_indices_for_candidate_index(solver, cand_index, ci),
            dtype=np.int32,
        )
        shared.append(dom)

    # 对 j=k, s=k-1 的 n=19 大实例，目标和候选是一一对应的，
    # 这里覆盖关系也是对称的，所以可共享同一份稀疏表，避免双份内存。
    solver._cov_table = shared
    solver._inv_table = shared
    solver._base_weighted_scores = solver._build_base_weighted_scores()
    solver._n19_jk_kminus1_sparse_ready = True
    solver._report(
        "optimize",
        (
            "N19 jk k-1 sparse tables ready: "
            f"targets={solver.num_targets}, cands={solver.num_cands}, "
            f"avg_cover={sum(len(row) for row in shared) / max(1, len(shared)):.1f}"
        ),
    )
    return True


def solve_n19_jk_small_s_direct_lane(
    solver: "BaseCoveringDesignSolver",
) -> list[int] | None:
    if not should_use_n19_jk_small_s_direct_lane(solver):
        return None
    if not _ensure_n19_jk_sparse_overlap_tables(solver):
        return None

    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 14.0:
        return None

    best: list[int] | None = None
    profiles = _build_n19_jk_small_s_direct_profiles(solver)
    if not profiles:
        return None

    solver._report(
        "optimize",
        (
            "N19 jk-small direct lane: "
            f"targets={solver.num_targets}, cands={solver.num_cands}, "
            f"profiles={len(profiles)}"
        ),
    )

    max_runs = min(len(profiles), 5 if solver.k == 4 else 3)
    for profile in profiles[:max_runs]:
        rem = solver._time_remaining_sec()
        if rem is None or rem < 5.0:
            break

        rebuilt, complete, _ = solver._greedy(
            profile,
            best_limit=(len(best) - 1) if best is not None else None,
        )
        if not complete:
            continue

        candidate = solver._local_search(rebuilt)
        if solver.k == 5 and solver.s == 3:
            candidate = solver._phase_f_mid_cp_sat_neighborhood(candidate)
        candidate = _n19_jk_small_s_direct_polish(solver, candidate)
        if not solver._verify(candidate):
            continue
        if best is None or len(candidate) < len(best):
            best = candidate
            solver._note_legal_solution()
            solver._report(
                "optimize",
                (
                    "N19 jk-small direct lane improved to "
                    f"{len(best)} groups via {profile.name}"
                ),
            )

    return best


def refine_n19_jk_solution(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    """对 n=19 的 j=k, s=k-1 组做专属精修。"""
    best = list(sol)
    huge_jk = solver.k >= 7 or solver.num_targets >= 50_000
    direct_k6 = should_use_n19_jk_direct_lane(solver)
    best = _phase_n19_jk_multi_seed_pool_rebuild(solver, best)
    best = _phase_n19_jk_backbone_rebuild(solver, best)
    before = len(best)
    if not huge_jk:
        orbit_rounds = 2 if direct_k6 else 1
        for _ in range(orbit_rounds):
            orbit_candidate = _phase_n19_jk_orbit_cp_sat_refine(solver, best)
            if len(orbit_candidate) >= len(best):
                break
            best = orbit_candidate
    best = _phase_n19_jk_target_drop_refine(solver, best)
    best = _phase_n19_jk_destroy_repair_refine(solver, best)
    if solver.num_cands > 12_000 and not huge_jk and not direct_k6:
        best = _phase_n19_jk_large_pool_refine(solver, best)
    orbit_gain = before - len(best)
    if (not huge_jk) and solver.num_cands <= 12_000 and orbit_gain < max(10, before // 9):
        best = _phase_n19_jk_kminus1_domset_refine(solver, best)
    return best


def refine_n19_jk_small_s_solution(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if not is_n19_jk_small_s_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return sol
    if solver._deadline_at is None:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 8.0:
        return sol
    if not _ensure_n19_jk_sparse_overlap_tables(solver):
        return sol

    best = list(sol)
    best = _n19_jk_sparse_target_len_loop(solver, best)
    if solver.k == 5 and solver.s == 3:
        best = solver._phase_i_jk_cycle_module(best)
    elif solver.k == 4 and solver.s == 3:
        best = _n19_jk_sparse_target_len_loop(solver, best, budget_plan=(10.0, 12.0, 16.0, 20.0))
    elif solver.k == 6 and solver.s == 4:
        best = _n19_jk_sparse_target_len_loop(solver, best, budget_plan=(8.0, 12.0, 16.0))
    return best


def _rotate_mask(solver: "BaseCoveringDesignSolver", mask: int, shift: int) -> int:
    if shift % solver.n == 0:
        return mask
    out = 0
    for e in mask_to_elements(mask):
        out |= 1 << ((e + shift) % solver.n)
    return out


def _build_cyclic_orbits(solver: "BaseCoveringDesignSolver") -> list[list[int]]:
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for ci, mm in enumerate(solver.cand_masks):
        if ci in seen:
            continue
        mask = int(mm)
        orbit_set: set[int] = set()
        for shift in range(solver.n):
            rotated = _rotate_mask(solver, mask, shift)
            idx = solver._cand_index_map.get(rotated)
            if idx is not None:
                orbit_set.add(int(idx))
        if not orbit_set:
            orbit_set.add(ci)
        orbit = sorted(orbit_set)
        seen.update(orbit)
        orbits.append(orbit)
    return orbits


def _build_n19_jk_progression_anchor_indices(
    solver: "BaseCoveringDesignSolver",
) -> list[int]:
    steps = [1, 2, 3, 4, 5, 7, 8, 9]
    anchors: list[int] = []
    seen: set[int] = set()
    for step in steps:
        elems = sorted({(step * offset) % solver.n for offset in range(solver.k)})
        if len(elems) != solver.k:
            continue
        mask = 0
        for elem in elems:
            mask |= 1 << elem
        idx = solver._cand_index_map.get(mask)
        if idx is None:
            continue
        idx = int(idx)
        if idx in seen:
            continue
        anchors.append(idx)
        seen.add(idx)
    return anchors


def _build_n19_jk_seed_partial(
    solver: "BaseCoveringDesignSolver",
    anchor_idx: int,
    seed_len: int,
) -> list[int]:
    if seed_len <= 1:
        return [int(solver.cand_masks[anchor_idx])]

    selected_idx = [int(anchor_idx)]
    chosen = {int(anchor_idx)}
    element_freq = np.zeros(solver.n, dtype=np.int16)
    for elem in mask_to_elements(int(solver.cand_masks[anchor_idx])):
        element_freq[elem] += 1

    while len(selected_idx) < seed_len:
        overlap_score = np.zeros(solver.num_cands, dtype=np.int16)
        for ci in selected_idx:
            overlap_score += popcount_uint32(
                solver.cand_masks & np.uint32(solver.cand_masks[ci])
            ).astype(np.int16)

        best_idx: int | None = None
        best_score: tuple[int, int, int] | None = None
        for ci, mask_uint in enumerate(solver.cand_masks):
            if ci in chosen:
                continue
            elems = mask_to_elements(int(mask_uint))
            overlap_penalty = int(overlap_score[ci])
            freq_penalty = int(sum(int(element_freq[e]) for e in elems))
            score = (overlap_penalty, freq_penalty, ci)
            if best_score is None or score < best_score:
                best_score = score
                best_idx = ci

        if best_idx is None:
            break
        selected_idx.append(int(best_idx))
        chosen.add(int(best_idx))
        for elem in mask_to_elements(int(solver.cand_masks[best_idx])):
            element_freq[elem] += 1

    return [int(solver.cand_masks[ci]) for ci in selected_idx]


def _build_n19_jk_seed_profiles(
    solver: "BaseCoveringDesignSolver",
) -> list[object]:
    profiles = solver._build_attempt_profiles(4)
    tuned: list[object] = []
    for profile in profiles[:3]:
        tuned.append(
            replace(
                profile,
                name=f"{profile.name}-n19-seed",
                coverage_weight=max(0.92, float(profile.coverage_weight)),
                rarity_weight=max(0.38, float(profile.rarity_weight)),
                randomize=True,
                noise_scale=max(0.7, float(profile.noise_scale)),
                rcl_fraction=max(0.08, float(profile.rcl_fraction)),
                rcl_min_count=max(4, int(profile.rcl_min_count)),
                spread_tiebreak=True,
                spread_recent=max(32, int(profile.spread_recent)),
                spread_pool_cap=max(384, int(profile.spread_pool_cap)),
                top_k_scale=max(1.65, float(profile.top_k_scale)),
                destroy_repair_rounds=max(0, int(profile.destroy_repair_rounds)),
            )
        )
    return tuned


def _build_n19_jk_small_s_direct_profiles(
    solver: "BaseCoveringDesignSolver",
) -> list[object]:
    profiles = solver._build_attempt_profiles(5)
    tuned: list[object] = []
    for profile in profiles[:5]:
        tuned.append(
            replace(
                profile,
                name=f"{profile.name}-n19-small-direct",
                coverage_weight=max(0.96, float(profile.coverage_weight)),
                rarity_weight=max(0.42, float(profile.rarity_weight)),
                randomize=True,
                noise_scale=max(0.7, float(profile.noise_scale)),
                rcl_fraction=max(0.06, float(profile.rcl_fraction)),
                rcl_min_count=max(4, int(profile.rcl_min_count)),
                spread_tiebreak=True,
                spread_recent=max(28, int(profile.spread_recent)),
                spread_pool_cap=max(320, int(profile.spread_pool_cap)),
                top_k_scale=max(1.4, float(profile.top_k_scale)),
                destroy_repair_rounds=max(0, int(profile.destroy_repair_rounds)),
            )
        )
    return tuned


def _ensure_n19_jk_sparse_overlap_tables(
    solver: "BaseCoveringDesignSolver",
) -> bool:
    if not is_n19_jk_small_s_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return False
    if getattr(solver, "_n19_jk_sparse_tables_ready", False):
        return True

    cand_index = solver._cand_index_map
    cov: list[np.ndarray] = [np.empty(0, dtype=np.int32) for _ in range(solver.num_cands)]
    inv: list[list[int]] = [[] for _ in range(solver.num_targets)]
    max_swap = solver.k - solver.s

    for ci, mask_uint in enumerate(solver.cand_masks):
        mask = int(mask_uint)
        bits_in = mask_to_elements(mask)
        bit_in_set = set(bits_in)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        coverers = {ci}
        for swap in range(1, max_swap + 1):
            for rems in combinations(bits_in, swap):
                base = mask
                for rem in rems:
                    base &= ~(1 << rem)
                for adds in combinations(bits_out, swap):
                    mm = base
                    for add in adds:
                        mm |= 1 << add
                    cj = cand_index.get(mm)
                    if cj is not None:
                        coverers.add(int(cj))

        dom = np.array(sorted(coverers), dtype=np.int32)
        cov[ci] = dom
        for tj in dom.tolist():
            inv[int(tj)].append(ci)

    solver._cov_table = cov
    solver._inv_table = [np.array(row, dtype=np.int32) for row in inv]
    solver._base_weighted_scores = solver._build_base_weighted_scores()
    solver._n19_jk_sparse_tables_ready = True
    solver._report(
        "optimize",
        (
            "N19 jk-small sparse tables ready: "
            f"targets={solver.num_targets}, cands={solver.num_cands}"
        ),
    )
    return True


def _n19_jk_sparse_target_len_loop(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
    *,
    budget_plan: tuple[float, ...] = (8.0, 12.0, 16.0, 24.0),
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol

    best = list(sol)
    for budget in budget_plan:
        rem = solver._time_remaining_sec()
        if rem is None or rem < 2.5:
            break
        if len(best) <= 1:
            break
        improved = solver._phase_g_try_target_len(
            list(best),
            len(best) - 1,
            float(min(budget, max(2.5, rem - 0.8))),
        )
        if improved is None:
            continue
        if len(improved) < len(best):
            best = improved
            solver._report(
                "optimize",
                f"N19 jk-small target-len refined to {len(best)} groups",
            )
    return best


def _n19_jk_small_s_direct_polish(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    best = list(sol)
    if solver.k == 4 and solver.s == 3:
        best = _n19_jk_sparse_target_len_loop(
            solver,
            best,
            budget_plan=(8.0, 12.0, 16.0, 20.0, 24.0),
        )
        best = _n19_jk_sparse_target_len_loop(
            solver,
            best,
            budget_plan=(10.0, 12.0, 16.0, 20.0),
        )
        best = solver._phase_i_jk_cycle_module(best)
        return best
    if solver.k == 5 and solver.s == 3:
        best = _n19_jk_sparse_target_len_loop(
            solver,
            best,
            budget_plan=(8.0, 12.0, 16.0, 20.0, 24.0),
        )
        best = solver._phase_i_jk_cycle_module(best)
        best = _n19_jk_sparse_target_len_loop(
            solver,
            best,
            budget_plan=(4.0, 6.0, 8.0),
        )
        return best
    return best




def _phase_n19_jk_orbit_cp_sat_refine(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if cp_model is None:
        return sol
    if not is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 20:
        return sol
    if not solver._phase_c_has_time(5.0):
        return sol

    orbits = _build_cyclic_orbits(solver)
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
        bits_in = mask_to_elements(tmask)
        bit_in_set = set(bits_in)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        for rem in bits_in:
            rem_bit = 1 << rem
            base = tmask & (~rem_bit)
            for add in bits_out:
                mm = base | (1 << add)
                ci = cand_index.get(mm)
                if ci is not None:
                    cover_orbits.add(int(orbit_of[ci]))
        dom_orbits.append(sorted(cover_orbits))

    best_len = len(sol)
    ub = best_len - 1
    rem = solver._time_remaining_sec()
    if rem is None or rem < 3.0:
        return sol

    model = cp_model.CpModel()
    vars_y = [model.NewBoolVar(f"n19_yo_{i}") for i in range(len(orbits))]
    weighted = sum(int(orbit_sizes[i]) * vars_y[i] for i in range(len(orbits)))
    model.Add(weighted <= ub)
    for cover in dom_orbits:
        model.AddBoolOr([vars_y[i] for i in cover])
    model.Minimize(weighted)

    per_run = min(24.0, max(5.0, rem * 0.45))
    seeds = [1, 17, 29]
    if rem >= 24.0:
        seeds.extend([43, 59])

    best_masks = list(sol)
    for seed in seeds:
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 2.5:
            break
        cp = cp_model.CpSolver()
        cp.parameters.max_time_in_seconds = float(min(per_run, max(1.8, rem_seed - 0.8)))
        cp.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        cp.parameters.random_seed = seed
        cp.parameters.randomize_search = True
        status = cp.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            continue
        picked_orbits = [i for i in range(len(orbits)) if cp.Value(vars_y[i]) == 1]
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
        solver._report("optimize", f"N19 jk-orbit refined to {best_len} groups")
        break

    return best_masks


def _phase_n19_jk_backbone_rebuild(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if not is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return sol
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 60:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 10.0:
        return sol

    best = list(sol)
    order = solver._destroy_repair_order(best)
    if len(order) < 12:
        return best
    profiles = solver._build_attempt_profiles(5)
    if not profiles:
        return best

    # 保留“更难替代”的骨架块，释放其余空间让贪心重建。
    keep_plans = [0.72, 0.64, 0.56] if len(best) >= 400 else [0.78, 0.68, 0.58]
    misses = 0
    for ridx, keep_ratio in enumerate(keep_plans):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 4.2:
            break

        keep_count = max(8, min(len(best) - 6, int(len(best) * keep_ratio)))
        backbone_idx = set(order[-keep_count:])
        partial = [mask for idx, mask in enumerate(best) if idx in backbone_idx]
        if len(partial) >= len(best):
            continue

        # 目标不是盲目回到原长度，而是直接冲 len(best)-1。
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
                best_limit=target_limit + 2,
            )
            if fallback is None:
                misses += 1
                if misses >= 2:
                    break
                continue
            rebuilt = fallback

        candidate = solver._local_search(rebuilt)
        if len(candidate) < len(best):
            best = candidate
            misses = 0
            solver._report(
                "optimize",
                (
                    "N19 jk-backbone rebuild improved to "
                    f"{len(best)} groups (keep_ratio={keep_ratio:.2f})"
                ),
            )
            continue

        misses += 1
        if misses >= 2:
            break

    return best


def _phase_n19_jk_target_drop_refine(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if not is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return sol
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 24:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 6.0:
        return sol

    best = list(sol)
    profiles = solver._build_attempt_profiles(3)
    if not profiles:
        return best
    rounds = 3 if solver.num_targets >= 25_000 else 4
    misses = 0
    for ridx in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 3.5:
            break
        strategy = profiles[ridx % len(profiles)]
        candidate = solver._targeted_drop_one(best, strategy)
        if len(candidate) < len(best):
            best = candidate
            misses = 0
            solver._report("optimize", f"N19 jk-target-drop improved to {len(best)} groups")
            continue
        budget = float(min(14.0, max(3.0, rem * 0.22)))
        tightened = solver._phase_g_try_target_len(best, len(best) - 1, budget)
        if tightened is not None and len(tightened) < len(best):
            best = tightened
            misses = 0
            solver._report("optimize", f"N19 jk-target-len improved to {len(best)} groups")
            continue
        misses += 1
        if misses >= 2:
            break
    return best


def _phase_n19_jk_destroy_repair_refine(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if not is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return sol
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 40:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 8.0:
        return sol

    best = list(sol)
    profiles = solver._build_attempt_profiles(4)
    if not profiles:
        return best
    rounds = 2 if solver.num_targets >= 25_000 else 3
    for ridx in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 4.0:
            break
        strategy = profiles[ridx % len(profiles)]
        candidate = solver._destroy_repair(best, strategy, rounds=1)
        if len(candidate) < len(best):
            best = candidate
            solver._report("optimize", f"N19 jk-destroy-repair improved to {len(best)} groups")
    return best


def _phase_n19_jk_kminus1_domset_refine(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if cp_model is None:
        return sol
    if not is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 12:
        return sol
    if solver.num_cands > 12_000:
        return sol
    if not solver._phase_c_has_time(4.0):
        return sol

    cand_index = solver._cand_index_map
    selected_idx = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_idx) != len(sol):
        return sol

    dom_lists: list[list[int]] = []
    for mask_uint in solver.cand_masks:
        tmask = int(mask_uint)
        coverers = {cand_index[tmask]}
        bits_in = mask_to_elements(tmask)
        bit_in_set = set(bits_in)
        bits_out = [e for e in range(solver.n) if e not in bit_in_set]
        for rem in bits_in:
            rem_bit = 1 << rem
            base = tmask & (~rem_bit)
            for add in bits_out:
                mm = base | (1 << add)
                ci = cand_index.get(mm)
                if ci is not None:
                    coverers.add(ci)
        dom_lists.append(sorted(coverers))

    best_masks = list(sol)
    best_len = len(best_masks)
    ub = best_len - 1
    miss = 0
    while ub >= 1:
        rem = solver._time_remaining_sec()
        if rem is None or rem < 2.8:
            break
        if miss >= 2:
            break

        model = cp_model.CpModel()
        vars_x = [model.NewBoolVar(f"n19_xk_{i}") for i in range(solver.num_cands)]
        model.Add(sum(vars_x) <= ub)
        for dom in dom_lists:
            model.AddBoolOr([vars_x[i] for i in dom])

        if miss == 0 and selected_idx:
            hint_keep = max(8, int(len(selected_idx) * 0.7))
            hint_idx = (
                random.sample(selected_idx, hint_keep)
                if hint_keep < len(selected_idx)
                else list(selected_idx)
            )
            for ci in hint_idx:
                model.AddHint(vars_x[ci], 1)

        seeds = [1, 17, 29]
        if rem >= 22.0:
            seeds.extend([43, 59])
        per_run = max(2.2, min(18.0, (rem * 0.72) / max(1, len(seeds))))
        if miss > 0:
            per_run = min(24.0, per_run * 1.35)

        found = False
        for seed in seeds:
            rem_seed = solver._time_remaining_sec()
            if rem_seed is None or rem_seed < 2.0:
                break
            cp = cp_model.CpSolver()
            cp.parameters.max_time_in_seconds = float(min(per_run, max(1.3, rem_seed - 0.6)))
            cp.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            cp.parameters.random_seed = seed
            cp.parameters.randomize_search = True
            status = cp.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                continue

            picked = [i for i in range(solver.num_cands) if cp.Value(vars_x[i]) == 1]
            if len(picked) >= best_len:
                continue
            candidate = [int(solver.cand_masks[i]) for i in picked]
            if not solver._verify(candidate):
                continue

            best_masks = candidate
            best_len = len(best_masks)
            selected_idx = picked
            ub = best_len - 1
            miss = 0
            found = True
            solver._report("optimize", f"N19 jk-domset refined to {best_len} groups")
            break

        if not found:
            miss += 1
            if miss >= 3:
                break

    return best_masks


def _dominating_indices_for_candidate_index(
    solver: "BaseCoveringDesignSolver",
    cand_index: dict[int, int],
    ci: int,
) -> list[int]:
    tmask = int(solver.cand_masks[ci])
    coverers = {ci}
    bits_in = mask_to_elements(tmask)
    bit_in_set = set(bits_in)
    bits_out = [e for e in range(solver.n) if e not in bit_in_set]
    for rem in bits_in:
        rem_bit = 1 << rem
        base = tmask & (~rem_bit)
        for add in bits_out:
            mm = base | (1 << add)
            cj = cand_index.get(mm)
            if cj is not None:
                coverers.add(int(cj))
    return sorted(coverers)


def _build_large_pool_candidate_indices(
    solver: "BaseCoveringDesignSolver",
    selected_idx: list[int],
) -> tuple[list[int], np.ndarray]:
    cand_index = solver._cand_index_map
    support = np.zeros(solver.num_targets, dtype=np.int16)
    dom_cache: dict[int, list[int]] = {}
    for ci in selected_idx:
        dom = _dominating_indices_for_candidate_index(solver, cand_index, ci)
        dom_cache[ci] = dom
        support[np.array(dom, dtype=np.int32)] += 1

    frag_score: list[tuple[float, int]] = []
    for ci in selected_idx:
        dom = dom_cache[ci]
        dom_arr = np.array(dom, dtype=np.int32)
        fragile = dom_arr[support[dom_arr] <= 2]
        score = float(solver._target_weights[fragile].sum()) if len(fragile) else 0.0
        frag_score.append((score, ci))
    frag_score.sort(reverse=True)

    pool_set: set[int] = set(selected_idx)
    bonus = np.zeros(solver.num_cands, dtype=np.float64)
    anchor_cap = 72 if len(selected_idx) >= 800 else 48
    anchors = [ci for _, ci in frag_score[:anchor_cap]]
    if len(selected_idx) > anchor_cap:
        random_part = random.sample(selected_idx, min(18, len(selected_idx) - anchor_cap))
        anchors.extend(random_part)

    fragile_targets = np.flatnonzero(support <= 1)
    if len(fragile_targets) > 256:
        weights = solver._target_weights[fragile_targets]
        keep = np.argpartition(weights, -256)[-256:]
        fragile_targets = fragile_targets[keep]

    for ti in fragile_targets.tolist():
        ti = int(ti)
        dom = _dominating_indices_for_candidate_index(solver, cand_index, ti)
        mult = 5.0 if support[ti] <= 0 else 2.6
        bonus[np.array(dom, dtype=np.int32)] += float(solver._target_weights[ti] * mult)

    for score, ci in frag_score[:anchor_cap]:
        dom = dom_cache.get(ci)
        if dom is None:
            dom = _dominating_indices_for_candidate_index(solver, cand_index, ci)
        if not dom:
            continue
        bonus[np.array(dom, dtype=np.int32)] += max(0.15, float(score) * 0.08)

    selected_arr = np.array(selected_idx, dtype=np.int32)
    bonus[selected_arr] += 0.35

    if solver._target_weights is not None:
        base_take = min(solver.num_cands, 768 if solver.num_targets >= 50_000 else 512)
        top_base = np.argpartition(solver._target_weights, -base_take)[-base_take:]
        bonus[top_base] += 0.25

    max_pool = 8800 if solver.num_targets >= 50_000 else 6200
    if len(pool_set) >= max_pool:
        pool_idx = sorted(pool_set)
        return pool_idx, bonus[np.array(pool_idx, dtype=np.int32)]

    extra_slots = max_pool - len(pool_set)
    ranked = np.argsort(bonus)[::-1]
    added = 0
    for dj in ranked.tolist():
        if dj in pool_set:
            continue
        pool_set.add(int(dj))
        added += 1
        if added >= extra_slots:
            break
    pool_idx = sorted(pool_set)
    return pool_idx, bonus[np.array(pool_idx, dtype=np.int32)]


def _solve_n19_jk_pool_model(
    solver: "BaseCoveringDesignSolver",
    pool_idx: list[int],
    pool_bonus: np.ndarray,
    selected_idx: list[int],
    best_len: int,
    *,
    tag: str,
) -> list[int] | None:
    if cp_model is None:
        return None
    if len(pool_idx) <= best_len:
        return None

    cand_index = solver._cand_index_map
    pool_map = {ci: pos for pos, ci in enumerate(pool_idx)}
    dom_lists_pool: list[list[int]] = []
    for ti in range(solver.num_targets):
        dom = _dominating_indices_for_candidate_index(solver, cand_index, ti)
        restricted = [pool_map[cj] for cj in dom if cj in pool_map]
        if not restricted:
            return None
        dom_lists_pool.append(restricted)

    ub = best_len - 1
    misses = 0
    best_masks: list[int] | None = None
    while ub >= 1:
        rem = solver._time_remaining_sec()
        if rem is None or rem < 3.0:
            break
        if misses >= 2:
            break

        model = cp_model.CpModel()
        vars_x = [model.NewBoolVar(f"n19_pool_{tag}_{i}") for i in range(len(pool_idx))]
        model.Add(sum(vars_x) <= ub)
        for dom in dom_lists_pool:
            model.AddBoolOr([vars_x[pos] for pos in dom])

        scaled_bonus = np.maximum(0, np.round(pool_bonus * 100.0)).astype(np.int64)
        if int(np.max(scaled_bonus)) > 0:
            model.Maximize(sum(int(scaled_bonus[i]) * vars_x[i] for i in range(len(pool_idx))))

        hint_keep = max(20, int(len(selected_idx) * 0.68))
        hint_idx = (
            random.sample(selected_idx, hint_keep)
            if hint_keep < len(selected_idx)
            else list(selected_idx)
        )
        for ci in hint_idx:
            pos = pool_map.get(ci)
            if pos is not None:
                model.AddHint(vars_x[pos], 1)

        seeds = [1, 17, 29]
        if rem >= 26.0:
            seeds.extend([43, 59])
        per_run = max(2.4, min(16.0, (rem * 0.62) / max(1, len(seeds))))
        if misses > 0:
            per_run = min(20.0, per_run * 1.2)

        found = False
        for seed in seeds:
            rem_seed = solver._time_remaining_sec()
            if rem_seed is None or rem_seed < 2.2:
                break
            cp = cp_model.CpSolver()
            cp.parameters.max_time_in_seconds = float(min(per_run, max(1.5, rem_seed - 0.7)))
            cp.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            cp.parameters.random_seed = seed
            cp.parameters.randomize_search = True
            status = cp.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                continue

            picked = [pool_idx[i] for i in range(len(pool_idx)) if cp.Value(vars_x[i]) == 1]
            if len(picked) >= best_len:
                continue
            candidate = [int(solver.cand_masks[i]) for i in picked]
            candidate = solver._local_search(candidate)
            if len(candidate) >= best_len:
                continue
            if not solver._verify(candidate):
                continue
            best_masks = candidate
            best_len = len(best_masks)
            ub = best_len - 1
            misses = 0
            found = True
            solver._report(
                "optimize",
                f"N19 jk-{tag} refined to {best_len} groups (pool={len(pool_idx)})",
            )
            break

        if not found:
            misses += 1
            if misses >= 3:
                break

    return best_masks


def _phase_n19_jk_multi_seed_pool_rebuild(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if not is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return sol
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 120:
        return sol
    if solver.k >= 7 or solver.num_targets >= 50_000:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 16.0:
        return sol

    best = list(sol)
    anchors = _build_n19_jk_progression_anchor_indices(solver)
    profiles = _build_n19_jk_seed_profiles(solver)
    if not anchors or not profiles:
        return best

    seed_len = 4 if solver.k >= 6 else 3
    max_runs = 4 if solver.num_targets >= 20_000 else 6
    fresh_solutions: list[list[int]] = [list(best)]
    run_count = 0
    for anchor_idx in anchors:
        if run_count >= max_runs:
            break
        for profile in profiles[:2]:
            rem = solver._time_remaining_sec()
            if rem is None or rem < 6.0 or run_count >= max_runs:
                break

            partial = _build_n19_jk_seed_partial(solver, anchor_idx, seed_len)
            rebuilt, complete, _ = solver._greedy(
                profile,
                partial=partial,
                best_limit=len(best) + 24,
            )
            if not complete:
                fallback = solver._fast_complete_partial_solution(
                    partial,
                    best_limit=len(best) + 32,
                )
                if fallback is None:
                    run_count += 1
                    continue
                rebuilt = fallback

            candidate = solver._local_search(rebuilt)
            if not solver._verify(candidate):
                run_count += 1
                continue

            fresh_solutions.append(candidate)
            if len(candidate) < len(best):
                best = candidate
                solver._report(
                    "optimize",
                    (
                        "N19 jk-multi-seed greedy improved to "
                        f"{len(best)} groups via {profile.name}"
                    ),
                )
            run_count += 1

    if len(fresh_solutions) <= 1:
        return best

    selected_idx: list[int] = []
    seen_idx: set[int] = set()
    for masks in sorted(fresh_solutions, key=len)[: min(4, len(fresh_solutions))]:
        for mask in masks:
            ci = solver._cand_index_map.get(mask)
            if ci is None or int(ci) in seen_idx:
                continue
            selected_idx.append(int(ci))
            seen_idx.add(int(ci))

    if len(selected_idx) <= len(best):
        return best

    pool_idx, pool_bonus = _build_large_pool_candidate_indices(solver, selected_idx)
    candidate = _solve_n19_jk_pool_model(
        solver,
        pool_idx,
        pool_bonus,
        selected_idx,
        len(best),
        tag="seed-pool",
    )
    if candidate is not None and len(candidate) < len(best):
        return candidate
    return best


def _phase_n19_jk_large_pool_refine(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if cp_model is None:
        return sol
    if not is_n19_jk_target_case(n=solver.n, k=solver.k, j=solver.j, s=solver.s):
        return sol
    if solver._deadline_at is None:
        return sol
    if solver.num_cands <= 12_000:
        return sol
    if len(sol) < 40:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 14.0:
        return sol
    if not solver._phase_c_has_time(8.0):
        return sol

    cand_index = solver._cand_index_map
    selected_idx = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_idx) != len(sol):
        return sol

    pool_idx, pool_bonus = _build_large_pool_candidate_indices(solver, selected_idx)
    if len(pool_idx) <= len(selected_idx):
        return sol

    pool_map = {ci: pos for pos, ci in enumerate(pool_idx)}
    dom_lists_pool: list[list[int]] = []
    for ti in range(solver.num_targets):
        dom = _dominating_indices_for_candidate_index(solver, cand_index, ti)
        restricted = [pool_map[cj] for cj in dom if cj in pool_map]
        if not restricted:
            return sol
        dom_lists_pool.append(restricted)

    best_masks = list(sol)
    best_len = len(best_masks)
    ub = best_len - 1
    misses = 0
    while ub >= 1:
        rem = solver._time_remaining_sec()
        if rem is None or rem < 3.0:
            break
        if misses >= 2:
            break

        model = cp_model.CpModel()
        vars_x = [model.NewBoolVar(f"n19_lp_{i}") for i in range(len(pool_idx))]
        model.Add(sum(vars_x) <= ub)
        for dom in dom_lists_pool:
            model.AddBoolOr([vars_x[pos] for pos in dom])

        scaled_bonus = np.maximum(0, np.round(pool_bonus * 100.0)).astype(np.int64)
        if int(np.max(scaled_bonus)) > 0:
            model.Maximize(sum(int(scaled_bonus[i]) * vars_x[i] for i in range(len(pool_idx))))

        if misses == 0:
            hint_keep = max(24, int(len(selected_idx) * 0.72))
            hint_idx = (
                random.sample(selected_idx, hint_keep)
                if hint_keep < len(selected_idx)
                else list(selected_idx)
            )
            for ci in hint_idx:
                pos = pool_map.get(ci)
                if pos is not None:
                    model.AddHint(vars_x[pos], 1)

        seeds = [1, 17, 29]
        if rem >= 26.0:
            seeds.extend([43, 59])
        per_run = max(2.4, min(16.0, (rem * 0.66) / max(1, len(seeds))))
        if misses > 0:
            per_run = min(20.0, per_run * 1.25)

        found = False
        for seed in seeds:
            rem_seed = solver._time_remaining_sec()
            if rem_seed is None or rem_seed < 2.2:
                break
            cp = cp_model.CpSolver()
            cp.parameters.max_time_in_seconds = float(min(per_run, max(1.5, rem_seed - 0.7)))
            cp.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            cp.parameters.random_seed = seed
            cp.parameters.randomize_search = True
            status = cp.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                continue

            picked = [pool_idx[i] for i in range(len(pool_idx)) if cp.Value(vars_x[i]) == 1]
            if len(picked) >= best_len:
                continue
            candidate = [int(solver.cand_masks[i]) for i in picked]
            candidate = solver._local_search(candidate)
            if len(candidate) >= best_len:
                continue
            if not solver._verify(candidate):
                continue

            best_masks = candidate
            best_len = len(best_masks)
            ub = best_len - 1
            misses = 0
            found = True
            solver._report(
                "optimize",
                (
                    "N19 jk-large-pool refined to "
                    f"{best_len} groups (pool={len(pool_idx)})"
                ),
            )
            break

        if not found:
            misses += 1
            if misses >= 3:
                break

    return best_masks
