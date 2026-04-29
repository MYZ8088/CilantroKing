from __future__ import annotations

import os
import random
from typing import TYPE_CHECKING

import numpy as np

from solver import cp_model
from solver import mask_to_elements

if TYPE_CHECKING:
    from solver import CoveringDesignSolver as BaseCoveringDesignSolver


def is_n19_containment_case(*, n: int, j: int, s: int) -> bool:
    return int(n) == 19 and int(s) == int(j)


def refine_n19_containment_solution(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
    *,
    cluster: str,
) -> list[int]:
    best = list(sol)
    if cluster in {"containment_low_j", "containment_balanced"}:
        best = _n19_try_target_drop(solver, best, aggressive=(cluster == "containment_low_j"))
    if cluster in {"containment_balanced", "containment_large_k"}:
        best = _phase_n19_containment_orbit_cp_sat_refine(solver, best)
    if cluster == "containment_large_k" or (
        cluster == "containment_balanced" and solver.num_cands > 15_000
    ):
        best = _phase_n19_containment_large_pool_sat_refine(solver, best)
    best = solver._phase_k_containment_iterative_sat_refine(best)
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


def _n19_try_target_drop(
    solver: "BaseCoveringDesignSolver",
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
    if not solver._phase_c_has_time(2.6):
        return sol

    best = list(sol)
    rounds = 6 if aggressive else 4
    target_drop = 2 if aggressive and len(sol) <= 180 else 1
    misses = 0
    for _ in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 2.2:
            break
        target_len = len(best) - target_drop
        if target_len < 1:
            break
        budget = float(min(12.0, max(2.2, rem * 0.30)))
        start_masks = list(best)
        if misses > 0:
            random.shuffle(start_masks)
        improved = solver._phase_g_try_target_len(start_masks, target_len, budget)
        if improved is None and target_drop == 2:
            improved = solver._phase_g_try_target_len(start_masks, len(best) - 1, budget)
        if improved is None:
            misses += 1
            if misses >= 3:
                break
            continue
        if len(improved) < len(best):
            best = improved
            misses = 0
            solver._report("optimize", f"N19 containment target-drop refined to {len(best)} groups")
        else:
            misses += 1
            if misses >= 3:
                break
    return best


def _phase_n19_containment_orbit_cp_sat_refine(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if cp_model is None:
        return sol
    if not is_n19_containment_case(n=solver.n, j=solver.j, s=solver.s):
        return sol
    if solver._inv_table is None or solver._deadline_at is None:
        return sol
    if len(sol) < 24:
        return sol
    if not solver._phase_c_has_time(3.8):
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
    vars_y = [model.NewBoolVar(f"n19_yc_{i}") for i in range(len(orbits))]
    weighted = sum(int(orbit_sizes[i]) * vars_y[i] for i in range(len(orbits)))
    model.Add(weighted <= ub)
    for cover in target_cover_orbits:
        model.AddBoolOr([vars_y[i] for i in cover])
    model.Minimize(weighted)

    per_run = min(18.0, max(3.5, rem * 0.42))
    seeds = [1, 17, 29]
    if rem >= 24.0:
        seeds.extend([43, 59])

    best_masks = list(sol)
    for seed in seeds:
        rem_seed = solver._time_remaining_sec()
        if rem_seed is None or rem_seed < 2.0:
            break
        cp = cp_model.CpSolver()
        cp.parameters.max_time_in_seconds = float(min(per_run, max(1.5, rem_seed - 0.6)))
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
        solver._report("optimize", f"N19 containment-orbit refined to {best_len} groups")
        break

    return best_masks


def _phase_n19_containment_large_pool_sat_refine(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if cp_model is None:
        return sol
    if not is_n19_containment_case(n=solver.n, j=solver.j, s=solver.s):
        return sol
    if solver._inv_table is None or solver._cov_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if solver.num_cands <= 12_000:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 10.0:
        return sol
    if len(sol) < 24:
        return sol

    cand_index = solver._cand_index_map
    selected_idx = [cand_index[m] for m in sol if m in cand_index]
    if len(selected_idx) != len(sol):
        return sol

    counts = np.zeros(solver.num_targets, dtype=np.int16)
    for ci in selected_idx:
        counts[solver._cov_table[ci]] += 1

    fragile_targets = np.flatnonzero(counts <= 1)
    if len(fragile_targets) < 16:
        fragile_targets = np.flatnonzero(counts <= 2)
    if len(fragile_targets) == 0:
        return sol
    if len(fragile_targets) > 320:
        weights = solver._target_weights[fragile_targets]
        keep = np.argpartition(weights, -320)[-320:]
        fragile_targets = fragile_targets[keep]

    bonus = np.zeros(solver.num_cands, dtype=np.float64)
    for ti in fragile_targets.tolist():
        ti = int(ti)
        mult = 5.0 if counts[ti] <= 0 else 2.8
        bonus[solver._inv_table[ti]] += float(solver._target_weights[ti] * mult)
    bonus[np.array(selected_idx, dtype=np.int32)] += 0.4

    pool_set = set(selected_idx)
    max_pool = 9000 if solver.num_cands >= 50_000 else 6500
    ranked = np.argsort(bonus)[::-1]
    for ci in ranked.tolist():
        if ci in pool_set:
            continue
        pool_set.add(int(ci))
        if len(pool_set) >= max_pool:
            break
    pool_idx = sorted(pool_set)
    if len(pool_idx) <= len(selected_idx):
        return sol

    pool_map = {ci: pos for pos, ci in enumerate(pool_idx)}
    cover_lists_pool: list[list[int]] = []
    for ti in range(solver.num_targets):
        restricted = [pool_map[int(ci)] for ci in solver._inv_table[ti] if int(ci) in pool_map]
        if not restricted:
            return sol
        cover_lists_pool.append(restricted)

    pool_bonus = bonus[np.array(pool_idx, dtype=np.int32)]
    best_masks = list(sol)
    best_len = len(best_masks)
    ub = best_len - 1
    misses = 0
    while ub >= 1:
        rem = solver._time_remaining_sec()
        if rem is None or rem < 2.8:
            break
        if misses >= 2:
            break

        model = cp_model.CpModel()
        vars_x = [model.NewBoolVar(f"n19_cp_{i}") for i in range(len(pool_idx))]
        model.Add(sum(vars_x) <= ub)
        for cover in cover_lists_pool:
            model.AddBoolOr([vars_x[pos] for pos in cover])

        scaled_bonus = np.maximum(0, np.round(pool_bonus * 100.0)).astype(np.int64)
        if int(np.max(scaled_bonus)) > 0:
            model.Maximize(sum(int(scaled_bonus[i]) * vars_x[i] for i in range(len(pool_idx))))

        if misses == 0:
            hint_keep = max(18, int(len(selected_idx) * 0.70))
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
        if rem >= 24.0:
            seeds.extend([43, 59])
        per_run = max(2.2, min(16.0, (rem * 0.62) / max(1, len(seeds))))
        if misses > 0:
            per_run = min(20.0, per_run * 1.25)

        found = False
        for seed in seeds:
            rem_seed = solver._time_remaining_sec()
            if rem_seed is None or rem_seed < 2.0:
                break
            cp = cp_model.CpSolver()
            cp.parameters.max_time_in_seconds = float(min(per_run, max(1.4, rem_seed - 0.6)))
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
                f"N19 containment-large-pool refined to {best_len} groups (pool={len(pool_idx)})",
            )
            break

        if not found:
            misses += 1
            if misses >= 3:
                break

    return best_masks
