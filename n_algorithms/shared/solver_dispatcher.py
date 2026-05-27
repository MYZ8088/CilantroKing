from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from n_algorithms.n15.solver import solve_n_15
from n_algorithms.n16.solver import solve_n_16


@dataclass(frozen=True)
class DispatchResult:
    index_blocks: tuple[tuple[int, ...], ...]
    strategy: str


@dataclass(frozen=True)
class SolverTools:
    lower_bound: Callable[..., int]
    count_bits: Callable[..., int]
    make_oracle: Callable[..., Any]
    profile_for_n: Callable[..., Any]
    replace_profile: Callable[..., Any]
    greedy_bitset_run: Callable[..., tuple[int, ...]]
    prune_indices_by_masks: Callable[..., tuple[int, ...]]
    exact_branch_and_bound: Callable[..., tuple[int, ...]]
    large_neighborhood_search_indices: Callable[..., tuple[int, ...]]
    covers_full_mask: Callable[..., bool]
    improve_with_ilp: Callable[..., tuple[int, ...]]
    solve_with_full_greedy: Callable[..., tuple[tuple[int, ...], ...]]
    should_use_subset_count_greedy: Callable[..., bool]
    solve_with_subset_count_greedy: Callable[..., tuple[tuple[int, ...], ...]]
    solve_with_candidate_pool: Callable[..., tuple[tuple[int, ...], ...]]


def dispatch_solver(problem: Any, oracle: Any, rng: Any, deadline: float, profile: Any, tools: SolverTools) -> DispatchResult:
    if problem.n == 15:
        blocks, strategy = solve_n_15(problem, oracle, rng, deadline, tools)
        return DispatchResult(index_blocks=blocks, strategy=strategy)
    if problem.n == 16:
        blocks, strategy = solve_n_16(problem, oracle, rng, deadline, tools)
        return DispatchResult(index_blocks=blocks, strategy=strategy)
    if problem.n < 17:
        raise ValueError("this trimmed project keeps only the dedicated n=15 and n=16 solvers for n <= 16")
    if problem.n == problem.k:
        return DispatchResult(index_blocks=(tuple(range(problem.n)),), strategy="exact-single-block")
    if problem.k == problem.j == problem.s:
        return DispatchResult(index_blocks=tuple(__import__("itertools").combinations(range(problem.n), problem.k)), strategy="exact-all-k-groups")
    if problem.n <= profile.full_greedy_max_n and oracle.use_masks:
        return DispatchResult(index_blocks=tools.solve_with_full_greedy(oracle, rng, deadline, profile), strategy="full-bitset-greedy")
    if tools.should_use_subset_count_greedy(problem):
        return DispatchResult(index_blocks=tools.solve_with_subset_count_greedy(oracle, rng, deadline), strategy="subset-count-greedy")
    return DispatchResult(index_blocks=tools.solve_with_candidate_pool(oracle, rng, deadline, profile), strategy="candidate-pool-greedy")