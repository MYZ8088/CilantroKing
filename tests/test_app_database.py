"""前端交互回归测试：验证轻量数据库查询和后台校验辅助函数。"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app_clean import _build_verified_result
from database import ResultDatabase
from solver import CoveringDesignSolver, SolverResult


def test_database_summary_and_count_queries(tmp_path) -> None:
    db = ResultDatabase(str(tmp_path / "results.db"))

    db.save(
        45, 7, 6, 5, 5,
        samples=[1, 2, 3, 4, 5, 6, 7],
        groups=[[1, 2, 3, 4, 5, 6]],
        elapsed_time=1.25,
        solution_found_time=0.8,
    )
    db.save(
        45, 7, 6, 5, 5,
        samples=[1, 2, 3, 4, 5, 6, 7],
        groups=[[2, 3, 4, 5, 6, 7]],
        elapsed_time=1.5,
        solution_found_time=1.0,
    )
    db.save(
        46, 8, 6, 5, 5,
        samples=[1, 2, 3, 4, 5, 6, 7, 8],
        groups=[[1, 2, 3, 4, 5, 6]],
        elapsed_time=2.0,
        solution_found_time=1.2,
    )

    summaries = db.list_summaries()

    assert len(summaries) == 3
    assert {item.num_groups for item in summaries} == {1}
    assert db.count_by_params(45, 7, 6, 5, 5) == 2
    assert db.count_by_params(46, 8, 6, 5, 5) == 1


def test_build_verified_result_keeps_solution_shape() -> None:
    solver = CoveringDesignSolver(n=7, k=6, j=5, s=5, num_attempts=1)
    result = solver.solve()
    pending = SolverResult(
        groups=result.groups,
        num_groups=result.num_groups,
        elapsed=result.elapsed,
        verified=False,
        first_legal_elapsed=result.first_legal_elapsed,
        groups_complete=result.groups_complete,
        group_masks=result.group_masks,
    )

    verified = _build_verified_result(
        {"m": 45, "n": 7, "k": 6, "j": 5, "s": 5, "timeout": 150},
        pending,
    )

    assert verified.verified
    assert verified.num_groups == pending.num_groups
    assert verified.groups == pending.groups
