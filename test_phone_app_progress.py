from __future__ import annotations

from phone_app import DEFAULT_PROGRESS_CEILING, format_progress_snapshot
from solver import SolverProgress


def test_progress_snapshot_does_not_treat_zero_remaining_as_complete() -> None:
    snapshot = format_progress_snapshot(
        SolverProgress(
            phase="start",
            message="Starting solver",
            remaining=0,
            total=120,
            elapsed=1.0,
        ),
        time_budget_sec=120,
    )

    assert 0 < snapshot.percent < 100
    assert snapshot.percent < DEFAULT_PROGRESS_CEILING
    assert snapshot.message == "Starting solver"


def test_progress_snapshot_uses_real_remaining_when_available() -> None:
    snapshot = format_progress_snapshot(
        SolverProgress(
            phase="greedy",
            message="Covering targets",
            solution_size=8,
            remaining=25,
            total=100,
            elapsed=3.5,
        ),
        time_budget_sec=120,
    )

    assert snapshot.percent == 75.0
    assert "75/100 targets covered" in snapshot.detail
    assert "8 groups" in snapshot.detail