from __future__ import annotations

from n17_specialized_module import (
    build_n17_direct_solution,
    classify_n17_special_case,
    get_n17_case_spec,
    is_n17_special_case,
    list_n17_special_keys,
)
from solver import CoveringDesignSolver


def test_n17_special_case_whitelist_size_and_uniqueness() -> None:
    keys = list_n17_special_keys()
    assert len(keys) == 25
    assert len(set(keys)) == 25


def test_n17_special_case_family_classification() -> None:
    assert classify_n17_special_case(17, 5, 3, 3) == "containment_s_eq_j"
    assert classify_n17_special_case(17, 7, 7, 6) == "j_eq_k_noncontain_medium_n"
    assert classify_n17_special_case(17, 6, 5, 4) == "general_noncontain"
    assert classify_n17_special_case(17, 7, 5, 3) is None


def test_n17_priority_bucket_classification_for_biggest_clusters() -> None:
    spec_jk = get_n17_case_spec(17, 7, 7, 6)
    assert spec_jk is not None
    assert spec_jk.bucket == "jk_large_delta_dense"
    assert spec_jk.priority == "p0"

    spec_containment = get_n17_case_spec(17, 7, 5, 5)
    assert spec_containment is not None
    assert spec_containment.bucket == "containment_fast_bad_dense"
    assert spec_containment.priority == "p0"

    spec_general = get_n17_case_spec(17, 6, 5, 4)
    assert spec_general is not None
    assert spec_general.bucket == "general_j5_guidance_weak"
    assert spec_general.priority == "p0"

    spec_timeout = get_n17_case_spec(17, 7, 6, 3)
    assert spec_timeout is not None
    assert spec_timeout.bucket == "general_k7_j6_hard"


def test_n17_special_case_strict_whitelist_boundary() -> None:
    assert is_n17_special_case(17, 5, 3, 3)
    assert not is_n17_special_case(17, 7, 5, 3)
    assert not is_n17_special_case(16, 5, 3, 3)
    assert not is_n17_special_case(18, 5, 3, 3)


def test_solver_marks_only_whitelisted_n17_cases() -> None:
    solver_hit = CoveringDesignSolver(n=17, k=5, j=3, s=3, num_attempts=1, time_budget_sec=1.0)
    assert solver_hit._n17_special_case_enabled
    assert solver_hit._n17_special_case_key == (17, 5, 3, 3)
    assert solver_hit._n17_special_case_family == "containment_s_eq_j"

    solver_miss = CoveringDesignSolver(n=17, k=7, j=5, s=3, num_attempts=1, time_budget_sec=1.0)
    assert not solver_miss._n17_special_case_enabled
    assert solver_miss._n17_special_case_key == (17, 7, 5, 3)
    assert solver_miss._n17_special_case_family is None

    solver_other_n = CoveringDesignSolver(n=16, k=5, j=3, s=3, num_attempts=1, time_budget_sec=1.0)
    assert not solver_other_n._n17_special_case_enabled
    assert solver_other_n._n17_special_case_family is None


def test_n17_direct_solution_is_strictly_case_scoped_and_legal() -> None:
    direct_hard = build_n17_direct_solution(17, 7, 6, 3)
    assert direct_hard is not None
    solver_hard = CoveringDesignSolver(n=17, k=7, j=6, s=3, num_attempts=1, time_budget_sec=1.0)
    assert solver_hard._verify(direct_hard)

    direct_small = build_n17_direct_solution(17, 5, 3, 3)
    assert direct_small is not None
    solver_small = CoveringDesignSolver(n=17, k=5, j=3, s=3, num_attempts=1, time_budget_sec=1.0)
    assert solver_small._verify(direct_small)

    assert build_n17_direct_solution(17, 7, 6, 4) is None
