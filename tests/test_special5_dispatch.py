from __future__ import annotations

import random
from itertools import combinations

import numpy as np

from solver import CoveringDesignSolver as BaseSolver
from solver_special5_dispatch import CoveringDesignSolver as DispatchSolver
from special5_case_module import get_special5_case_spec, get_special5_groups, list_special5_keys


def _verify_cover(n: int, j: int, s: int, groups: list[list[int]]) -> bool:
    gsets = [set(g) for g in groups]
    for tgt in combinations(range(n), j):
        tset = set(tgt)
        if not any(len(tset & gset) >= s for gset in gsets):
            return False
    return True


def test_special5_cached_groups_are_compliant() -> None:
    for key in list_special5_keys():
        spec = get_special5_case_spec(*key)
        assert spec is not None
        groups = get_special5_groups(*key)
        assert groups is not None
        assert _verify_cover(spec.n, spec.j, spec.s, groups)
        assert len(groups) <= int(spec.baseline_blocks * 1.10 + 1e-9)


def test_dispatch_solver_hits_special_case_cache() -> None:
    random.seed(20260425)
    np.random.seed(20260425)
    solver = DispatchSolver(
        n=14,
        k=6,
        j=5,
        s=4,
        num_attempts=1,
        time_budget_sec=5.0,
    )
    solved = solver.solve()
    assert solved.verified
    assert solved.num_groups == 31


def test_dispatch_solver_fallback_keeps_main_behavior() -> None:
    random.seed(123456)
    np.random.seed(123456)
    base = BaseSolver(
        n=8,
        k=4,
        j=3,
        s=3,
        num_attempts=2,
        time_budget_sec=10.0,
    )
    base_res = base.solve()

    random.seed(123456)
    np.random.seed(123456)
    dispatch = DispatchSolver(
        n=8,
        k=4,
        j=3,
        s=3,
        num_attempts=2,
        time_budget_sec=10.0,
    )
    dispatch_res = dispatch.solve()

    assert base_res.num_groups == dispatch_res.num_groups
    assert base_res.verified == dispatch_res.verified
