from __future__ import annotations

from tools.rerun_selected_cases import RUN_FIELDNAMES, RunTask, failed_run_row
from tools.validate_all import Case


def test_failed_run_row_keeps_case_metadata() -> None:
    task = RunTask(
        run_index=3,
        input_case_id="15776",
        case=Case(order=305, n=15, k=7, j=7, s=6, baseline=180, t=1),
    )

    row = failed_run_row(task, "process pool died")

    assert set(RUN_FIELDNAMES).issuperset(row)
    assert row["run_index"] == 3
    assert row["input_case_id"] == "15776"
    assert row["case_order"] == 305
    assert row["case_id"] == "L_15_7_7_6"
    assert row["n"] == 15
    assert row["k"] == 7
    assert row["j"] == 7
    assert row["s"] == 6
    assert row["t"] == 1
    assert row["baseline_blocks"] == 180
    assert row["actual_blocks"] == ""
    assert row["error"] == "process pool died"