from __future__ import annotations

from types import SimpleNamespace

import pytest

from app_core import groups_for_samples, serialize_solver_result, validate_solve_payload


def test_validate_solve_payload_accepts_manual_pdf_shape() -> None:
    request = validate_solve_payload(
        {
            "m": 45,
            "n": 8,
            "k": 6,
            "j": 5,
            "s": 5,
            "t": 1,
            "timeout": 30,
            "mode": "manual",
            "samples": "1, 2, 3, 4, 5, 6, 7, 8",
        }
    )

    assert request.population_size == 45
    assert request.sample_size == 8
    assert request.group_size == 6
    assert request.test_size == 5
    assert request.threshold == 5
    assert request.cover_count == 1
    assert request.selected_samples == (1, 2, 3, 4, 5, 6, 7, 8)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("m", 44, "m must be between 45 and 54"),
        ("n", 26, "n must be between 7 and 25"),
        ("k", 8, "k must be between 4 and 7"),
        ("s", 2, "s must be between 3 and 7"),
    ],
)
def test_validate_solve_payload_rejects_pdf_range_errors(field: str, value: int, message: str) -> None:
    payload = {
        "m": 45,
        "n": 8,
        "k": 6,
        "j": 5,
        "s": 5,
        "mode": "random",
        "timeout": 30,
    }

    with pytest.raises(ValueError, match=message):
        validate_solve_payload({**payload, field: value})


def test_validate_solve_payload_rejects_duplicate_manual_samples() -> None:
    with pytest.raises(ValueError, match="Each sample number must be unique"):
        validate_solve_payload(
            {
                "m": 45,
                "n": 8,
                "k": 6,
                "j": 5,
                "s": 5,
                "mode": "manual",
                "timeout": 30,
                "samples": [1, 2, 3, 4, 5, 6, 7, 7],
            }
        )


def test_groups_for_samples_maps_solver_indices_to_real_numbers() -> None:
    samples = (11, 13, 17, 19, 23, 29, 31, 37)
    groups = [[0, 1, 2, 3, 4, 5], [2, 3, 4, 5, 6, 7]]

    assert groups_for_samples(groups, samples) == [
        [11, 13, 17, 19, 23, 29],
        [17, 19, 23, 29, 31, 37],
    ]


def test_serialize_solver_result_includes_pdf_filename_shape() -> None:
    request = validate_solve_payload(
        {
            "m": 45,
            "n": 8,
            "k": 6,
            "j": 5,
            "s": 5,
            "mode": "manual",
            "timeout": 30,
            "samples": "1,2,3,4,5,6,7,8",
        }
    )
    solver_result = SimpleNamespace(
        groups=[[0, 1, 2, 3, 4, 5]],
        num_groups=1,
        elapsed=0.25,
        verified=False,
        first_legal_elapsed=0.2,
        route_module="n_algorithms.n08.solver",
        solution_source="search",
        route_case="L(8,6,5,5)",
        group_masks=None,
        preview_groups=lambda limit=None: [[0, 1, 2, 3, 4, 5]],
    )

    payload = serialize_solver_result(
        request=request,
        solver_result=solver_result,
        run_number=3,
        stop_reason="completed",
    )

    assert payload["filename"] == "45-8-6-5-5-3-1"
    assert payload["groups"] == [[1, 2, 3, 4, 5, 6]]
    assert payload["selected_samples"] == [1, 2, 3, 4, 5, 6, 7, 8]
    assert payload["verified"] is False