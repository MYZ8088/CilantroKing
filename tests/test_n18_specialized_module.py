from n18_specialized_module import (
    get_n18_case_spec,
    is_n18_special_case,
    run_n18_specialized_module,
)
from solver import CoveringDesignSolver


def test_n18_special_case_guard() -> None:
    assert is_n18_special_case(18, 7, 5, 5)
    assert not is_n18_special_case(17, 7, 5, 5)
    assert not is_n18_special_case(19, 7, 5, 5)


def test_n18_case_spec_family_and_bucket() -> None:
    spec = get_n18_case_spec(18, 7, 5, 5)
    assert spec is not None
    assert spec.family == "containment_s_eq_j"
    assert spec.bucket == "containment_dense"
    assert spec.strategy_profile.strategy_key == "n18_containment_dense_v1"

    spec2 = get_n18_case_spec(18, 7, 6, 5)
    assert spec2 is not None
    assert spec2.family == "general_noncontain"
    assert spec2.bucket == "general_k7"
    assert spec2.strategy_profile.strategy_key == "n18_general_k7_v1"

    spec3 = get_n18_case_spec(18, 7, 6, 4)
    assert spec3 is not None
    assert spec3.family == "general_noncontain"
    assert spec3.bucket == "general_k7_j6_local"
    assert spec3.strategy_profile.strategy_key == "n18_general_k7_j6_local_v1"


def test_n18_jk_case_uses_feature_adaptive_strategy() -> None:
    spec = get_n18_case_spec(18, 7, 7, 6)
    assert spec is not None
    assert spec.bucket == "jk_dense_compress"
    assert spec.feature_profile.one_block_hit_count == 77
    assert spec.strategy_profile.strategy_key == "n18_jk_dense_compress_v1"

    spec_small = get_n18_case_spec(18, 4, 4, 3)
    assert spec_small is not None
    assert spec_small.bucket == "jk_dense_compress"
    assert spec_small.feature_profile.candidate_count == 3060
    assert spec_small.strategy_profile.strategy_key == "n18_jk_dense_small_candidate_v1"

    spec2 = get_n18_case_spec(18, 7, 7, 4)
    assert spec2 is not None
    assert spec2.bucket == "jk_small_target_exactish"
    assert spec2.feature_profile.one_block_hit_count == 5775
    assert spec2.strategy_profile.strategy_key == "n18_jk_small_target_exactish_v1"


def test_solver_n18_dispatch_only_for_n18() -> None:
    solver = CoveringDesignSolver(n=17, k=7, j=5, s=5, num_attempts=1, time_budget_sec=1.0)
    sentinel = [1, 2, 3]
    assert solver._phase_n18_specialized_module_dispatch(sentinel) is sentinel


def test_n18_jk_dense_strategy_executes_pipeline() -> None:
    class FakeSolver:
        def __init__(self) -> None:
            self.n = 18
            self.k = 7
            self.j = 7
            self.s = 6
            self.events: list[str] = []

        def _time_remaining_sec(self) -> float:
            return 20.0

        def _report(self, phase: str, message: str) -> None:
            self.events.append(f"{phase}:{message}")

        def _phase_g_try_target_len(
            self,
            start_masks: list[int],
            target_len: int,
            budget_sec: float,
        ) -> list[int] | None:
            if target_len == len(start_masks) - 1:
                return start_masks[:-1]
            return None

        def _phase_i_full_cp_sat_module(self, sol: list[int], *, hard_case: bool) -> list[int]:
            assert hard_case is True
            return sol[:-1]

        def _verify(self, masks: list[int]) -> bool:
            return True

    solver = FakeSolver()
    result = run_n18_specialized_module(solver, list(range(30)))
    assert len(result) < 30
    assert any("jk-dense" in event for event in solver.events)


def test_n18_containment_dense_strategy_executes_pipeline() -> None:
    class FakeSolver:
        def __init__(self) -> None:
            self.n = 18
            self.k = 7
            self.j = 5
            self.s = 5
            self._containment = True
            self._deadline_at = 1.0
            self._cov_table = [1]
            self._inv_table = [1]
            self.events: list[str] = []

        def _time_remaining_sec(self) -> float:
            return 20.0

        def _report(self, phase: str, message: str) -> None:
            self.events.append(f"{phase}:{message}")

        def _phase_g_try_target_len(
            self,
            start_masks: list[int],
            target_len: int,
            budget_sec: float,
        ) -> list[int] | None:
            if target_len == len(start_masks) - 1:
                return start_masks[:-1]
            return None

        def _phase_c_has_time(self, minimum_sec: float) -> bool:
            return True

        def _build_cyclic_orbits(self) -> list[list[int]]:
            return [[0], [1]]

        @property
        def num_cands(self) -> int:
            return 2

        @property
        def cand_masks(self) -> list[int]:
            return [1, 2]

        def _local_search(self, sol: list[int]) -> list[int]:
            return sol

        def _phase_k_containment_iterative_sat_refine(self, sol: list[int]) -> list[int]:
            return sol

        def _verify(self, masks: list[int]) -> bool:
            return True

    solver = FakeSolver()
    result = run_n18_specialized_module(solver, list(range(30)))
    assert len(result) < 30
    assert any("containment" in event for event in solver.events)


def test_n18_general_core_strategy_executes_pipeline() -> None:
    class FakeSolver:
        def __init__(self) -> None:
            self.n = 18
            self.k = 6
            self.j = 5
            self.s = 4
            self._containment = False
            self._deadline_at = 1.0
            self._cov_table = [1]
            self._inv_table = [1]
            self.events: list[str] = []

        def _time_remaining_sec(self) -> float:
            return 20.0

        def _report(self, phase: str, message: str) -> None:
            self.events.append(f"{phase}:{message}")

        def _phase_g_try_target_len(
            self,
            start_masks: list[int],
            target_len: int,
            budget_sec: float,
        ) -> list[int] | None:
            if target_len == len(start_masks) - 1:
                return start_masks[:-1]
            return None

        def _phase_k_general_iterative_sat_refine(self, sol: list[int]) -> list[int]:
            return sol

        def _verify(self, masks: list[int]) -> bool:
            return True

    solver = FakeSolver()
    result = run_n18_specialized_module(solver, list(range(30)))
    assert len(result) < 30
    assert any("general" in event for event in solver.events)
