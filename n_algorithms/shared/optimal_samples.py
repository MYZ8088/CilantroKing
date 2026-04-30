from __future__ import annotations

import argparse
import math
import random
import sys
import time
from dataclasses import dataclass, replace
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from n_algorithms.shared.solver_dispatcher import SolverTools, dispatch_solver


SYSTEM_TITLE = "An Optimal Samples Selection System"
DEFAULT_DB_DIR = Path("db")
MAX_SAMPLE_VALUE = 54
HAS_NATIVE_BIT_COUNT = hasattr(int, "bit_count")


def count_bits(value: int) -> int:
    if HAS_NATIVE_BIT_COUNT:
        return value.bit_count()  # type: ignore[attr-defined]
    return bin(value).count("1")


@dataclass(frozen=True)
class Problem:
    m: int
    n: int
    k: int
    j: int
    s: int

    def validate(self) -> None:
        if self.m <= 0:
            raise ValueError("m must be a positive integer")
        if self.n <= 0 or self.k <= 0 or self.j <= 0 or self.s <= 0:
            raise ValueError("n, k, j and s must be positive integers")
        if self.m > MAX_SAMPLE_VALUE:
            raise ValueError("m must not exceed 54 according to the project range")
        if not 7 <= self.n <= 25:
            raise ValueError("n must be in the project range 7..25")
        if not 4 <= self.k <= 7:
            raise ValueError("k must be in the project range 4..7")
        if not 3 <= self.s <= 7:
            raise ValueError("s must be in the project range 3..7")
        if self.n > self.m:
            raise ValueError("n cannot be greater than m")
        if self.k > self.n:
            raise ValueError("k cannot be greater than n")
        if self.j > self.n:
            raise ValueError("j cannot be greater than n")
        if self.s > self.j:
            raise ValueError("s cannot be greater than j")
        if self.s > self.k:
            raise ValueError("s cannot be greater than k")
        if self.j > self.k:
            raise ValueError("this implementation follows the PDF constraint s <= j <= k")


@dataclass(frozen=True)
class SolverProfile:
    exact_max_universe: int
    full_greedy_max_n: int
    full_restarts: int
    top_width: int
    pool_size: int
    sampled_requirements: int
    generated_per_requirement: int
    exact_pool_limit: int
    max_mask_bytes: int


@dataclass(frozen=True)
class SolverResult:
    problem: Problem
    samples: tuple[int, ...]
    index_blocks: tuple[tuple[int, ...], ...]
    blocks: tuple[tuple[int, ...], ...]
    lower_bound: int
    total_requirements: int
    elapsed_seconds: float
    strategy: str


class CoverageOracle:
    def __init__(self, problem: Problem, *, prefer_masks: bool, max_mask_bytes: int) -> None:
        self.problem = problem
        self.requirements = tuple(combinations(range(problem.n), problem.j))
        self.requirement_index = {requirement: index for index, requirement in enumerate(self.requirements)}
        self.total_requirements = len(self.requirements)
        self.full_mask = (1 << self.total_requirements) - 1
        self.block_cover_capacity = block_cover_count(problem)
        estimated_mask_bytes = math.comb(problem.n, problem.s) * max(1, (self.total_requirements + 7) // 8)
        self.use_masks = prefer_masks and estimated_mask_bytes <= max_mask_bytes
        self.s_masks = self._build_s_masks() if self.use_masks else {}

    def _build_s_masks(self) -> dict[tuple[int, ...], int]:
        masks = {sample_set: 0 for sample_set in combinations(range(self.problem.n), self.problem.s)}
        for requirement_index, requirement in enumerate(self.requirements):
            bit = 1 << requirement_index
            for sample_set in combinations(requirement, self.problem.s):
                masks[sample_set] |= bit
        return masks

    def block_mask(self, block: tuple[int, ...]) -> int:
        mask = 0
        for sample_set in combinations(block, self.problem.s):
            mask |= self.s_masks.get(sample_set, 0)
        return mask

    def block_cover_indices(self, block: tuple[int, ...]) -> Iterator[int]:
        block_set = set(block)
        outside = tuple(index for index in range(self.problem.n) if index not in block_set)
        for intersection_size in range(self.problem.s, min(self.problem.j, self.problem.k) + 1):
            outside_size = self.problem.j - intersection_size
            if outside_size < 0 or outside_size > len(outside):
                continue
            for inside_part in combinations(block, intersection_size):
                for outside_part in combinations(outside, outside_size):
                    requirement = tuple(sorted(inside_part + outside_part))
                    yield self.requirement_index[requirement]

    def score_block_exact(self, block: tuple[int, ...], uncovered_mask: int | None, uncovered_flags: bytearray | None) -> int:
        if self.use_masks:
            if uncovered_mask is None:
                raise ValueError("uncovered_mask is required when masks are enabled")
            return count_bits(self.block_mask(block) & uncovered_mask)
        if uncovered_flags is None:
            raise ValueError("uncovered_flags is required when masks are disabled")
        return sum(1 for index in self.block_cover_indices(block) if uncovered_flags[index])

    def mark_block_covered(
        self,
        block: tuple[int, ...],
        uncovered_mask: int | None,
        uncovered_flags: bytearray | None,
        uncovered_count: int,
    ) -> tuple[int | None, int]:
        if self.use_masks:
            if uncovered_mask is None:
                raise ValueError("uncovered_mask is required when masks are enabled")
            next_mask = uncovered_mask & ~self.block_mask(block)
            return next_mask, count_bits(next_mask)
        if uncovered_flags is None:
            raise ValueError("uncovered_flags is required when masks are disabled")
        next_count = uncovered_count
        for index in self.block_cover_indices(block):
            if uncovered_flags[index]:
                uncovered_flags[index] = 0
                next_count -= 1
        return None, next_count

    def uncovered_indices_from_mask(self, uncovered_mask: int) -> list[int]:
        indices: list[int] = []
        pending = uncovered_mask
        while pending:
            bit = pending & -pending
            indices.append(bit.bit_length() - 1)
            pending ^= bit
        return indices


def profile_for_n(n: int) -> SolverProfile:
    if n <= 10:
        return SolverProfile(1000, 18, 80, 10, 500, 300, 6, 120, 180_000_000)
    if n <= 14:
        return SolverProfile(1200, 18, 42, 12, 900, 600, 5, 160, 180_000_000)
    if n <= 18:
        return SolverProfile(0, 18, 12, 8, 1400, 900, 4, 180, 180_000_000)
    if n <= 21:
        return SolverProfile(0, 18, 4, 8, 2200, 1800, 4, 220, 110_000_000)
    return SolverProfile(0, 18, 3, 8, 3200, 2600, 3, 260, 95_000_000)


def block_cover_count(problem: Problem) -> int:
    total = 0
    for intersection_size in range(problem.s, min(problem.j, problem.k) + 1):
        outside_size = problem.j - intersection_size
        if 0 <= outside_size <= problem.n - problem.k:
            total += math.comb(problem.k, intersection_size) * math.comb(problem.n - problem.k, outside_size)
    return total


def lower_bound(problem: Problem) -> int:
    capacity = block_cover_count(problem)
    if capacity <= 0:
        raise ValueError("no k-group can cover the requested j/s condition")
    counting_bound = math.ceil(math.comb(problem.n, problem.j) / capacity)
    if problem.s == problem.j:
        return max(counting_bound, schonheim_bound(problem.n, problem.k, problem.j))
    return counting_bound


def schonheim_bound(n: int, k: int, t: int) -> int:
    if t <= 0:
        return 1
    return math.ceil(n * schonheim_bound(n - 1, k - 1, t - 1) / k)


def parse_samples(raw_samples: str | None, problem: Problem, rng: random.Random) -> tuple[int, ...]:
    if raw_samples:
        raw_parts = tuple(part.strip() for part in raw_samples.split(",") if part.strip())
        if len(raw_parts) != problem.n:
            raise ValueError(f"exactly {problem.n} samples are required")
        try:
            samples = tuple(int(part) for part in raw_parts)
        except ValueError as exc:
            raise ValueError("samples must use positive integers, e.g. 1,2,3,...,54") from exc
        if len(samples) != problem.n:
            raise ValueError(f"exactly {problem.n} samples are required")
        if len(set(samples)) != len(samples):
            raise ValueError("samples must be unique")
        if min(samples) < 1 or max(samples) > problem.m:
            raise ValueError("samples must be within 1..m")
        return tuple(sorted(samples))
    return tuple(sorted(rng.sample(range(1, problem.m + 1), problem.n)))


def stable_solver_seed(problem: Problem, samples: Sequence[int]) -> int:
    value = 2166136261
    for item in (problem.m, problem.n, problem.k, problem.j, problem.s, *samples):
        value ^= int(item) & 0xFFFFFFFF
        value = (value * 16777619) & 0xFFFFFFFF
    return value


def solve_problem(problem: Problem, samples: Sequence[int], *, seed: int | None = None, time_limit: float) -> SolverResult:
    problem.validate()
    start = time.monotonic()
    deadline = start + max(1.0, time_limit)
    rng = random.Random(stable_solver_seed(problem, samples) if seed is None else seed)
    profile = profile_for_n(problem.n)
    prefer_masks = problem.n <= profile.full_greedy_max_n or problem.s <= 3
    oracle = CoverageOracle(problem, prefer_masks=prefer_masks, max_mask_bytes=profile.max_mask_bytes)
    dispatch = dispatch_solver(problem, oracle, rng, deadline, profile, make_solver_tools())
    index_blocks = dispatch.index_blocks
    strategy = dispatch.strategy
    repaired_blocks = repair_solution(oracle, tuple(index_blocks), rng)
    pruned_blocks = prune_solution(oracle, repaired_blocks, rng)
    blocks = tuple(tuple(samples[index] for index in block) for block in pruned_blocks)
    return SolverResult(
        problem=problem,
        samples=tuple(samples),
        index_blocks=pruned_blocks,
        blocks=blocks,
        lower_bound=lower_bound(problem),
        total_requirements=oracle.total_requirements,
        elapsed_seconds=time.monotonic() - start,
        strategy=strategy,
    )


def make_solver_tools() -> SolverTools:
    return SolverTools(
        lower_bound=lower_bound,
        count_bits=count_bits,
        make_oracle=make_coverage_oracle,
        profile_for_n=profile_for_n,
        replace_profile=replace,
        greedy_bitset_run=greedy_bitset_run,
        prune_indices_by_masks=prune_indices_by_masks,
        exact_branch_and_bound=exact_branch_and_bound,
        large_neighborhood_search_indices=large_neighborhood_search_indices,
        covers_full_mask=covers_full_mask,
        improve_with_ilp=improve_small_n_with_milp,
        solve_with_full_greedy=solve_with_full_greedy,
        should_use_subset_count_greedy=should_use_subset_count_greedy,
        solve_with_subset_count_greedy=solve_with_subset_count_greedy,
        solve_with_candidate_pool=solve_with_candidate_pool,
    )


def make_coverage_oracle(problem: Problem) -> CoverageOracle:
    profile = profile_for_n(problem.n)
    prefer_masks = problem.n <= profile.full_greedy_max_n or problem.s <= 3
    return CoverageOracle(problem, prefer_masks=prefer_masks, max_mask_bytes=profile.max_mask_bytes)


def solve_with_full_greedy(
    oracle: CoverageOracle,
    rng: random.Random,
    deadline: float,
    profile: SolverProfile,
) -> tuple[tuple[int, ...], ...]:
    candidates = tuple(combinations(range(oracle.problem.n), oracle.problem.k))
    candidate_masks = tuple(oracle.block_mask(candidate) for candidate in candidates)
    target_bound = lower_bound(oracle.problem)
    best_indices = greedy_bitset_run(oracle, candidates, candidate_masks, rng, profile, randomized=False)
    if len(best_indices) <= target_bound:
        return tuple(candidates[index] for index in best_indices)
    if 0 < profile.exact_max_universe >= oracle.total_requirements and time.monotonic() < deadline:
        exact_deadline = min(deadline, time.monotonic() + exact_search_seconds(oracle.problem.n))
        exact_indices = exact_branch_and_bound(oracle, candidate_masks, best_indices, exact_deadline)
        if exact_indices and len(exact_indices) <= len(best_indices):
            best_indices = exact_indices
    if len(best_indices) <= target_bound:
        return tuple(candidates[index] for index in best_indices)
    restart = 0
    while restart < profile.full_restarts and time.monotonic() < deadline:
        candidate_indices = greedy_bitset_run(oracle, candidates, candidate_masks, rng, profile, randomized=True)
        candidate_indices = prune_indices_by_masks(candidate_indices, candidate_masks, oracle.full_mask, rng)
        if len(candidate_indices) < len(best_indices):
            best_indices = candidate_indices
            if len(best_indices) <= target_bound:
                break
        restart += 1
    if deadline - time.monotonic() > 8.0:
        best_indices = large_neighborhood_search_indices(candidates, candidate_masks, oracle.full_mask, best_indices, rng, deadline)
    best_indices = improve_small_n_with_milp(oracle, candidate_masks, best_indices, deadline)
    best_indices = prune_indices_by_masks(best_indices, candidate_masks, oracle.full_mask, rng)
    return tuple(candidates[index] for index in best_indices)


def large_neighborhood_search_indices(
    candidates: Sequence[tuple[int, ...]],
    candidate_masks: Sequence[int],
    full_mask: int,
    initial_indices: Sequence[int],
    rng: random.Random,
    deadline: float,
) -> tuple[int, ...]:
    best = list(dict.fromkeys(initial_indices))
    if len(best) <= 2:
        return tuple(best)
    local_seconds = 48.0 if len(candidates) <= 1500 else 38.0
    local_deadline = min(deadline, time.monotonic() + local_seconds)
    while time.monotonic() < local_deadline:
        max_remove = min(max(8, len(best) // 3), 36, len(best) - 1)
        remove_count = rng.randint(2, max_remove)
        removed = set(rng.sample(best, remove_count))
        partial = [index for index in best if index not in removed]
        coverage = 0
        for index in partial:
            coverage |= candidate_masks[index]
        uncovered = full_mask & ~coverage
        additions: list[int] = []
        while uncovered and len(partial) + len(additions) < len(best):
            partial_set = set(partial + additions)
            scored: list[tuple[int, float, int]] = []
            for candidate_index, mask in enumerate(candidate_masks):
                if candidate_index in partial_set:
                    continue
                gain = count_bits(mask & uncovered)
                if gain <= 0:
                    continue
                scored.append((gain, rng.random(), candidate_index))
            if not scored:
                break
            scored.sort(reverse=True)
            best_gain = scored[0][0]
            top = [entry for entry in scored[: min(32, len(scored))] if entry[0] >= max(1, int(best_gain * 0.985))]
            selected_index = rng.choice(top or scored[:1])[2]
            additions.append(selected_index)
            uncovered &= ~candidate_masks[selected_index]
        if uncovered:
            continue
        candidate_solution = prune_indices_by_masks(partial + additions, candidate_masks, full_mask, rng)
        if len(candidate_solution) < len(best):
            best = list(candidate_solution)
            local_deadline = min(deadline, time.monotonic() + local_seconds)
    return tuple(best)


def improve_small_n_with_milp(
    oracle: CoverageOracle,
    candidate_masks: Sequence[int],
    initial_indices: Sequence[int],
    deadline: float,
    max_nnz: int = 8_000_000,
) -> tuple[int, ...]:
    if oracle.problem.n > 15:
        return tuple(initial_indices)
    remaining = deadline - time.monotonic()
    if remaining < 8.0:
        return tuple(initial_indices)
    estimated_nnz = len(candidate_masks) * oracle.block_cover_capacity
    if estimated_nnz > max_nnz:
        return tuple(initial_indices)
    time_fraction = 0.94 if oracle.problem.n <= 12 else 0.72
    time_budget = min(remaining * time_fraction, small_n_milp_seconds(oracle.problem.n))
    if time_budget < 2.0:
        return tuple(initial_indices)
    try:
        from scipy.optimize import Bounds, LinearConstraint, milp
        from scipy.sparse import coo_array
        import numpy as np
    except Exception:
        return tuple(initial_indices)

    rows: list[int] = []
    columns: list[int] = []
    for candidate_index, mask in enumerate(candidate_masks):
        pending = mask
        while pending:
            bit = pending & -pending
            rows.append(bit.bit_length() - 1)
            columns.append(candidate_index)
            pending ^= bit
    data = np.ones(len(rows), dtype=np.int8)
    matrix = coo_array(
        (data, (np.array(rows, dtype=np.int32), np.array(columns, dtype=np.int32))),
        shape=(oracle.total_requirements, len(candidate_masks)),
    ).tocsc()
    objective = np.ones(len(candidate_masks), dtype=np.float64)
    cover_constraints = LinearConstraint(matrix, lb=np.ones(oracle.total_requirements), ub=np.full(oracle.total_requirements, np.inf))
    target_size = max(lower_bound(oracle.problem), math.floor(len(initial_indices) * 0.90))
    if target_size < len(initial_indices):
        size_matrix = coo_array(np.ones((1, len(candidate_masks)), dtype=np.int8)).tocsc()
        size_constraint = LinearConstraint(size_matrix, lb=-np.inf, ub=target_size)
        feasibility_budget = min(time_budget * 0.48, 52.0)
        feasibility = milp(
            c=np.zeros(len(candidate_masks), dtype=np.float64),
            integrality=np.ones(len(candidate_masks), dtype=np.int8),
            bounds=Bounds(0, 1),
            constraints=(cover_constraints, size_constraint),
            options={"time_limit": feasibility_budget, "mip_rel_gap": 0.0, "presolve": True},
        )
        selected = selected_from_milp_result(feasibility)
        if selected and len(selected) < len(initial_indices) and covers_full_mask(selected, candidate_masks, oracle.full_mask):
            return selected
        time_budget -= feasibility_budget
        if time_budget < 2.0:
            return tuple(initial_indices)
    result = milp(
        c=objective,
        integrality=np.ones(len(candidate_masks), dtype=np.int8),
        bounds=Bounds(0, 1),
        constraints=cover_constraints,
        options={"time_limit": time_budget, "mip_rel_gap": 0.0, "presolve": True},
    )
    selected = selected_from_milp_result(result)
    if selected and len(selected) <= len(initial_indices):
        if covers_full_mask(selected, candidate_masks, oracle.full_mask):
            return selected
    return tuple(initial_indices)


def selected_from_milp_result(result: object) -> tuple[int, ...]:
    values = getattr(result, "x", None)
    if values is None:
        return tuple()
    return tuple(index for index, value in enumerate(values) if value >= 0.5)


def covers_full_mask(selected_indices: Sequence[int], candidate_masks: Sequence[int], full_mask: int) -> bool:
    coverage = 0
    for index in selected_indices:
        coverage |= candidate_masks[index]
    return coverage == full_mask


def small_n_milp_seconds(n: int) -> float:
    if n <= 10:
        return 12.0
    if n <= 12:
        return 112.0
    return 70.0


def should_use_subset_count_greedy(problem: Problem) -> bool:
    score_terms = sum(math.comb(problem.k, size) for size in range(problem.s, min(problem.j, problem.k) + 1))
    subset_terms = sum(math.comb(problem.n, size) for size in range(problem.s, problem.j + 1))
    candidate_count = math.comb(problem.n, problem.k)
    return candidate_count * score_terms <= 8_000_000 and subset_terms <= 360_000


def solve_with_subset_count_greedy(
    oracle: CoverageOracle,
    rng: random.Random,
    deadline: float,
) -> tuple[tuple[int, ...], ...]:
    problem = oracle.problem
    candidates = tuple(combinations(range(problem.n), problem.k))
    subset_sizes = tuple(range(problem.s, min(problem.j, problem.k) + 1))
    coefficients = intersection_coefficients(problem.s, min(problem.j, problem.k))
    uncovered_counts = {
        size: {sample_set: math.comb(problem.n - size, problem.j - size) for sample_set in combinations(range(problem.n), size)}
        for size in subset_sizes
    }
    uncovered_flags = bytearray(b"\x01") * oracle.total_requirements
    uncovered_count = oracle.total_requirements
    selected: list[tuple[int, ...]] = []
    target_bound = lower_bound(problem)
    while uncovered_count > 0:
        best_score = 0
        best_blocks: list[tuple[int, ...]] = []
        for block in candidates:
            score = subset_count_score(block, subset_sizes, coefficients, uncovered_counts)
            if score > best_score:
                best_score = score
                best_blocks = [block]
            elif score == best_score and score > 0:
                best_blocks.append(block)
        if best_score <= 0:
            break
        block = rng.choice(best_blocks[:64])
        selected.append(block)
        newly_covered = [index for index in oracle.block_cover_indices(block) if uncovered_flags[index]]
        for requirement_index in newly_covered:
            uncovered_flags[requirement_index] = 0
            uncovered_count -= 1
            requirement = oracle.requirements[requirement_index]
            for size in subset_sizes:
                for sample_set in combinations(requirement, size):
                    uncovered_counts[size][sample_set] -= 1
        if uncovered_count == 0 or len(selected) <= target_bound and uncovered_count == 0:
            break
        if time.monotonic() >= deadline and len(selected) >= target_bound:
            break
    return tuple(selected)


def intersection_coefficients(s: int, max_intersection: int) -> dict[int, int]:
    coefficients: dict[int, int] = {}
    for size in range(s, max_intersection + 1):
        previous = sum(coefficients[smaller] * math.comb(size, smaller) for smaller in range(s, size))
        coefficients[size] = 1 - previous
    return coefficients


def subset_count_score(
    block: tuple[int, ...],
    subset_sizes: Sequence[int],
    coefficients: dict[int, int],
    uncovered_counts: dict[int, dict[tuple[int, ...], int]],
) -> int:
    score = 0
    for size in subset_sizes:
        subset_total = sum(uncovered_counts[size][sample_set] for sample_set in combinations(block, size))
        score += coefficients[size] * subset_total
    return score


def exact_search_seconds(n: int) -> float:
    if n <= 9:
        return 1.0
    if n <= 12:
        return 2.0
    return 3.0


def greedy_bitset_run(
    oracle: CoverageOracle,
    candidates: Sequence[tuple[int, ...]],
    candidate_masks: Sequence[int],
    rng: random.Random,
    profile: SolverProfile,
    *,
    randomized: bool,
) -> tuple[int, ...]:
    uncovered = oracle.full_mask
    selected: list[int] = []
    while uncovered:
        scored: list[tuple[int, int]] = []
        best_score = 0
        for index, mask in enumerate(candidate_masks):
            gain = count_bits(mask & uncovered)
            if gain > 0:
                if not randomized:
                    if gain > best_score:
                        best_score = gain
                        scored = [(gain, index)]
                    elif gain == best_score:
                        scored.append((gain, index))
                else:
                    scored.append((gain, index))
                    best_score = max(best_score, gain)
        if best_score <= 0:
            break
        if randomized:
            scored.sort(reverse=True)
            threshold = max(1, int(best_score * 0.985))
            top = [entry for entry in scored[: profile.top_width * 4] if entry[0] >= threshold]
            gain, selected_index = rng.choice(top[: profile.top_width] or scored[:1])
        else:
            gain, selected_index = min(scored, key=lambda entry: candidates[entry[1]])
        selected.append(selected_index)
        uncovered &= ~candidate_masks[selected_index]
    return tuple(selected)


def exact_branch_and_bound(
    oracle: CoverageOracle,
    candidate_masks: Sequence[int],
    initial_indices: Sequence[int],
    deadline: float,
) -> tuple[int, ...]:
    if oracle.total_requirements > 1200 or len(candidate_masks) > 2000:
        return tuple(initial_indices)
    requirement_to_candidates: list[list[int]] = [[] for _ in range(oracle.total_requirements)]
    for candidate_index, mask in enumerate(candidate_masks):
        pending = mask
        while pending:
            bit = pending & -pending
            requirement_to_candidates[bit.bit_length() - 1].append(candidate_index)
            pending ^= bit
    max_gain = max(count_bits(mask) for mask in candidate_masks)
    best = list(initial_indices)
    seen: dict[int, int] = {}

    def choose_requirement(uncovered: int) -> int:
        best_requirement = -1
        best_count = sys.maxsize
        pending = uncovered
        while pending:
            bit = pending & -pending
            requirement = bit.bit_length() - 1
            count = sum(1 for index in requirement_to_candidates[requirement] if candidate_masks[index] & uncovered)
            if count < best_count:
                best_requirement = requirement
                best_count = count
                if count <= 1:
                    break
            pending ^= bit
        return best_requirement

    def search(chosen: list[int], uncovered: int) -> None:
        nonlocal best
        if time.monotonic() >= deadline:
            return
        if not uncovered:
            if len(chosen) < len(best):
                best = chosen.copy()
            return
        previous_depth = seen.get(uncovered)
        if previous_depth is not None and previous_depth <= len(chosen):
            return
        seen[uncovered] = len(chosen)
        lower = math.ceil(count_bits(uncovered) / max_gain)
        if len(chosen) + lower >= len(best):
            return
        requirement = choose_requirement(uncovered)
        if requirement < 0:
            return
        options = [
            (count_bits(candidate_masks[index] & uncovered), index)
            for index in requirement_to_candidates[requirement]
        ]
        options = [option for option in options if option[0] > 0]
        options.sort(reverse=True)
        for _, candidate_index in options:
            search(chosen + [candidate_index], uncovered & ~candidate_masks[candidate_index])

    search([], oracle.full_mask)
    return tuple(best)


def prune_indices_by_masks(
    selected_indices: Sequence[int],
    candidate_masks: Sequence[int],
    full_mask: int,
    rng: random.Random,
) -> tuple[int, ...]:
    kept = list(dict.fromkeys(selected_indices))
    changed = True
    while changed and len(kept) > 1:
        changed = False
        order = kept.copy()
        rng.shuffle(order)
        for candidate_index in order:
            trial = [index for index in kept if index != candidate_index]
            coverage = 0
            for index in trial:
                coverage |= candidate_masks[index]
            if coverage == full_mask:
                kept = trial
                changed = True
                break
    return tuple(kept)


def solve_with_candidate_pool(
    oracle: CoverageOracle,
    rng: random.Random,
    deadline: float,
    profile: SolverProfile,
) -> tuple[tuple[int, ...], ...]:
    best_solution: tuple[tuple[int, ...], ...] | None = None
    attempts = max(1, profile.full_restarts)
    for _ in range(attempts):
        if time.monotonic() >= deadline and best_solution is not None:
            break
        candidate_solution = candidate_pool_run(oracle, rng, deadline, profile)
        candidate_solution = prune_solution(oracle, candidate_solution, rng)
        if best_solution is None or len(candidate_solution) < len(best_solution):
            best_solution = candidate_solution
    return best_solution or tuple()


def candidate_pool_run(
    oracle: CoverageOracle,
    rng: random.Random,
    deadline: float,
    profile: SolverProfile,
) -> tuple[tuple[int, ...], ...]:
    problem = oracle.problem
    selected: list[tuple[int, ...]] = []
    usage = [0] * problem.n
    uncovered_mask: int | None = oracle.full_mask if oracle.use_masks else None
    uncovered_flags: bytearray | None = None if oracle.use_masks else bytearray(b"\x01") * oracle.total_requirements
    uncovered_count = oracle.total_requirements
    while uncovered_count > 0:
        sample_indices = sample_uncovered_indices(oracle, uncovered_mask, uncovered_flags, uncovered_count, profile.sampled_requirements, rng)
        pool = build_candidate_pool(oracle, sample_indices, usage, profile, rng)
        block = choose_best_pool_block(oracle, pool, sample_indices, uncovered_mask, uncovered_flags, profile, rng)
        if block is None:
            block = block_from_requirement(oracle.requirements[sample_indices[0]], problem, usage, rng)
        gain = oracle.score_block_exact(block, uncovered_mask, uncovered_flags)
        if gain <= 0:
            block = block_from_requirement(oracle.requirements[sample_indices[0]], problem, usage, rng)
        selected.append(block)
        for index in block:
            usage[index] += 1
        uncovered_mask, uncovered_count = oracle.mark_block_covered(block, uncovered_mask, uncovered_flags, uncovered_count)
        if time.monotonic() >= deadline and uncovered_count > 0:
            break
    return tuple(selected)


def sample_uncovered_indices(
    oracle: CoverageOracle,
    uncovered_mask: int | None,
    uncovered_flags: bytearray | None,
    uncovered_count: int,
    sample_size: int,
    rng: random.Random,
) -> list[int]:
    target = min(sample_size, uncovered_count)
    if target <= 0:
        return []
    if oracle.use_masks:
        if uncovered_mask is None:
            raise ValueError("uncovered_mask is required when masks are enabled")
        if uncovered_count <= target * 3:
            indices = oracle.uncovered_indices_from_mask(uncovered_mask)
            rng.shuffle(indices)
            return indices[:target]
        sampled: set[int] = set()
        while len(sampled) < target:
            index = rng.randrange(oracle.total_requirements)
            if (uncovered_mask >> index) & 1:
                sampled.add(index)
        return list(sampled)
    if uncovered_flags is None:
        raise ValueError("uncovered_flags is required when masks are disabled")
    if uncovered_count <= target * 3:
        indices = [index for index, is_uncovered in enumerate(uncovered_flags) if is_uncovered]
        rng.shuffle(indices)
        return indices[:target]
    sampled = set()
    while len(sampled) < target:
        index = rng.randrange(oracle.total_requirements)
        if uncovered_flags[index]:
            sampled.add(index)
    return list(sampled)


def build_candidate_pool(
    oracle: CoverageOracle,
    sample_indices: Sequence[int],
    usage: Sequence[int],
    profile: SolverProfile,
    rng: random.Random,
) -> set[tuple[int, ...]]:
    problem = oracle.problem
    pool: set[tuple[int, ...]] = set()
    all_indices = tuple(range(problem.n))
    for _ in range(max(20, profile.pool_size // 8)):
        pool.add(tuple(sorted(rng.sample(all_indices, problem.k))))
    for offset in range(problem.n):
        pool.add(tuple(sorted(((offset + step) % problem.n for step in range(problem.k)))))
        pool.add(tuple(sorted(((offset + 2 * step) % problem.n for step in range(problem.k)))))
    requirements = [oracle.requirements[index] for index in sample_indices]
    rng.shuffle(requirements)
    for requirement in requirements:
        if len(pool) >= profile.pool_size:
            break
        for _ in range(profile.generated_per_requirement):
            pool.add(block_from_requirement(requirement, problem, usage, rng))
            if len(pool) >= profile.pool_size:
                break
    while len(pool) < min(profile.pool_size, math.comb(problem.n, problem.k)):
        weighted = sorted(all_indices, key=lambda index: (usage[index], rng.random()))
        low_usage_prefix = weighted[: max(problem.k, problem.n // 2)]
        pool.add(tuple(sorted(rng.sample(low_usage_prefix, problem.k))))
    return pool


def block_from_requirement(
    requirement: tuple[int, ...],
    problem: Problem,
    usage: Sequence[int],
    rng: random.Random,
) -> tuple[int, ...]:
    max_inside = min(problem.j, problem.k)
    possible_inside = list(range(problem.s, max_inside + 1))
    weights = [inside_size * inside_size for inside_size in possible_inside]
    inside_size = rng.choices(possible_inside, weights=weights, k=1)[0]
    inside = set(rng.sample(requirement, inside_size))
    remaining = [index for index in range(problem.n) if index not in inside]
    remaining.sort(key=lambda index: (usage[index], rng.random()))
    block = tuple(sorted((*inside, *remaining[: problem.k - inside_size])))
    return block


def choose_best_pool_block(
    oracle: CoverageOracle,
    pool: Iterable[tuple[int, ...]],
    sample_indices: Sequence[int],
    uncovered_mask: int | None,
    uncovered_flags: bytearray | None,
    profile: SolverProfile,
    rng: random.Random,
) -> tuple[int, ...] | None:
    pool_tuple = tuple(pool)
    if not pool_tuple:
        return None
    if oracle.use_masks or oracle.block_cover_capacity <= 40_000:
        scored = [
            (oracle.score_block_exact(block, uncovered_mask, uncovered_flags), rng.random(), block)
            for block in pool_tuple
        ]
        scored = [entry for entry in scored if entry[0] > 0]
        if not scored:
            return None
        scored.sort(reverse=True)
        return scored[0][2]
    sample_requirements = tuple(oracle.requirements[index] for index in sample_indices)
    estimated = [
        (estimate_sample_score(block, sample_requirements, oracle.problem.s), rng.random(), block)
        for block in pool_tuple
    ]
    estimated.sort(reverse=True)
    finalists = [entry[2] for entry in estimated[: profile.exact_pool_limit]]
    exact = [
        (oracle.score_block_exact(block, uncovered_mask, uncovered_flags), rng.random(), block)
        for block in finalists
    ]
    exact = [entry for entry in exact if entry[0] > 0]
    if not exact:
        return None
    exact.sort(reverse=True)
    return exact[0][2]


def estimate_sample_score(block: tuple[int, ...], requirements: Sequence[tuple[int, ...]], s: int) -> int:
    block_set = set(block)
    return sum(1 for requirement in requirements if len(block_set.intersection(requirement)) >= s)


def repair_solution(
    oracle: CoverageOracle,
    selected_blocks: Sequence[tuple[int, ...]],
    rng: random.Random,
) -> tuple[tuple[int, ...], ...]:
    problem = oracle.problem
    repaired = list(dict.fromkeys(tuple(block) for block in selected_blocks))
    usage = [0] * problem.n
    for block in repaired:
        for index in block:
            usage[index] += 1
    if oracle.use_masks:
        coverage = 0
        for block in repaired:
            coverage |= oracle.block_mask(block)
        uncovered = oracle.full_mask & ~coverage
        while uncovered:
            bit = uncovered & -uncovered
            requirement = oracle.requirements[bit.bit_length() - 1]
            block = block_from_requirement(requirement, problem, usage, rng)
            repaired.append(block)
            for index in block:
                usage[index] += 1
            uncovered &= ~oracle.block_mask(block)
        return tuple(repaired)
    flags = bytearray(b"\x01") * oracle.total_requirements
    uncovered_count = oracle.total_requirements
    for block in repaired:
        _, uncovered_count = oracle.mark_block_covered(block, None, flags, uncovered_count)
    while uncovered_count > 0:
        requirement_index = next(index for index, is_uncovered in enumerate(flags) if is_uncovered)
        block = block_from_requirement(oracle.requirements[requirement_index], problem, usage, rng)
        repaired.append(block)
        for index in block:
            usage[index] += 1
        _, uncovered_count = oracle.mark_block_covered(block, None, flags, uncovered_count)
    return tuple(repaired)


def prune_solution(
    oracle: CoverageOracle,
    selected_blocks: Sequence[tuple[int, ...]],
    rng: random.Random,
) -> tuple[tuple[int, ...], ...]:
    unique_blocks = list(dict.fromkeys(tuple(block) for block in selected_blocks))
    if len(unique_blocks) <= 1:
        return tuple(unique_blocks)
    if oracle.use_masks:
        masks = tuple(oracle.block_mask(block) for block in unique_blocks)
        indices = prune_indices_by_masks(tuple(range(len(unique_blocks))), masks, oracle.full_mask, rng)
        return tuple(sorted((unique_blocks[index] for index in indices)))
    coverages = [tuple(oracle.block_cover_indices(block)) for block in unique_blocks]
    counts = [0] * oracle.total_requirements
    for coverage in coverages:
        for requirement_index in coverage:
            counts[requirement_index] += 1
    kept = [True] * len(unique_blocks)
    changed = True
    while changed:
        changed = False
        order = list(range(len(unique_blocks)))
        rng.shuffle(order)
        for block_index in order:
            if not kept[block_index]:
                continue
            coverage = coverages[block_index]
            if all(counts[requirement_index] > 1 for requirement_index in coverage):
                kept[block_index] = False
                for requirement_index in coverage:
                    counts[requirement_index] -= 1
                changed = True
                break
    return tuple(sorted(block for block, is_kept in zip(unique_blocks, kept) if is_kept))


def verify_solution(problem: Problem, index_blocks: Sequence[tuple[int, ...]]) -> bool:
    problem.validate()
    for block in index_blocks:
        if len(block) != problem.k or len(set(block)) != problem.k:
            return False
        if min(block) < 0 or max(block) >= problem.n:
            return False
    block_sets = tuple(set(block) for block in index_blocks)
    return all(
        any(len(block_set.intersection(requirement)) >= problem.s for block_set in block_sets)
        for requirement in combinations(range(problem.n), problem.j)
    )


def save_result(result: SolverResult, db_dir: Path, run_number: int) -> Path:
    db_dir.mkdir(parents=True, exist_ok=True)
    filename = (
        f"{result.problem.m}-{result.problem.n}-{result.problem.k}-"
        f"{result.problem.j}-{result.problem.s}-{run_number}-{len(result.blocks)}.txt"
    )
    path = db_dir / filename
    lines = [
        SYSTEM_TITLE,
        f"m={result.problem.m}, n={result.problem.n}, k={result.problem.k}, j={result.problem.j}, s={result.problem.s}",
        f"selected_n_samples={','.join(str(sample) for sample in result.samples)}",
        f"result_groups={len(result.blocks)}",
        f"lower_bound={result.lower_bound}",
        f"total_j_groups={result.total_requirements}",
        f"strategy={result.strategy}",
        f"elapsed_seconds={result.elapsed_seconds:.3f}",
        "groups:",
    ]
    lines.extend(f"{index}. {','.join(str(value) for value in block)}" for index, block in enumerate(result.blocks, 1))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def next_run_number(db_dir: Path, problem: Problem) -> int:
    if not db_dir.exists():
        return 1
    prefix = f"{problem.m}-{problem.n}-{problem.k}-{problem.j}-{problem.s}-"
    runs = []
    for path in db_dir.glob(f"{prefix}*.txt"):
        parts = path.stem.split("-")
        if len(parts) >= 7 and parts[5].isdigit():
            runs.append(int(parts[5]))
    return max(runs, default=0) + 1


def list_db_files(db_dir: Path) -> list[Path]:
    if not db_dir.exists():
        return []
    return sorted(path for path in db_dir.glob("*.txt") if path.is_file())


def resolve_db_file(db_dir: Path, name: str) -> Path:
    path = Path(name)
    if path.exists():
        return path
    candidate = db_dir / name
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"DB file not found: {name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=SYSTEM_TITLE)
    subparsers = parser.add_subparsers(dest="command")
    generate = subparsers.add_parser("generate", help="generate optimized k-sample groups")
    generate.add_argument("--m", type=int, required=True)
    generate.add_argument("--n", type=int, required=True)
    generate.add_argument("--k", type=int, required=True)
    generate.add_argument("--j", type=int, required=True)
    generate.add_argument("--s", type=int, required=True)
    generate.add_argument("--samples", help="comma-separated n samples; omitted means random selection from 1..m")
    generate.add_argument("--time-limit", type=float, default=110.0)
    generate.add_argument("--db-dir", type=Path, default=DEFAULT_DB_DIR)
    generate.add_argument("--show", action="store_true", help="print result groups after saving")
    list_command = subparsers.add_parser("list", help="list DB result files")
    list_command.add_argument("--db-dir", type=Path, default=DEFAULT_DB_DIR)
    show = subparsers.add_parser("show", help="show a DB result file")
    show.add_argument("file")
    show.add_argument("--db-dir", type=Path, default=DEFAULT_DB_DIR)
    delete = subparsers.add_parser("delete", help="delete a DB result file")
    delete.add_argument("file")
    delete.add_argument("--db-dir", type=Path, default=DEFAULT_DB_DIR)
    delete.add_argument("--yes", action="store_true", help="delete without confirmation")
    return parser


def run_generate(args: argparse.Namespace) -> int:
    problem = Problem(args.m, args.n, args.k, args.j, args.s)
    problem.validate()
    rng = random.Random()
    samples = parse_samples(args.samples, problem, rng)
    result = solve_problem(problem, samples, time_limit=args.time_limit)
    if not verify_solution(problem, result.index_blocks):
        raise RuntimeError("internal verification failed: generated groups do not satisfy the PDF rule")
    run_number = next_run_number(args.db_dir, problem)
    path = save_result(result, args.db_dir, run_number)
    print(SYSTEM_TITLE)
    print(f"Selected n samples: {','.join(str(sample) for sample in result.samples)}")
    print(f"Generated groups: {len(result.blocks)}")
    print(f"Counting lower bound: {result.lower_bound}")
    print(f"Total j groups covered: {result.total_requirements}")
    print(f"Strategy: {result.strategy}")
    print(f"Elapsed seconds: {result.elapsed_seconds:.3f}")
    print(f"DB file: {path}")
    if args.show:
        for index, block in enumerate(result.blocks, 1):
            print(f"{index}. {','.join(str(value) for value in block)}")
    return 0


def run_list(args: argparse.Namespace) -> int:
    files = list_db_files(args.db_dir)
    if not files:
        print("No DB files found.")
        return 0
    for path in files:
        print(path)
    return 0


def run_show(args: argparse.Namespace) -> int:
    path = resolve_db_file(args.db_dir, args.file)
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def run_delete(args: argparse.Namespace) -> int:
    path = resolve_db_file(args.db_dir, args.file)
    if not args.yes:
        answer = input(f"Delete {path}? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Cancelled.")
            return 0
    path.unlink()
    print(f"Deleted {path}")
    return 0


def prompt_int(name: str) -> int:
    while True:
        raw_value = input(f"{name}: ").strip()
        try:
            return int(raw_value)
        except ValueError:
            print("Please enter a positive integer.")


def interactive_menu() -> int:
    print(SYSTEM_TITLE)
    while True:
        print("\n1. Generate groups")
        print("2. List DB files")
        print("3. Show DB file")
        print("4. Delete DB file")
        print("5. Exit")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                namespace = argparse.Namespace(
                    m=prompt_int("m"),
                    n=prompt_int("n"),
                    k=prompt_int("k"),
                    j=prompt_int("j"),
                    s=prompt_int("s"),
                    samples=None,
                    time_limit=110.0,
                    db_dir=DEFAULT_DB_DIR,
                    show=True,
                )
                manual = input("Input n samples manually? [y/N] ").strip().lower()
                if manual in {"y", "yes"}:
                    namespace.samples = input("Samples, comma-separated: ").strip()
                run_generate(namespace)
            elif choice == "2":
                run_list(argparse.Namespace(db_dir=DEFAULT_DB_DIR))
            elif choice == "3":
                run_show(argparse.Namespace(db_dir=DEFAULT_DB_DIR, file=input("File name/path: ").strip()))
            elif choice == "4":
                run_delete(argparse.Namespace(db_dir=DEFAULT_DB_DIR, file=input("File name/path: ").strip(), yes=False))
            elif choice == "5":
                return 0
            else:
                print("Please choose 1, 2, 3, 4 or 5.")
        except Exception as exc:
            print(f"Error: {exc}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        return interactive_menu()
    try:
        if args.command == "generate":
            return run_generate(args)
        if args.command == "list":
            return run_list(args)
        if args.command == "show":
            return run_show(args)
        if args.command == "delete":
            return run_delete(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())