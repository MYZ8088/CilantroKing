from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:  # pragma: no cover
    from solver_n16_isolated import CoveringDesignSolver


# floor(1.10 * baseline) for the current 13 n=16 non-compliant cases.
_N16_ASPIRATION_LEN: dict[str, int] = {
    "L_16_4_4_3": 70,
    "L_16_5_3_3": 71,
    "L_16_5_5_4": 145,
    "L_16_6_4_4": 167,
    "L_16_6_5_4": 57,
    "L_16_6_6_5": 245,
    "L_16_7_4_4": 83,
    "L_16_7_5_4": 30,
    "L_16_7_5_5": 311,
    "L_16_7_6_5": 85,
    "L_16_7_7_4": 6,
    "L_16_7_7_5": 34,
    "L_16_7_7_6": 322,
}

_NEAR_CASES = {
    "L_16_5_3_3",
    "L_16_4_4_3",
    "L_16_6_5_4",
    "L_16_7_5_4",
    "L_16_7_7_4",
    "L_16_7_7_5",
}

_HARD_CASES = {
    "L_16_7_5_5",
    "L_16_7_7_6",
}


def _case_id(solver: "CoveringDesignSolver") -> str:
    return f"L_{solver.n}_{solver.k}_{solver.j}_{solver.s}"


def _cluster_tag(solver: "CoveringDesignSolver") -> str:
    cid = _case_id(solver)
    if cid in _NEAR_CASES:
        return "near"
    if cid in _HARD_CASES:
        if solver.j == solver.k and not solver._containment:
            return "hard_jk"
        if solver._containment:
            return "hard_containment"
        return "hard_general"
    if solver.j == solver.k and not solver._containment:
        return "mid_jk"
    if solver._containment:
        return "mid_containment"
    return "mid_general"


def _strip_superfluous_blocks(
    solver: "CoveringDesignSolver",
    masks: list[int],
    *,
    rounds: int,
    min_remaining: float,
    module_tag: str,
) -> list[int]:
    if solver._cov_table is None or solver._inv_table is None:
        return masks
    if solver._deadline_at is None:
        return masks
    if len(masks) < 4:
        return masks

    cand_index = solver._cand_index_map
    selected = [cand_index[m] for m in masks if m in cand_index]
    if len(selected) != len(masks):
        return masks

    cov_table = solver._cov_table
    best_idx = list(selected)

    for _ in range(max(1, rounds)):
        rem = solver._time_remaining_sec()
        if rem is None or rem < min_remaining:
            break
        counts = np.zeros(solver.num_targets, dtype=np.int32)
        for ci in best_idx:
            counts[cov_table[ci]] += 1

        removed_any = False
        while True:
            rem2 = solver._time_remaining_sec()
            if rem2 is None or rem2 < min_remaining:
                break

            remove_ci: int | None = None
            remove_cov_len: int | None = None
            for ci in best_idx:
                covered = cov_table[ci]
                # A superfluous block covers only already multiply-covered targets.
                if int(np.min(counts[covered])) < 2:
                    continue
                cov_len = len(covered)
                if remove_ci is None or cov_len < int(remove_cov_len):
                    remove_ci = int(ci)
                    remove_cov_len = int(cov_len)

            if remove_ci is None:
                break

            best_idx.remove(remove_ci)
            counts[cov_table[remove_ci]] -= 1
            removed_any = True

        if not removed_any:
            break

    candidate = [int(solver.cand_masks[ci]) for ci in best_idx]
    if len(candidate) < len(masks) and solver._verify(candidate):
        solver._report(
            "optimize",
            f"N16 case {module_tag} superfluous-strip improved to {len(candidate)} groups",
        )
        return candidate
    return masks


def _aggressive_anchor_chain(
    solver: "CoveringDesignSolver",
    best: list[int],
    *,
    cluster: str,
    module_tag: str,
) -> list[int]:
    if cluster == "near":
        best = solver._phase_n16_anchor_drop_one_intensify(
            best,
            rounds=8,
            ratio=0.30,
            cap=9.0,
            min_remaining=3.2,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_pair_compress(
            best,
            module_tag=module_tag,
            max_pool=36,
            max_pairs=320,
            min_remaining=2.8,
        )
        return best

    if cluster == "hard_jk":
        best = solver._phase_n16_anchor_multi_drop(
            best,
            drop_plan=(4, 3, 2, 1),
            rounds_per_drop=5,
            ratio=0.40,
            cap=22.0,
            min_remaining=4.8,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_reseed(
            best,
            rounds=4,
            keep_ratio=0.60,
            min_remaining=4.6,
            module_tag=module_tag,
            allow_same_len_fallback=False,
        )
        best = solver._phase_n16_anchor_drop_one_intensify(
            best,
            rounds=11,
            ratio=0.31,
            cap=12.0,
            min_remaining=3.8,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_pair_compress(
            best,
            module_tag=module_tag,
            max_pool=46,
            max_pairs=460,
            min_remaining=3.2,
        )
        return best

    if cluster == "hard_containment":
        best = solver._phase_n16_anchor_multi_drop(
            best,
            drop_plan=(4, 3, 2, 1),
            rounds_per_drop=5,
            ratio=0.42,
            cap=24.0,
            min_remaining=4.8,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_reseed(
            best,
            rounds=4,
            keep_ratio=0.58,
            min_remaining=4.6,
            module_tag=module_tag,
            allow_same_len_fallback=False,
        )
        best = solver._phase_n16_anchor_drop_one_intensify(
            best,
            rounds=11,
            ratio=0.30,
            cap=12.0,
            min_remaining=3.8,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_pair_compress(
            best,
            module_tag=module_tag,
            max_pool=44,
            max_pairs=420,
            min_remaining=3.2,
        )
        return best

    if cluster == "mid_jk":
        best = solver._phase_n16_anchor_multi_drop(
            best,
            drop_plan=(3, 2, 1),
            rounds_per_drop=4,
            ratio=0.36,
            cap=16.0,
            min_remaining=4.2,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_reseed(
            best,
            rounds=3,
            keep_ratio=0.64,
            min_remaining=4.0,
            module_tag=module_tag,
            allow_same_len_fallback=False,
        )
        best = solver._phase_n16_anchor_drop_one_intensify(
            best,
            rounds=9,
            ratio=0.28,
            cap=10.0,
            min_remaining=3.4,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_pair_compress(
            best,
            module_tag=module_tag,
            max_pool=40,
            max_pairs=360,
            min_remaining=3.0,
        )
        return best

    if cluster == "mid_containment":
        best = solver._phase_n16_anchor_multi_drop(
            best,
            drop_plan=(3, 2, 1),
            rounds_per_drop=4,
            ratio=0.37,
            cap=17.0,
            min_remaining=4.2,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_reseed(
            best,
            rounds=3,
            keep_ratio=0.62,
            min_remaining=4.0,
            module_tag=module_tag,
            allow_same_len_fallback=False,
        )
        best = solver._phase_n16_anchor_drop_one_intensify(
            best,
            rounds=9,
            ratio=0.29,
            cap=10.0,
            min_remaining=3.4,
            module_tag=module_tag,
        )
        best = solver._phase_n16_anchor_pair_compress(
            best,
            module_tag=module_tag,
            max_pool=40,
            max_pairs=340,
            min_remaining=3.0,
        )
        return best

    best = solver._phase_n16_anchor_multi_drop(
        best,
        drop_plan=(3, 2, 1),
        rounds_per_drop=3,
        ratio=0.34,
        cap=14.0,
        min_remaining=4.0,
        module_tag=module_tag,
    )
    best = solver._phase_n16_anchor_reseed(
        best,
        rounds=2,
        keep_ratio=0.64,
        min_remaining=3.8,
        module_tag=module_tag,
        allow_same_len_fallback=False,
    )
    best = solver._phase_n16_anchor_drop_one_intensify(
        best,
        rounds=8,
        ratio=0.28,
        cap=9.4,
        min_remaining=3.2,
        module_tag=module_tag,
    )
    return solver._phase_n16_anchor_pair_compress(
        best,
        module_tag=module_tag,
        max_pool=38,
        max_pairs=320,
        min_remaining=2.9,
    )


def _target_len_squeeze(
    solver: "CoveringDesignSolver",
    best: list[int],
    *,
    aspiration_len: int | None,
    cluster: str,
    min_remaining: float,
    module_tag: str,
) -> list[int]:
    if solver._deadline_at is None:
        return best
    if len(best) < 3:
        return best

    if aspiration_len is None:
        aspiration_len = max(1, len(best) - (3 if cluster == "near" else 6))
    aspiration_len = int(max(1, aspiration_len))

    misses = 0
    if cluster == "near":
        miss_limit = 16
    elif cluster.startswith("hard"):
        miss_limit = 8
    else:
        miss_limit = 10
    while True:
        rem = solver._time_remaining_sec()
        if rem is None or rem < min_remaining:
            break
        if len(best) <= aspiration_len:
            break

        gap = len(best) - aspiration_len
        if gap >= 12 and cluster.startswith("hard"):
            step = 4
        elif gap >= 7:
            step = 3
        elif gap >= 4:
            step = 2
        else:
            step = 1
        target_len = max(1, len(best) - step)
        if cluster == "near":
            budget = float(min(18.0, max(3.0, rem * 0.24)))
        elif cluster.startswith("hard"):
            budget = float(min(14.0, max(2.8, rem * 0.26)))
        else:
            budget = float(min(15.0, max(2.8, rem * 0.22)))
        start_masks = list(best)
        if misses > 0 or random.random() < 0.75:
            random.shuffle(start_masks)
        improved = solver._phase_g_try_target_len(start_masks, target_len, budget)
        if improved is None or len(improved) >= len(best):
            misses += 1
            if misses >= miss_limit:
                break
            continue

        best = improved
        misses = 0
        solver._report(
            "optimize",
            f"N16 case {module_tag} target-len squeeze improved to {len(best)} groups",
        )

    return best


def _intensive_reconstruct(
    solver: "CoveringDesignSolver",
    best: list[int],
    *,
    aspiration_len: int | None,
    cluster: str,
    min_remaining: float,
    module_tag: str,
) -> list[int]:
    if solver._deadline_at is None:
        return best
    if len(best) < 8:
        return best

    profiles = solver._build_attempt_profiles(max(4, int(solver._num_attempts) + 3))
    if not profiles:
        return best

    misses = 0
    if cluster == "near":
        rounds = 18
        miss_limit = 10
    elif cluster.startswith("hard"):
        rounds = 16
        miss_limit = 8
    else:
        rounds = 12
        miss_limit = 8
    for round_idx in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < min_remaining:
            break

        if aspiration_len is None:
            gap = 6
        else:
            gap = max(0, len(best) - int(aspiration_len))
        if gap >= 12 and cluster.startswith("hard"):
            target_drop = 4
        elif gap >= 7:
            target_drop = 3
        elif gap >= 3:
            target_drop = 2
        else:
            target_drop = 1
        strict_limit = max(1, len(best) - target_drop)

        base = profiles[round_idx % len(profiles)]
        strategy = solver._phase_b_strategy_variant(base, attempt_idx=round_idx + 7)

        if cluster == "near":
            keep_ratio = 0.82
        elif cluster.startswith("hard"):
            keep_ratio = 0.52 if round_idx % 2 == 0 else 0.64
        else:
            keep_ratio = 0.60 if round_idx % 2 == 0 else 0.72
        keep_count = int(len(best) * keep_ratio)
        partial: list[int] | None = None
        if keep_count >= 3 and keep_count < len(best):
            partial = random.sample(best, keep_count)

        candidate, complete, _ = solver._greedy(
            strategy,
            partial=partial,
            best_limit=strict_limit,
        )
        if not complete:
            misses += 1
            if misses >= miss_limit:
                break
            continue

        candidate = solver._optimise_solution(
            candidate,
            strategy,
            best_len=len(best),
            stagnant=0,
        )
        if len(candidate) >= len(best):
            misses += 1
            if misses >= miss_limit:
                break
            continue
        if not solver._verify(candidate):
            misses += 1
            if misses >= miss_limit:
                break
            continue

        best = candidate
        misses = 0
        solver._report(
            "optimize",
            f"N16 case {module_tag} reconstruct improved to {len(best)} groups",
        )

        rem2 = solver._time_remaining_sec()
        if rem2 is not None and rem2 >= (min_remaining + 0.6) and len(best) >= 6:
            target_len = max(1, len(best) - 1)
            budget = float(min(8.5, max(2.4, rem2 * 0.16)))
            squeezed = solver._phase_g_try_target_len(list(best), target_len, budget)
            if squeezed is not None and len(squeezed) < len(best):
                best = squeezed
                solver._report(
                    "optimize",
                    f"N16 case {module_tag} reconstruct+squeeze improved to {len(best)} groups",
                )

        if aspiration_len is not None and len(best) <= int(aspiration_len):
            break

    return best


def run_n16_case_specialized_module(
    solver: "CoveringDesignSolver",
    sol: list[int],
) -> list[int]:
    if solver.n != 16:
        return sol
    if solver._deadline_at is None:
        return sol
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 4.2:
        return sol
    if len(sol) < 8:
        return sol

    case_id = _case_id(solver)
    cluster = _cluster_tag(solver)
    module_tag = f"n16case-{cluster}"
    aspiration = _N16_ASPIRATION_LEN.get(case_id)

    best = list(sol)
    entry_len = len(best)

    # Stage 1: deterministic superfluous-element stripping.
    best = _strip_superfluous_blocks(
        solver,
        best,
        rounds=2 if cluster == "near" else 3,
        min_remaining=3.6,
        module_tag=module_tag,
    )

    # Stage 2: cluster-specific aggressive rebuild/descent.
    rounds = 3 if cluster.startswith("hard") else 2
    for _ in range(rounds):
        rem = solver._time_remaining_sec()
        if rem is None or rem < 4.0:
            break
        before = len(best)
        best = _intensive_reconstruct(
            solver,
            best,
            aspiration_len=aspiration,
            cluster=cluster,
            min_remaining=3.8,
            module_tag=module_tag,
        )
        best = _aggressive_anchor_chain(solver, best, cluster=cluster, module_tag=module_tag)
        best = _strip_superfluous_blocks(
            solver,
            best,
            rounds=1,
            min_remaining=3.2,
            module_tag=module_tag,
        )
        best = _target_len_squeeze(
            solver,
            best,
            aspiration_len=aspiration,
            cluster=cluster,
            min_remaining=3.0,
            module_tag=module_tag,
        )
        if len(best) >= before:
            break

    # Stage 3: exact patch if CP-SAT is available and we are still above aspiration.
    if aspiration is not None and len(best) > aspiration and solver._phase_c_has_time(6.0):
        before_cp = len(best)
        best = solver._phase_i_full_cp_sat_module(best, hard_case=cluster.startswith("hard"))
        if len(best) < before_cp:
            solver._report(
                "optimize",
                (
                    f"N16 case {module_tag} exact-patch improved to {len(best)} groups "
                    f"(aspire<={aspiration})"
                ),
            )
            best = _strip_superfluous_blocks(
                solver,
                best,
                rounds=1,
                min_remaining=2.8,
                module_tag=module_tag,
            )

    if len(best) < entry_len:
        gain = entry_len - len(best)
        aim_text = f", aspiration={aspiration}" if aspiration is not None else ""
        solver._report(
            "optimize",
            f"N16 case module finished {case_id}: -{gain} groups ({entry_len}->{len(best)}{aim_text})",
        )

    return best
