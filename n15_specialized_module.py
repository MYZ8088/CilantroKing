from __future__ import annotations

import math
import random
from typing import Any, Callable


_SPECIAL_CASE_BASELINES: dict[tuple[int, int, int, int], int] = {
    (13, 6, 6, 5): 61,
    (13, 7, 7, 6): 61,
    (14, 5, 5, 4): 69,
    (14, 6, 4, 4): 80,
    (14, 6, 6, 5): 98,
    (14, 7, 5, 5): 138,
    (14, 7, 6, 6): 501,
    (14, 7, 7, 6): 100,
    (15, 6, 4, 4): 117,
    (15, 6, 5, 4): 40,
    (15, 6, 6, 5): 142,
    (15, 7, 5, 5): 189,
    (15, 7, 6, 5): 58,
    (15, 7, 6, 6): 817,
    (15, 7, 7, 6): 180,
}


def is_n15_special_case(n: int, k: int, j: int, s: int) -> bool:
    return (int(n), int(k), int(j), int(s)) in _SPECIAL_CASE_BASELINES


def _family_of(n: int, k: int, j: int, s: int) -> str:
    if s == j:
        return "containment_s_eq_j"
    if j == k:
        return "j_eq_k_noncontain_medium_n"
    return "general_noncontain"


def _target_limit_for_compliance(baseline: int) -> int:
    return int(math.floor(float(baseline) * 1.10 + 1e-9))


def _log(solver: Any, message: str) -> None:
    report = getattr(solver, "_report", None)
    if callable(report):
        report("optimize", message)


def _has_time(solver: Any, minimum_sec: float) -> bool:
    remaining = solver._time_remaining_sec()
    if remaining is None:
        return False
    return remaining >= minimum_sec


def _note_legal(solver: Any) -> None:
    note_fn = getattr(solver, "_note_legal_solution", None)
    if callable(note_fn):
        note_fn()


def _accept_if_better(solver: Any, best: list[int], candidate: list[int] | None) -> list[int]:
    if candidate is None:
        return best
    if len(candidate) >= len(best):
        return best
    _note_legal(solver)
    return list(candidate)


def _build_family_ops(
    solver: Any,
    family: str,
) -> list[tuple[str, Callable[[list[int]], list[int]]]]:
    if family == "j_eq_k_noncontain_medium_n":
        return [
            ("jk-cycle", lambda cur: solver._phase_i_jk_cycle_module(cur)),
            ("h-refine", lambda cur: solver._phase_h_nlt16_cp_sat_refine(cur)),
            ("jk-orbit", lambda cur: solver._phase_k_jk_orbit_cp_sat_refine(cur)),
            ("i-full-hard", lambda cur: solver._phase_i_full_cp_sat_module(cur, hard_case=True)),
            ("jk-domset", lambda cur: solver._phase_k_jk_kminus1_domset_refine(cur)),
        ]
    if family == "containment_s_eq_j":
        hard_case = bool(solver.k >= 6 and solver.n >= 14)
        return [
            ("contain-cycle", lambda cur: solver._phase_i_containment_cycle_module(cur)),
            ("h-refine", lambda cur: solver._phase_h_nlt16_cp_sat_refine(cur)),
            ("contain-orbit", lambda cur: solver._phase_k_containment_orbit_cp_sat_refine(cur)),
            ("contain-sat", lambda cur: solver._phase_k_containment_iterative_sat_refine(cur)),
            ("i-full", lambda cur: solver._phase_i_full_cp_sat_module(cur, hard_case=hard_case)),
        ]
    return [
        ("general-cycle", lambda cur: solver._phase_i_general_small_module(cur)),
        ("h-refine", lambda cur: solver._phase_h_nlt16_cp_sat_refine(cur)),
        ("general-sat", lambda cur: solver._phase_k_general_iterative_sat_refine(cur)),
        ("i-full", lambda cur: solver._phase_i_full_cp_sat_module(cur, hard_case=False)),
    ]


def _run_family_sequence(
    solver: Any,
    best: list[int],
    family: str,
    *,
    max_rounds: int,
) -> list[int]:
    ops = _build_family_ops(solver, family)
    out = list(best)
    for _ in range(max_rounds):
        if not _has_time(solver, 2.0):
            break
        round_improved = False
        for name, op in ops:
            if not _has_time(solver, 1.6):
                break
            prev_len = len(out)
            try:
                candidate = op(out)
            except Exception:
                continue
            out = _accept_if_better(solver, out, candidate)
            if len(out) < prev_len:
                round_improved = True
                _log(solver, f"N15 module {name} improved to {len(out)} groups")
                if len(out) <= 1:
                    return out
        if not round_improved:
            break
    return out


def _descent_budget(remaining_sec: float, family: str, gap: int, attempts: int) -> float:
    if family == "j_eq_k_noncontain_medium_n":
        ratio = 0.30 if gap >= 5 else 0.24
        cap = 24.0 if gap >= 5 else 16.0
    elif family == "containment_s_eq_j":
        ratio = 0.34 if gap >= 5 else 0.26
        cap = 28.0 if gap >= 5 else 20.0
    else:
        ratio = 0.26 if gap >= 4 else 0.20
        cap = 18.0 if gap >= 4 else 12.0
    total = min(cap, max(2.0, remaining_sec * ratio))
    return max(1.2, total / max(1, attempts))


def _aggressive_descent(
    solver: Any,
    best: list[int],
    *,
    target_len: int,
    family: str,
) -> list[int]:
    out = list(best)
    misses = 0
    rounds = 0
    while len(out) > target_len and rounds < 12:
        remaining = solver._time_remaining_sec()
        if remaining is None or remaining < 2.8:
            break

        gap = len(out) - target_len
        if gap >= 10:
            drop = 3
        elif gap >= 4:
            drop = 2
        else:
            drop = 1
        trial_target = len(out) - drop
        attempts = 4 if gap <= 3 else 3
        per_try_budget = _descent_budget(float(remaining), family, gap, attempts)

        improved: list[int] | None = None
        for attempt in range(attempts):
            if not _has_time(solver, 1.6):
                break
            start_masks = list(out)
            if attempt > 0:
                random.shuffle(start_masks)
            candidate = solver._phase_g_try_target_len(
                start_masks,
                trial_target,
                per_try_budget,
            )
            if candidate is None and drop > 1:
                candidate = solver._phase_g_try_target_len(
                    start_masks,
                    len(out) - 1,
                    max(1.0, per_try_budget * 0.82),
                )
            candidate = _accept_if_better(solver, out, candidate)
            if len(candidate) < len(out):
                improved = candidate
                break

        if improved is None:
            misses += 1
            if misses >= 3:
                break
        else:
            out = improved
            misses = 0
            _log(
                solver,
                f"N15 module descent improved to {len(out)} groups (target<={target_len})",
            )
            if len(out) > target_len and _has_time(solver, 2.0):
                out = _run_family_sequence(solver, out, family, max_rounds=1)
        rounds += 1
    return out


def _threshold_closer(
    solver: Any,
    best: list[int],
    *,
    target_len: int,
    family: str,
) -> list[int]:
    out = list(best)
    misses = 0
    while len(out) > target_len and misses < 4:
        if not _has_time(solver, 2.2):
            break
        remaining = solver._time_remaining_sec()
        if remaining is None:
            break

        goal = max(target_len, len(out) - 1)
        gap = len(out) - target_len
        if family == "containment_s_eq_j" and gap <= 2:
            per_try_budget = max(1.8, min(10.0, float(remaining) * 0.34))
            tries = 4
        elif family == "j_eq_k_noncontain_medium_n" and gap <= 2:
            per_try_budget = max(1.6, min(9.0, float(remaining) * 0.30))
            tries = 4
        else:
            per_try_budget = max(1.0, min(8.0, float(remaining) * 0.16))
            tries = 3
        improved: list[int] | None = None
        for _ in range(tries):
            if not _has_time(solver, 1.4):
                break
            start_masks = list(out)
            random.shuffle(start_masks)
            candidate = solver._phase_g_try_target_len(
                start_masks,
                goal,
                per_try_budget,
            )
            candidate = _accept_if_better(solver, out, candidate)
            if len(candidate) < len(out):
                improved = candidate
                break

        if improved is not None:
            out = improved
            misses = 0
            _log(solver, f"N15 module threshold-closer improved to {len(out)} groups")
            continue

        prev_len = len(out)
        out = _run_family_sequence(solver, out, family, max_rounds=1)
        if len(out) < prev_len:
            continue
        misses += 1
    return out


def run_n15_specialized_module(solver: Any, sol: list[int]) -> list[int]:
    key = (int(solver.n), int(solver.k), int(solver.j), int(solver.s))
    baseline = _SPECIAL_CASE_BASELINES.get(key)
    if baseline is None:
        return sol
    if solver._deadline_at is None:
        return sol
    if solver._cov_table is None or solver._inv_table is None:
        return sol

    best = list(sol)
    target_len = _target_limit_for_compliance(baseline)
    if len(best) <= target_len:
        return best

    family = _family_of(*key)
    _log(
        solver,
        (
            "N15 special module start: "
            f"L({key[0]},{key[1]},{key[2]},{key[3]}), "
            f"current={len(best)}, target<={target_len}"
        ),
    )

    best = _aggressive_descent(
        solver,
        best,
        target_len=target_len,
        family=family,
    )
    if len(best) > target_len:
        best = _run_family_sequence(solver, best, family, max_rounds=2)
    if len(best) > target_len:
        best = _threshold_closer(
            solver,
            best,
            target_len=target_len,
            family=family,
        )

    if len(best) <= target_len:
        _log(
            solver,
            (
                "N15 special module reached compliance target: "
                f"{len(best)}/{target_len}"
            ),
        )
    else:
        _log(
            solver,
            (
                "N15 special module exit without full compliance: "
                f"{len(best)}/{target_len}"
            ),
        )
    return best
