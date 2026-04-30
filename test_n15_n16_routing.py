from __future__ import annotations

import random
import time
from dataclasses import dataclass
from itertools import combinations
from typing import Any

from n_algorithms.n16 import solver as n16_solver
from n_algorithms.shared.optimal_samples import Problem, verify_solution
from solver import CoveringDesignSolver


@dataclass(frozen=True)
class RecursiveProblem:
    m: int
    n: int
    k: int
    j: int
    s: int


class RecursiveTools:
    def make_oracle(self, problem: RecursiveProblem) -> object:
        return object()


def test_n15_and_n16_route_to_dedicated_root_solvers() -> None:
    cases = (
        (15, 7, 6, 3, "n_algorithms.n15.solver", 2),
        (16, 7, 7, 3, "n_algorithms.n16.solver", 2),
    )
    for n, k, j, s, route_module, expected_at_most in cases:
        solver = CoveringDesignSolver(
            n=n,
            k=k,
            j=j,
            s=s,
            num_attempts=1,
            time_budget_sec=10,
            skip_final_verify=False,
        )
        result = solver.solve()

        assert result.route_module == route_module
        assert result.verified
        assert result.num_groups <= expected_at_most
        assert verify_solution(
            Problem(45, n, k, j, s),
            tuple(tuple(group) for group in result.groups),
        )


def test_n16_recursive_construction_splits_to_n15_subproblems(monkeypatch: Any) -> None:
    calls: list[tuple[int, int, int, int]] = []

    def fake_solve_n_le_16_internal(
        problem: RecursiveProblem,
        oracle: object,
        rng: random.Random,
        deadline: float,
        tools: RecursiveTools,
    ) -> tuple[tuple[tuple[int, ...], ...], str]:
        calls.append((problem.n, problem.k, problem.j, problem.s))
        if problem.k == 5:
            return (((0, 1, 2, 3, 4),), "fake-first")
        return (((0, 1, 2, 3),), "fake-second")

    monkeypatch.setattr(
        n16_solver,
        "solve_n_le_16_internal",
        fake_solve_n_le_16_internal,
    )

    indices = n16_solver.recursive_covering_indices(
        n16_solver.N_SOLVER_CONFIGS[16],
        RecursiveProblem(45, 16, 5, 4, 4),
        random.Random(0),
        time.monotonic() + 30.0,
        RecursiveTools(),
    )
    candidates = tuple(combinations(range(16), 5))
    blocks = tuple(candidates[index] for index in indices)

    assert calls == [(15, 5, 4, 4), (15, 4, 3, 3)]
    assert blocks == ((0, 1, 2, 3, 4), (0, 1, 2, 3, 15))


def test_n19_routes_to_dedicated_solver() -> None:
    solver = CoveringDesignSolver(
        n=19,
        k=4,
        j=4,
        s=4,
        num_attempts=1,
        time_budget_sec=10,
        skip_final_verify=True,
    )
    result = solver.solve()

    assert result.route_module == "n_algorithms.n19.solver"
    assert result.num_groups == 3876