from __future__ import annotations

import random
import time
from dataclasses import dataclass
from itertools import combinations
from typing import Any


@dataclass(frozen=True)
class NSolverConfig:
    n: int
    orbit_seconds: float
    restarts: int
    lns_seconds: float
    exact_seconds: float
    ilp_seconds: float
    ilp_nnz_limit: int


N_SOLVER_CONFIGS: dict[int, NSolverConfig] = {
    7: NSolverConfig(7, 3.0, 40, 6.0, 2.0, 8.0, 1_000_000),
    8: NSolverConfig(8, 4.0, 60, 8.0, 2.0, 12.0, 1_500_000),
    9: NSolverConfig(9, 5.0, 80, 12.0, 2.5, 18.0, 2_000_000),
    10: NSolverConfig(10, 6.0, 90, 18.0, 3.0, 28.0, 3_000_000),
    11: NSolverConfig(11, 8.0, 100, 24.0, 3.5, 42.0, 4_000_000),
    12: NSolverConfig(12, 10.0, 110, 30.0, 4.0, 55.0, 5_000_000),
    13: NSolverConfig(13, 34.0, 120, 30.0, 4.0, 55.0, 6_500_000),
    14: NSolverConfig(14, 44.0, 130, 34.0, 4.0, 60.0, 8_000_000),
    15: NSolverConfig(15, 50.0, 140, 36.0, 4.0, 65.0, 10_000_000),
}

ORBIT_ILP_MAX_VARIABLES = 240
ORBIT_ILP_MAX_REQUIREMENTS = 1200


def solve_n_15(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    if problem.n != 15:
        raise ValueError("n15_solver only supports n=15")
    return solve_small_n(N_SOLVER_CONFIGS[15], problem, oracle, rng, deadline, tools)


def solve_n_le_15_internal(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    if problem.n not in N_SOLVER_CONFIGS or problem.n > 15:
        raise ValueError("n15_solver internal recursion only supports n <= 15")
    if problem.n == 15:
        return solve_n_15(problem, oracle, rng, deadline, tools)
    solvers = {
        7: solve_n_07,
        8: solve_n_08,
        9: solve_n_09,
        10: solve_n_10,
        11: solve_n_11,
        12: solve_n_12,
        13: solve_n_13,
        14: solve_n_14,
    }
    return solvers[problem.n](problem, oracle, rng, deadline, tools)


def solve_n_07(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    return solve_small_n(N_SOLVER_CONFIGS[7], problem, oracle, rng, deadline, tools)


def solve_n_08(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    return solve_small_n(N_SOLVER_CONFIGS[8], problem, oracle, rng, deadline, tools)


def solve_n_09(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    return solve_small_n(N_SOLVER_CONFIGS[9], problem, oracle, rng, deadline, tools)


def solve_n_10(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    return solve_small_n(N_SOLVER_CONFIGS[10], problem, oracle, rng, deadline, tools)


def solve_n_11(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    return solve_small_n(N_SOLVER_CONFIGS[11], problem, oracle, rng, deadline, tools)


def solve_n_12(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    return solve_small_n(N_SOLVER_CONFIGS[12], problem, oracle, rng, deadline, tools)


def solve_n_13(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    return solve_small_n(N_SOLVER_CONFIGS[13], problem, oracle, rng, deadline, tools)


def solve_n_14(problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    return solve_small_n(N_SOLVER_CONFIGS[14], problem, oracle, rng, deadline, tools)


def solve_small_n(config: NSolverConfig, problem: Any, oracle: Any, rng: Any, deadline: float, tools: Any) -> tuple[tuple[tuple[int, ...], ...], str]:
    if problem.n == problem.k:
        return (tuple(range(problem.n)),), f"n={config.n}:exact-single-block"
    if problem.k == problem.j == problem.s:
        return tuple(combinations(range(problem.n), problem.k)), f"n={config.n}:exact-all-k-groups"
    candidates = tuple(combinations(range(problem.n), problem.k))
    candidate_masks = tuple(oracle.block_mask(candidate) for candidate in candidates)
    target_bound = tools.lower_bound(problem)

    if is_hard_15_7_5(problem) and deadline - time.monotonic() > 35.0:
        best_indices = partial_cyclic_orbit_repair_indices(
            problem,
            oracle,
            candidates,
            candidate_masks,
            rng,
            min(deadline, time.monotonic() + 118.0),
            tools,
        )
    else:
        best_indices = cyclic_orbit_cover_indices(
            problem,
            oracle,
            candidates,
            candidate_masks,
            rng,
            min(deadline, time.monotonic() + config.orbit_seconds),
            tools,
        )

    if not is_hard_15_7_5(problem) and deadline - time.monotonic() > 35.0:
        partial_orbit_indices = partial_cyclic_orbit_repair_indices(
            problem,
            oracle,
            candidates,
            candidate_masks,
            rng,
            min(deadline, time.monotonic() + max(28.0, config.orbit_seconds)),
            tools,
        )
        if partial_orbit_indices and (not best_indices or len(partial_orbit_indices) < len(best_indices)):
            best_indices = partial_orbit_indices

    if deadline - time.monotonic() > 12.0:
        recursive_indices = recursive_covering_indices(config, problem, rng, min(deadline, time.monotonic() + config.orbit_seconds), tools)
        if recursive_indices and (not best_indices or len(recursive_indices) < len(best_indices)):
            best_indices = recursive_indices

    greedy_indices = tools.greedy_bitset_run(oracle, candidates, candidate_masks, rng, tools.profile_for_n(problem.n), randomized=False)
    if not best_indices or len(greedy_indices) < len(best_indices):
        best_indices = greedy_indices
    if len(best_indices) <= target_bound:
        return tuple(candidates[index] for index in best_indices), f"n={config.n}:bitmask-greedy-bound"

    if deadline - time.monotonic() > 12.0:
        exact_deadline = min(deadline, time.monotonic() + config.exact_seconds)
        exact_indices = tools.exact_branch_and_bound(oracle, candidate_masks, best_indices, exact_deadline)
        if exact_indices and len(exact_indices) < len(best_indices):
            best_indices = exact_indices
    if len(best_indices) <= target_bound:
        return tuple(candidates[index] for index in best_indices), f"n={config.n}:branch-and-bound"

    profile = tools.profile_for_n(problem.n)
    profile = tools.replace_profile(profile, full_restarts=config.restarts)
    restart = 0
    while restart < config.restarts and time.monotonic() < deadline:
        candidate_indices = tools.greedy_bitset_run(oracle, candidates, candidate_masks, rng, profile, randomized=True)
        candidate_indices = tools.prune_indices_by_masks(candidate_indices, candidate_masks, oracle.full_mask, rng)
        if len(candidate_indices) < len(best_indices):
            best_indices = candidate_indices
            if len(best_indices) <= target_bound:
                break
        restart += 1

    if deadline - time.monotonic() > 12.0 and len(best_indices) > target_bound:
        lns_deadline = min(deadline, time.monotonic() + config.lns_seconds)
        best_indices = tools.large_neighborhood_search_indices(candidates, candidate_masks, oracle.full_mask, best_indices, rng, lns_deadline)

    if deadline - time.monotonic() > 12.0 and len(best_indices) > target_bound:
        swap_deadline = min(deadline, time.monotonic() + max(6.0, config.lns_seconds * 0.45))
        best_indices = fixed_size_swap_compression(
            problem,
            oracle,
            candidates,
            candidate_masks,
            best_indices,
            target_bound,
            rng,
            swap_deadline,
            tools,
        )

    if config.ilp_seconds > 0 and deadline - time.monotonic() > 15.0 and len(best_indices) > target_bound:
        ilp_deadline = min(deadline, time.monotonic() + config.ilp_seconds)
        best_indices = tools.improve_with_ilp(oracle, candidate_masks, best_indices, ilp_deadline, config.ilp_nnz_limit)

    best_indices = tools.prune_indices_by_masks(best_indices, candidate_masks, oracle.full_mask, rng)
    return tuple(candidates[index] for index in best_indices), f"n={config.n}:bitmask-random-greedy-lns-ilp"


def is_hard_15_7_5(problem: Any) -> bool:
    return problem.n == 15 and problem.k == 7 and problem.j == 5 and problem.s == 5


def recursive_covering_indices(config: NSolverConfig, problem: Any, rng: Any, deadline: float, tools: Any) -> tuple[int, ...]:
    if problem.s <= 3 or problem.n - 1 < problem.k:
        return tuple()
    if problem.n - 1 not in N_SOLVER_CONFIGS:
        return tuple()
    first_problem = problem.__class__(problem.m, problem.n - 1, problem.k, problem.j, problem.s)
    second_problem = problem.__class__(problem.m, problem.n - 1, problem.k - 1, problem.j - 1, problem.s - 1)
    split_deadline = min(deadline, time.monotonic() + max(1.0, (deadline - time.monotonic()) * 0.52))
    first_blocks, _ = solve_n_le_15_internal(first_problem, tools.make_oracle(first_problem), rng, split_deadline, tools)
    if time.monotonic() >= deadline:
        return tuple()
    second_blocks, _ = solve_n_le_15_internal(second_problem, tools.make_oracle(second_problem), rng, deadline, tools)
    lifted = tuple(tuple((*block, problem.n - 1)) for block in second_blocks)
    combined_blocks = tuple(first_blocks) + lifted
    candidate_index = {block: index for index, block in enumerate(combinations(range(problem.n), problem.k))}
    try:
        return tuple(candidate_index[tuple(sorted(block))] for block in combined_blocks)
    except KeyError:
        return tuple()


def fixed_size_swap_compression(
    problem: Any,
    oracle: Any,
    candidates: tuple[tuple[int, ...], ...],
    candidate_masks: tuple[int, ...],
    initial_indices: tuple[int, ...],
    target_bound: int,
    rng: Any,
    deadline: float,
    tools: Any,
) -> tuple[int, ...]:
    best = tuple(dict.fromkeys(initial_indices))
    if len(best) <= target_bound + 1:
        return best
    cover_indices = coverage_indices_from_masks(candidate_masks)
    req_to_candidates = requirement_to_candidates(cover_indices, oracle.total_requirements)
    stalled_rounds = 0
    while len(best) > target_bound and time.monotonic() < deadline and stalled_rounds < 3:
        max_drop = max(1, min(len(best) - target_bound, 4))
        improved = False
        for drop in range(1, max_drop + 1):
            if time.monotonic() >= deadline:
                break
            target_size = len(best) - drop
            trial_deadline = min(deadline, time.monotonic() + max(3.0, (deadline - time.monotonic()) * 0.35))
            trial = try_fixed_size_repair(
                best,
                target_size,
                cover_indices,
                req_to_candidates,
                oracle.total_requirements,
                rng,
                trial_deadline,
            )
            if trial and tools.covers_full_mask(trial, candidate_masks, oracle.full_mask):
                best = tools.prune_indices_by_masks(trial, candidate_masks, oracle.full_mask, rng)
                improved = True
                break
        stalled_rounds = 0 if improved else stalled_rounds + 1
    return best


def coverage_indices_from_masks(candidate_masks: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    coverages: list[tuple[int, ...]] = []
    for mask in candidate_masks:
        indices: list[int] = []
        pending = mask
        while pending:
            bit = pending & -pending
            indices.append(bit.bit_length() - 1)
            pending ^= bit
        coverages.append(tuple(indices))
    return tuple(coverages)


def requirement_to_candidates(cover_indices: tuple[tuple[int, ...], ...], total_requirements: int) -> tuple[tuple[int, ...], ...]:
    buckets: list[list[int]] = [[] for _ in range(total_requirements)]
    for candidate_index, coverage in enumerate(cover_indices):
        for requirement_index in coverage:
            buckets[requirement_index].append(candidate_index)
    return tuple(tuple(bucket) for bucket in buckets)


def try_fixed_size_repair(
    current_indices: tuple[int, ...],
    target_size: int,
    cover_indices: tuple[tuple[int, ...], ...],
    req_to_candidates: tuple[tuple[int, ...], ...],
    total_requirements: int,
    rng: Any,
    deadline: float,
) -> tuple[int, ...]:
    selected = list(current_indices)
    counts = [0] * total_requirements
    for candidate_index in selected:
        for requirement_index in cover_indices[candidate_index]:
            counts[requirement_index] += 1
    while len(selected) > target_size:
        removal = choose_low_loss_removal(selected, cover_indices, counts, rng)
        selected.remove(removal)
        for requirement_index in cover_indices[removal]:
            counts[requirement_index] -= 1
    best_uncovered = uncovered_count(counts)
    while best_uncovered and time.monotonic() < deadline:
        uncovered = [index for index, count in enumerate(counts) if count == 0]
        rng.shuffle(uncovered)
        accepted = False
        for requirement_index in uncovered[: min(12, len(uncovered))]:
            swap = best_repair_swap(selected, counts, cover_indices, req_to_candidates[requirement_index], rng)
            if swap is None:
                continue
            add_index, remove_index, score = swap
            if score < 0 and rng.random() > 0.03:
                continue
            selected.remove(remove_index)
            for covered_requirement in cover_indices[remove_index]:
                counts[covered_requirement] -= 1
            selected.append(add_index)
            for covered_requirement in cover_indices[add_index]:
                counts[covered_requirement] += 1
            next_uncovered = uncovered_count(counts)
            best_uncovered = min(best_uncovered, next_uncovered)
            accepted = True
            if next_uncovered == 0:
                return tuple(dict.fromkeys(selected))
            break
        if not accepted:
            break
    return tuple(dict.fromkeys(selected)) if uncovered_count(counts) == 0 else tuple()


def choose_low_loss_removal(selected: list[int], cover_indices: tuple[tuple[int, ...], ...], counts: list[int], rng: Any) -> int:
    scored = []
    sample = selected if len(selected) <= 220 else rng.sample(selected, 220)
    for candidate_index in sample:
        loss = sum(1 for requirement_index in cover_indices[candidate_index] if counts[requirement_index] == 1)
        scored.append((loss, rng.random(), candidate_index))
    scored.sort()
    return scored[0][2]


def best_repair_swap(
    selected: list[int],
    counts: list[int],
    cover_indices: tuple[tuple[int, ...], ...],
    add_candidates: tuple[int, ...],
    rng: Any,
) -> tuple[int, int, int] | None:
    selected_set = set(selected)
    add_pool = [candidate_index for candidate_index in add_candidates if candidate_index not in selected_set]
    rng.shuffle(add_pool)
    best: tuple[int, int, int, float] | None = None
    removal_pool = selected if len(selected) <= 110 else rng.sample(selected, 110)
    for add_index in add_pool[:120]:
        add_coverage = set(cover_indices[add_index])
        gain = sum(1 for requirement_index in add_coverage if counts[requirement_index] == 0)
        if gain <= 0:
            continue
        for remove_index in removal_pool:
            loss = sum(
                1
                for requirement_index in cover_indices[remove_index]
                if counts[requirement_index] == 1 and requirement_index not in add_coverage
            )
            candidate = (gain - loss, add_index, remove_index, rng.random())
            if best is None or candidate > best:
                best = candidate
    if best is None:
        return None
    return best[1], best[2], best[0]


def uncovered_count(counts: list[int]) -> int:
    return sum(1 for count in counts if count == 0)


def cyclic_orbit_cover_indices(
    problem: Any,
    oracle: Any,
    candidates: tuple[tuple[int, ...], ...],
    candidate_masks: tuple[int, ...],
    rng: Any,
    deadline: float,
    tools: Any,
) -> tuple[int, ...]:
    orbits = build_cyclic_orbits(problem, candidates, candidate_masks)
    greedy_indices = greedy_orbit_cover(orbits, oracle.full_mask, rng, tools)
    best_indices = tools.prune_indices_by_masks(greedy_indices, candidate_masks, oracle.full_mask, rng) if greedy_indices else tuple()

    # Mid-sized orbit MILPs on highly symmetric cases can overrun the global per-case
    # budget without improving over greedy/local search enough to justify the delay.
    if (
        time.monotonic() < deadline
        and len(orbits) <= ORBIT_ILP_MAX_VARIABLES
        and oracle.total_requirements <= ORBIT_ILP_MAX_REQUIREMENTS
    ):
        ilp_indices = solve_orbit_ilp(orbits, oracle.total_requirements, oracle.full_mask, deadline, tools)
        if ilp_indices:
            ilp_indices = tools.prune_indices_by_masks(ilp_indices, candidate_masks, oracle.full_mask, rng)
            if not best_indices or len(ilp_indices) < len(best_indices):
                best_indices = ilp_indices
    return best_indices


def build_cyclic_orbits(
    problem: Any,
    candidates: tuple[tuple[int, ...], ...],
    candidate_masks: tuple[int, ...],
) -> tuple[tuple[tuple[int, ...], int], ...]:
    index_by_block = {block: index for index, block in enumerate(candidates)}
    orbit_map: dict[tuple[int, ...], tuple[tuple[int, ...], int]] = {}
    for block in candidates:
        orbit_blocks = tuple(
            sorted(
                {
                    tuple(sorted((value + shift) % problem.n for value in block))
                    for shift in range(problem.n)
                }
            )
        )
        key = min(orbit_blocks)
        if key in orbit_map:
            continue
        orbit_indices = tuple(index_by_block[orbit_block] for orbit_block in orbit_blocks)
        mask = 0
        for candidate_index in orbit_indices:
            mask |= candidate_masks[candidate_index]
        orbit_map[key] = (orbit_indices, mask)
    return tuple(orbit_map.values())


def partial_cyclic_orbit_repair_indices(
    problem: Any,
    oracle: Any,
    candidates: tuple[tuple[int, ...], ...],
    candidate_masks: tuple[int, ...],
    rng: Any,
    deadline: float,
    tools: Any,
) -> tuple[int, ...]:
    if not is_hard_15_7_5(problem):
        return tuple()
    search_rng = random.Random(141414)
    orbits = build_cyclic_orbits(problem, candidates, candidate_masks)
    orbit_requirements = tuple(mask_to_indices(orbit_mask) for _, orbit_mask in orbits)
    req_to_orbits = orbit_requirement_buckets(orbit_requirements, oracle.total_requirements)
    greedy_orbits = greedy_orbit_selection(orbits, oracle.full_mask, tools)
    target_orbits = 14
    if len(greedy_orbits) <= target_orbits:
        return tuple()

    fast_solution = fast_partial_orbit_uncovered_repair_indices(
        orbits,
        orbit_requirements,
        req_to_orbits,
        greedy_orbits,
        target_orbits,
        oracle,
        candidate_masks,
        min(deadline, time.monotonic() + 85.0),
        tools,
    )
    if fast_solution and len(fast_solution) <= 228:
        return fast_solution

    current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
    best_orbits = list(current_orbits)
    best_record = evaluate_repaired_orbit_record(
        current_orbits,
        orbits,
        oracle,
        candidate_masks,
        search_rng,
        min(deadline, time.monotonic() + 15.0),
        tools,
    )
    iteration = 0
    while deadline - time.monotonic() > 6.0:
        uncovered_requirements = mask_to_indices(oracle.full_mask & ~orbit_selection_coverage(current_orbits, orbits))
        trial_best: tuple[int, float, list[int]] | None = None
        add_pool: list[int] = []
        for _ in range(64):
            if uncovered_requirements and search_rng.random() < 0.88:
                add_pool.append(search_rng.choice(req_to_orbits[search_rng.choice(uncovered_requirements)]))
            else:
                add_pool.append(search_rng.randrange(len(orbits)))
        for add_orbit in add_pool:
            if add_orbit in current_orbits:
                continue
            for remove_orbit in current_orbits:
                trial = [orbit for orbit in current_orbits if orbit != remove_orbit]
                trial.append(add_orbit)
                uncovered_count_after_swap = tools.count_bits(oracle.full_mask & ~orbit_selection_coverage(trial, orbits))
                candidate = (uncovered_count_after_swap, search_rng.random(), trial)
                if trial_best is None or candidate < trial_best:
                    trial_best = candidate
        if trial_best is None:
            current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
            iteration += 1
            continue
        quick_uncovered, _, trial_orbits = trial_best
        if quick_uncovered <= best_record[2] + 40 or iteration % 25 == 0:
            record = evaluate_repaired_orbit_record(
                trial_orbits,
                orbits,
                oracle,
                candidate_masks,
                search_rng,
                min(deadline, time.monotonic() + 5.0),
                tools,
            )
            if record[3] and record[:3] < best_record[:3]:
                best_record = record
                best_orbits = list(trial_orbits)
                if best_record[0] <= 217:
                    break
        if quick_uncovered < best_record[2] + 80 or search_rng.random() < 0.08:
            current_orbits = list(trial_orbits)
        else:
            current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
        iteration += 1
    if best_record[3]:
        if deadline - time.monotonic() > 2.0:
            final_record = evaluate_repaired_orbit_record(
                best_orbits,
                orbits,
                oracle,
                candidate_masks,
                search_rng,
                min(deadline, time.monotonic() + 35.0),
                tools,
            )
            if final_record[3] and final_record[:3] <= best_record[:3]:
                return final_record[4]
        return best_record[4]
    return tuple()


def partial_cyclic_orbit_repair_with_seed(
    oracle: Any,
    candidates: tuple[tuple[int, ...], ...],
    candidate_masks: tuple[int, ...],
    target_orbits: int,
    seed: int,
    deadline: float,
    tools: Any,
) -> tuple[int, ...]:
    search_rng = random.Random(seed)
    orbits = build_cyclic_orbits(oracle.problem, candidates, candidate_masks)
    orbit_requirements = tuple(mask_to_indices(orbit_mask) for _, orbit_mask in orbits)
    req_to_orbits = orbit_requirement_buckets(orbit_requirements, oracle.total_requirements)
    greedy_orbits = greedy_orbit_selection(orbits, oracle.full_mask, tools)
    if len(greedy_orbits) <= target_orbits:
        return tuple()
    current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
    best_orbits = list(current_orbits)
    best_uncovered = tools.count_bits(oracle.full_mask & ~orbit_selection_coverage(best_orbits, orbits))
    search_deadline = min(deadline, time.monotonic() + max(1.0, deadline - time.monotonic() - 30.0))
    while time.monotonic() < search_deadline:
        uncovered_requirements = mask_to_indices(oracle.full_mask & ~orbit_selection_coverage(current_orbits, orbits))
        trial_best: tuple[int, float, list[int]] | None = None
        for _ in range(120):
            if uncovered_requirements and search_rng.random() < 0.92:
                add_orbit = search_rng.choice(req_to_orbits[search_rng.choice(uncovered_requirements)])
            else:
                add_orbit = search_rng.randrange(len(orbits))
            if add_orbit in current_orbits:
                continue
            for remove_orbit in current_orbits:
                trial = [orbit for orbit in current_orbits if orbit != remove_orbit]
                trial.append(add_orbit)
                uncovered_after_swap = tools.count_bits(oracle.full_mask & ~orbit_selection_coverage(trial, orbits))
                candidate = (uncovered_after_swap, search_rng.random(), trial)
                if trial_best is None or candidate < trial_best:
                    trial_best = candidate
        if trial_best is None:
            current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
            continue
        uncovered_after_swap, _, trial_orbits = trial_best
        if uncovered_after_swap < best_uncovered:
            best_uncovered = uncovered_after_swap
            best_orbits = list(trial_orbits)
            if best_uncovered <= 64:
                break
        if uncovered_after_swap < best_uncovered + 160 or search_rng.random() < 0.1:
            current_orbits = list(trial_orbits)
        else:
            current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
    record = evaluate_repaired_orbit_record(
        best_orbits,
        orbits,
        oracle,
        candidate_masks,
        search_rng,
        min(deadline, time.monotonic() + 30.0),
        tools,
    )
    return record[4] if record[3] else tuple()


def fast_partial_orbit_uncovered_repair_indices(
    orbits: tuple[tuple[tuple[int, ...], int], ...],
    orbit_requirements: tuple[tuple[int, ...], ...],
    req_to_orbits: tuple[tuple[int, ...], ...],
    greedy_orbits: list[int],
    target_orbits: int,
    oracle: Any,
    candidate_masks: tuple[int, ...],
    deadline: float,
    tools: Any,
) -> tuple[int, ...]:
    search_rng = random.Random(777001)
    current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
    best_orbits = list(current_orbits)
    best_uncovered = tools.count_bits(oracle.full_mask & ~orbit_selection_coverage(best_orbits, orbits))
    search_deadline = min(deadline, time.monotonic() + max(1.0, deadline - time.monotonic() - 25.0))
    while time.monotonic() < search_deadline:
        uncovered_requirements = mask_to_indices(oracle.full_mask & ~orbit_selection_coverage(current_orbits, orbits))
        trial_best: tuple[int, float, list[int]] | None = None
        for _ in range(130):
            if uncovered_requirements and search_rng.random() < 0.92:
                add_orbit = search_rng.choice(req_to_orbits[search_rng.choice(uncovered_requirements)])
            else:
                add_orbit = search_rng.randrange(len(orbits))
            if add_orbit in current_orbits:
                continue
            for remove_orbit in current_orbits:
                trial = [orbit for orbit in current_orbits if orbit != remove_orbit]
                trial.append(add_orbit)
                uncovered_after_swap = tools.count_bits(oracle.full_mask & ~orbit_selection_coverage(trial, orbits))
                candidate = (uncovered_after_swap, search_rng.random(), trial)
                if trial_best is None or candidate < trial_best:
                    trial_best = candidate
        if trial_best is None:
            current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
            continue
        uncovered_after_swap, _, trial_orbits = trial_best
        if uncovered_after_swap < best_uncovered:
            best_uncovered = uncovered_after_swap
            best_orbits = list(trial_orbits)
            if best_uncovered <= 33:
                break
        if uncovered_after_swap < best_uncovered + 100 or search_rng.random() < 0.1:
            current_orbits = list(trial_orbits)
        else:
            current_orbits = trim_orbit_selection(greedy_orbits, target_orbits, orbit_requirements, oracle.total_requirements, search_rng)[0]
    record = evaluate_repaired_orbit_record(
        best_orbits,
        orbits,
        oracle,
        candidate_masks,
        search_rng,
        min(deadline, time.monotonic() + 25.0),
        tools,
    )
    return record[4] if record[3] else tuple()


def repaired_solution_score(solution: tuple[int, ...]) -> tuple[int, int]:
    return len(solution), sum(solution)


def orbit_selection_coverage(selected_orbits: list[int], orbits: tuple[tuple[tuple[int, ...], int], ...]) -> int:
    coverage = 0
    for orbit_index in selected_orbits:
        coverage |= orbits[orbit_index][1]
    return coverage


def evaluate_repaired_orbit_record(
    selected_orbits: list[int],
    orbits: tuple[tuple[tuple[int, ...], int], ...],
    oracle: Any,
    candidate_masks: tuple[int, ...],
    rng: Any,
    deadline: float,
    tools: Any,
) -> tuple[int, int, int, bool, tuple[int, ...]]:
    selected_indices: list[int] = []
    coverage = 0
    for orbit_index in selected_orbits:
        orbit_indices, orbit_mask = orbits[orbit_index]
        selected_indices.extend(orbit_indices)
        coverage |= orbit_mask
    uncovered_mask = oracle.full_mask & ~coverage
    repair_indices = repair_uncovered_requirements_with_ilp(
        selected_indices,
        uncovered_mask,
        candidate_masks,
        oracle.total_requirements,
        rng,
        deadline,
        tools,
    )
    candidate_solution = tuple(dict.fromkeys((*selected_indices, *repair_indices)))
    if tools.covers_full_mask(candidate_solution, candidate_masks, oracle.full_mask):
        pruned = tools.prune_indices_by_masks(candidate_solution, candidate_masks, oracle.full_mask, rng)
        return len(pruned), len(repair_indices), tools.count_bits(uncovered_mask), True, pruned
    return len(candidate_solution), len(repair_indices), tools.count_bits(uncovered_mask), False, tuple()


def evaluate_repaired_orbit_selection(
    selected_orbits: list[int],
    orbits: tuple[tuple[tuple[int, ...], int], ...],
    oracle: Any,
    candidate_masks: tuple[int, ...],
    rng: Any,
    deadline: float,
    tools: Any,
) -> tuple[int, ...]:
    selected_indices: list[int] = []
    coverage = 0
    for orbit_index in selected_orbits:
        orbit_indices, orbit_mask = orbits[orbit_index]
        selected_indices.extend(orbit_indices)
        coverage |= orbit_mask
    uncovered_mask = oracle.full_mask & ~coverage
    repair_indices = repair_uncovered_requirements_with_ilp(
        selected_indices,
        uncovered_mask,
        candidate_masks,
        oracle.total_requirements,
        rng,
        deadline,
        tools,
    )
    candidate_solution = tuple(dict.fromkeys((*selected_indices, *repair_indices)))
    if tools.covers_full_mask(candidate_solution, candidate_masks, oracle.full_mask):
        return tools.prune_indices_by_masks(candidate_solution, candidate_masks, oracle.full_mask, rng)
    return tuple()


def mask_to_indices(mask: int) -> tuple[int, ...]:
    indices: list[int] = []
    pending = mask
    while pending:
        bit = pending & -pending
        indices.append(bit.bit_length() - 1)
        pending ^= bit
    return tuple(indices)


def orbit_requirement_buckets(orbit_requirements: tuple[tuple[int, ...], ...], total_requirements: int) -> tuple[tuple[int, ...], ...]:
    buckets: list[list[int]] = [[] for _ in range(total_requirements)]
    for orbit_index, requirements in enumerate(orbit_requirements):
        for requirement in requirements:
            buckets[requirement].append(orbit_index)
    return tuple(tuple(bucket) for bucket in buckets)


def greedy_orbit_selection(orbits: tuple[tuple[tuple[int, ...], int], ...], full_mask: int, tools: Any) -> list[int]:
    uncovered = full_mask
    selected: list[int] = []
    while uncovered:
        best: tuple[int, int] | None = None
        for orbit_index, (_, orbit_mask) in enumerate(orbits):
            gain = tools.count_bits(orbit_mask & uncovered)
            if gain > 0 and (best is None or gain > best[0]):
                best = (gain, orbit_index)
        if best is None:
            break
        selected.append(best[1])
        uncovered &= ~orbits[best[1]][1]
    return selected


def trim_orbit_selection(
    selected_orbits: list[int],
    target_orbits: int,
    orbit_requirements: tuple[tuple[int, ...], ...],
    total_requirements: int,
    rng: Any,
) -> tuple[list[int], list[int]]:
    selected = list(selected_orbits)
    counts = [0] * total_requirements
    for orbit_index in selected:
        for requirement in orbit_requirements[orbit_index]:
            counts[requirement] += 1
    while len(selected) > target_orbits:
        scored: list[tuple[int, float, int]] = []
        for orbit_index in selected:
            loss = sum(1 for requirement in orbit_requirements[orbit_index] if counts[requirement] == 1)
            scored.append((loss, rng.random(), orbit_index))
        scored.sort()
        remove_orbit = scored[0][2]
        selected.remove(remove_orbit)
        for requirement in orbit_requirements[remove_orbit]:
            counts[requirement] -= 1
    return selected, counts


def best_orbit_swap(
    selected_orbits: list[int],
    selected_set: set[int],
    counts: list[int],
    orbit_requirements: tuple[tuple[int, ...], ...],
    req_to_orbits: tuple[tuple[int, ...], ...],
    rng: Any,
) -> tuple[int, int, int] | None:
    uncovered = [requirement for requirement, count in enumerate(counts) if count == 0]
    if not uncovered:
        return None
    best: tuple[int, float, int, int] | None = None
    for _ in range(100):
        add_orbit = rng.choice(req_to_orbits[rng.choice(uncovered)]) if rng.random() < 0.9 else rng.randrange(len(orbit_requirements))
        if add_orbit in selected_set:
            continue
        for remove_orbit in selected_orbits:
            delta = orbit_swap_delta(counts, orbit_requirements, remove_orbit, add_orbit)
            candidate = (delta, rng.random(), remove_orbit, add_orbit)
            if best is None or candidate < best:
                best = candidate
    if best is None:
        return None
    return best[0], best[2], best[3]


def orbit_swap_delta(
    counts: list[int],
    orbit_requirements: tuple[tuple[int, ...], ...],
    remove_orbit: int,
    add_orbit: int,
) -> int:
    remove_requirements = set(orbit_requirements[remove_orbit])
    add_requirements = set(orbit_requirements[add_orbit])
    delta = 0
    for requirement in remove_requirements | add_requirements:
        old_count = counts[requirement]
        next_count = old_count - (1 if requirement in remove_requirements else 0) + (1 if requirement in add_requirements else 0)
        if old_count == 0 and next_count > 0:
            delta -= 1
        elif old_count > 0 and next_count == 0:
            delta += 1
    return delta


def apply_orbit_swap(
    selected_orbits: list[int],
    selected_set: set[int],
    counts: list[int],
    orbit_requirements: tuple[tuple[int, ...], ...],
    remove_orbit: int,
    add_orbit: int,
) -> None:
    selected_orbits.remove(remove_orbit)
    selected_set.remove(remove_orbit)
    for requirement in orbit_requirements[remove_orbit]:
        counts[requirement] -= 1
    selected_orbits.append(add_orbit)
    selected_set.add(add_orbit)
    for requirement in orbit_requirements[add_orbit]:
        counts[requirement] += 1


def repair_uncovered_requirements_with_ilp(
    selected_indices: list[int],
    uncovered_mask: int,
    candidate_masks: tuple[int, ...],
    total_requirements: int,
    rng: Any,
    deadline: float,
    tools: Any,
) -> tuple[int, ...]:
    if not uncovered_mask:
        return tuple()
    uncovered_requirements = mask_to_indices(uncovered_mask)
    selected_set = set(selected_indices)
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
        from scipy.sparse import coo_array
    except Exception:
        return greedy_repair_uncovered(selected_set, uncovered_mask, candidate_masks, rng, tools)

    variable_indices: list[int] = []
    rows: list[int] = []
    columns: list[int] = []
    for candidate_index, candidate_mask in enumerate(candidate_masks):
        if candidate_index in selected_set:
            continue
        column = len(variable_indices)
        hit = False
        for row, requirement in enumerate(uncovered_requirements):
            if candidate_mask & (1 << requirement):
                rows.append(row)
                columns.append(column)
                hit = True
        if hit:
            variable_indices.append(candidate_index)
    if not variable_indices:
        return tuple()
    matrix = coo_array(
        (
            np.ones(len(rows), dtype=np.int8),
            (np.array(rows, dtype=np.int32), np.array(columns, dtype=np.int32)),
        ),
        shape=(len(uncovered_requirements), len(variable_indices)),
    ).tocsc()
    constraints = LinearConstraint(matrix, lb=np.ones(len(uncovered_requirements)), ub=np.full(len(uncovered_requirements), np.inf))
    time_budget = deadline - time.monotonic()
    if time_budget < 2.0:
        return greedy_repair_uncovered(selected_set, uncovered_mask, candidate_masks, rng, tools)
    result = milp(
        c=np.ones(len(variable_indices), dtype=np.float64),
        integrality=np.ones(len(variable_indices), dtype=np.int8),
        bounds=Bounds(0, 1),
        constraints=constraints,
        options={"time_limit": max(1.0, time_budget), "mip_rel_gap": 0.0, "presolve": True},
    )
    values = getattr(result, "x", None)
    if values is None:
        return greedy_repair_uncovered(selected_set, uncovered_mask, candidate_masks, rng, tools)
    repair = tuple(variable_indices[column] for column, value in enumerate(values) if value >= 0.5)
    return repair or greedy_repair_uncovered(selected_set, uncovered_mask, candidate_masks, rng, tools)


def greedy_repair_uncovered(
    selected_set: set[int],
    uncovered_mask: int,
    candidate_masks: tuple[int, ...],
    rng: Any,
    tools: Any,
) -> tuple[int, ...]:
    repair: list[int] = []
    while uncovered_mask:
        scored: list[tuple[int, float, int]] = []
        for candidate_index, candidate_mask in enumerate(candidate_masks):
            if candidate_index in selected_set:
                continue
            gain = tools.count_bits(candidate_mask & uncovered_mask)
            if gain > 0:
                scored.append((gain, rng.random(), candidate_index))
        if not scored:
            break
        scored.sort(reverse=True)
        selected_index = scored[0][2]
        selected_set.add(selected_index)
        repair.append(selected_index)
        uncovered_mask &= ~candidate_masks[selected_index]
    return tuple(repair)


def greedy_orbit_cover(orbits: tuple[tuple[tuple[int, ...], int], ...], full_mask: int, rng: Any, tools: Any) -> tuple[int, ...]:
    uncovered = full_mask
    selected: list[int] = []
    while uncovered:
        scored: list[tuple[float, int, float, tuple[int, ...], int]] = []
        for orbit_indices, orbit_mask in orbits:
            gain = tools.count_bits(orbit_mask & uncovered)
            if gain > 0:
                scored.append((gain / len(orbit_indices), gain, rng.random(), orbit_indices, orbit_mask))
        if not scored:
            break
        scored.sort(reverse=True)
        _, _, _, orbit_indices, orbit_mask = scored[0]
        selected.extend(orbit_indices)
        uncovered &= ~orbit_mask
    return tuple(dict.fromkeys(selected))


def solve_orbit_ilp(
    orbits: tuple[tuple[tuple[int, ...], int], ...],
    total_requirements: int,
    full_mask: int,
    deadline: float,
    tools: Any,
) -> tuple[int, ...]:
    remaining = deadline - time.monotonic()
    if remaining < 1.0:
        return tuple()
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
        from scipy.sparse import coo_array
    except Exception:
        return tuple()

    rows: list[int] = []
    columns: list[int] = []
    costs: list[float] = []
    for orbit_index, (orbit_indices, orbit_mask) in enumerate(orbits):
        costs.append(float(len(orbit_indices)))
        pending = orbit_mask
        while pending:
            bit = pending & -pending
            rows.append(bit.bit_length() - 1)
            columns.append(orbit_index)
            pending ^= bit
    if not rows:
        return tuple()
    matrix = coo_array(
        (
            np.ones(len(rows), dtype=np.int8),
            (np.array(rows, dtype=np.int32), np.array(columns, dtype=np.int32)),
        ),
        shape=(total_requirements, len(orbits)),
    ).tocsc()
    constraints = LinearConstraint(matrix, lb=np.ones(total_requirements), ub=np.full(total_requirements, np.inf))
    result = milp(
        c=np.array(costs, dtype=np.float64),
        integrality=np.ones(len(orbits), dtype=np.int8),
        bounds=Bounds(0, 1),
        constraints=constraints,
        options={"time_limit": max(1.0, remaining), "mip_rel_gap": 0.04, "presolve": True},
    )
    values = getattr(result, "x", None)
    if values is None:
        return tuple()
    selected: list[int] = []
    coverage = 0
    for orbit_index, value in enumerate(values):
        if value >= 0.5:
            orbit_indices, orbit_mask = orbits[orbit_index]
            selected.extend(orbit_indices)
            coverage |= orbit_mask
    if coverage != full_mask:
        return tuple()
    return tuple(dict.fromkeys(selected))


class CoveringDesignSolver:
    """Root-level adapter for the dedicated n=15 algorithm."""

    def __init__(
        self,
        n: int,
        k: int,
        j: int,
        s: int,
        t: int = 1,
        *,
        progress_cb: Any | None = None,
        cancel_fn: Any | None = None,
        num_attempts: int = 3,
        time_budget_sec: float | None = None,
        skip_final_verify: bool = False,
    ) -> None:
        if int(n) != 15:
            raise ValueError(f"n15_solver only handles n=15, got n={n}")
        if int(t) != 1:
            raise ValueError("n15_solver only supports t=1")
        self.n = int(n)
        self.k = int(k)
        self.j = int(j)
        self.s = int(s)
        self.t = int(t)
        self._progress_cb = progress_cb
        self._cancel_fn = cancel_fn or (lambda: False)
        self._num_attempts = int(num_attempts)
        self._time_budget_sec = time_budget_sec
        self._skip_final_verify = skip_final_verify
        self._started_at = time.time()

    def solve(self) -> Any:
        from n_algorithms.shared.optimal_samples import Problem, solve_problem, verify_solution
        from solver import SolverProgress, SolverResult

        if self._cancel_fn():
            return SolverResult(
                groups=[],
                num_groups=0,
                elapsed=time.time() - self._started_at,
                verified=False,
                route_module=__name__,
                solution_source="cancelled",
                route_case=self._case_label(),
            )

        if self._progress_cb is not None:
            self._progress_cb(
                SolverProgress(
                    phase="dispatch",
                    message=f"n15 dedicated solver: {self._case_label()}",
                    elapsed=time.time() - self._started_at,
                )
            )

        problem = Problem(45, self.n, self.k, self.j, self.s)
        samples = tuple(range(1, self.n + 1))
        time_limit = self._time_budget_sec if self._time_budget_sec and self._time_budget_sec > 0 else 120.0
        solved = solve_problem(problem, samples, time_limit=float(time_limit))
        groups = [list(block) for block in solved.index_blocks]
        verified = False if self._skip_final_verify else verify_solution(problem, solved.index_blocks)
        return SolverResult(
            groups=groups,
            num_groups=len(groups),
            elapsed=solved.elapsed_seconds,
            verified=verified,
            first_legal_elapsed=solved.elapsed_seconds if groups else None,
            route_module=__name__,
            solution_source=solved.strategy,
            route_case=self._case_label(),
        )

    def _case_label(self) -> str:
        return f"L({self.n},{self.k},{self.j},{self.s})"

    def _verify(self, masks: list[int]) -> bool:
        from n_algorithms.shared.optimal_samples import Problem, verify_solution
        from n_algorithms.shared.solver_core import mask_to_elements

        blocks = tuple(tuple(mask_to_elements(int(mask))) for mask in masks)
        return verify_solution(Problem(45, self.n, self.k, self.j, self.s), blocks)