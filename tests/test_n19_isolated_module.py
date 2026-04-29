from __future__ import annotations

import pytest

from n19_adaptive_strategy import build_n19_features
from n19_adaptive_strategy import classify_n19_cluster
from n19_adaptive_strategy import select_n19_strategy_steps
from n19_jk_specialized_module import is_n19_jk_target_case
from n19_jk_specialized_module import is_n19_jk_small_s_case
from n19_jk_specialized_module import is_n19_jk_small_s_direct_case
from n19_jk_specialized_module import should_use_n19_jk_kminus1_sparse_tables
from n19_jk_specialized_module import should_use_n19_jk_direct_lane
from n19_jk_specialized_module import should_use_n19_jk_small_s_direct_lane
from solver_n19_isolated import CoveringDesignSolver


def test_n19_isolated_solver_rejects_other_n() -> None:
    with pytest.raises(ValueError):
        CoveringDesignSolver(n=18, k=7, j=7, s=6, num_attempts=1, time_budget_sec=1.0)


def test_n19_cluster_and_jk_guard() -> None:
    assert classify_n19_cluster(k=7, j=7, s=6) == "jk_near_dominating"
    assert is_n19_jk_target_case(n=19, k=7, j=7, s=6)
    assert not is_n19_jk_target_case(n=19, k=7, j=7, s=5)
    assert is_n19_jk_small_s_case(n=19, k=4, j=4, s=3)
    assert is_n19_jk_small_s_case(n=19, k=5, j=5, s=3)
    assert is_n19_jk_small_s_case(n=19, k=6, j=6, s=4)
    assert is_n19_jk_small_s_direct_case(n=19, k=4, j=4, s=3)
    assert is_n19_jk_small_s_direct_case(n=19, k=5, j=5, s=3)
    assert not is_n19_jk_small_s_direct_case(n=19, k=6, j=6, s=4)
    assert not is_n19_jk_small_s_case(n=19, k=7, j=7, s=4)


def test_n19_adaptive_steps_keep_jk_isolated() -> None:
    features = build_n19_features(
        n=19,
        k=7,
        j=7,
        s=6,
        num_targets=50388,
        num_cands=50388,
        interaction_scale=10,
        solution_len=1400,
    )
    assert features.family == "j_eq_k_noncontain_medium_n"
    assert select_n19_strategy_steps(features) == ["jk_bundle"]


def test_n19_direct_lane_guard_is_only_for_large_jk() -> None:
    solver_hit = CoveringDesignSolver(n=19, k=6, j=6, s=5, num_attempts=1, time_budget_sec=1.0)
    assert should_use_n19_jk_direct_lane(solver_hit)

    solver_large_k = CoveringDesignSolver(n=19, k=7, j=7, s=6, num_attempts=1, time_budget_sec=1.0)
    assert not should_use_n19_jk_direct_lane(solver_large_k)

    solver_miss = CoveringDesignSolver(n=19, k=7, j=7, s=5, num_attempts=1, time_budget_sec=1.0)
    assert not should_use_n19_jk_direct_lane(solver_miss)


def test_n19_small_s_direct_lane_guard_is_whitelisted() -> None:
    solver_443 = CoveringDesignSolver(n=19, k=4, j=4, s=3, num_attempts=1, time_budget_sec=30.0)
    assert should_use_n19_jk_small_s_direct_lane(solver_443)

    solver_553 = CoveringDesignSolver(n=19, k=5, j=5, s=3, num_attempts=1, time_budget_sec=30.0)
    assert should_use_n19_jk_small_s_direct_lane(solver_553)

    solver_664 = CoveringDesignSolver(n=19, k=6, j=6, s=4, num_attempts=1, time_budget_sec=30.0)
    assert not should_use_n19_jk_small_s_direct_lane(solver_664)


def test_n19_kminus1_sparse_tables_guard_is_large_k_only() -> None:
    solver_776 = CoveringDesignSolver(n=19, k=7, j=7, s=6, num_attempts=1, time_budget_sec=30.0)
    assert should_use_n19_jk_kminus1_sparse_tables(solver_776)

    solver_665 = CoveringDesignSolver(n=19, k=6, j=6, s=5, num_attempts=1, time_budget_sec=30.0)
    assert not should_use_n19_jk_kminus1_sparse_tables(solver_665)

    solver_775 = CoveringDesignSolver(n=19, k=7, j=7, s=5, num_attempts=1, time_budget_sec=30.0)
    assert not should_use_n19_jk_kminus1_sparse_tables(solver_775)
