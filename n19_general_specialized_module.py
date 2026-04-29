from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from solver import CoveringDesignSolver as BaseCoveringDesignSolver


def is_n19_general_case(*, n: int, j: int, k: int, s: int) -> bool:
    return int(n) == 19 and int(s) != int(j) and int(j) != int(k)


def refine_n19_general_solution(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
    *,
    cluster: str,
) -> list[int]:
    best = list(sol)
    best = _n19_general_target_drop(
        solver,
        best,
        aggressive=(cluster == "general_sparse_overlap"),
    )
    if cluster == "general_large_overlap":
        best = _n19_general_destroy_repair(solver, best)
    best = solver._phase_k_general_iterative_sat_refine(best)
    return best


def _n19_general_target_drop(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
    *,
    aggressive: bool,
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 8:
        return sol
    if not solver._phase_c_has_time(2.4):
        return sol

    best = list(sol)
    misses = 0
    rounds = 6 if aggressive else 4
    for _ in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 2.0:
            break
        target_drop = 2 if aggressive and len(best) <= 40 else 1
        target_len = len(best) - target_drop
        if target_len < 1:
            break
        budget = float(min(12.0, max(2.0, rem * 0.28)))
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
            solver._report("optimize", f"N19 general target-drop refined to {len(best)} groups")
        else:
            misses += 1
            if misses >= 3:
                break
    return best


def _n19_general_destroy_repair(
    solver: "BaseCoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if len(sol) < 16:
        return sol
    rem0 = solver._time_remaining_sec()
    if rem0 is None or rem0 < 6.0:
        return sol

    best = list(sol)
    profiles = solver._build_attempt_profiles(3)
    if not profiles:
        return best
    rounds = 2
    for ridx in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 3.5:
            break
        strategy = profiles[ridx % len(profiles)]
        candidate = solver._destroy_repair(best, strategy, rounds=1)
        if len(candidate) < len(best):
            best = candidate
            solver._report("optimize", f"N19 general destroy-repair improved to {len(best)} groups")
    return best
