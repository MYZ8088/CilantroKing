"""Shared app boundary helpers for the Optimal Samples Selection UI."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from math import comb
from typing import Any, Mapping


DEFAULT_TIMEOUT_SEC = 120


@dataclass(frozen=True)
class SolveRequest:
    population_size: int
    sample_size: int
    group_size: int
    test_size: int
    threshold: int
    cover_count: int
    timeout_sec: int
    selection_mode: str
    selected_samples: tuple[int, ...]

    def params(self) -> dict[str, int]:
        return {
            "m": self.population_size,
            "n": self.sample_size,
            "k": self.group_size,
            "j": self.test_size,
            "s": self.threshold,
            "t": self.cover_count,
            "timeout": self.timeout_sec,
        }


def validate_solve_payload(payload: Mapping[str, Any]) -> SolveRequest:
    population_size = _payload_int(payload, "m")
    sample_size = _payload_int(payload, "n")
    group_size = _payload_int(payload, "k")
    test_size = _payload_int(payload, "j")
    threshold = _payload_int(payload, "s")
    cover_count = _payload_int(payload, "t", default=1)
    timeout_sec = _payload_int(payload, "timeout", default=DEFAULT_TIMEOUT_SEC)
    raw_mode = str(payload.get("mode", "random")).strip().lower()
    selection_mode = "manual" if raw_mode in {"manual", "input"} else raw_mode

    if not 45 <= population_size <= 54:
        raise ValueError("m must be between 45 and 54")
    if not 7 <= sample_size <= 25:
        raise ValueError("n must be between 7 and 25")
    if not 4 <= group_size <= 7:
        raise ValueError("k must be between 4 and 7")
    if not 3 <= threshold <= 7:
        raise ValueError("s must be between 3 and 7")
    if not threshold <= test_size <= group_size:
        raise ValueError(f"Need s({threshold}) <= j({test_size}) <= k({group_size})")
    if sample_size > population_size:
        raise ValueError(f"n({sample_size}) cannot exceed m({population_size})")
    max_cover_count = comb(test_size, threshold)
    if not 1 <= cover_count <= max_cover_count:
        raise ValueError(f"t must be between 1 and C({test_size},{threshold})={max_cover_count}")
    if not 30 <= timeout_sec <= 600:
        raise ValueError("Timeout must be between 30 and 600 seconds")
    if selection_mode not in {"random", "manual"}:
        raise ValueError("mode must be random or manual")

    selected_samples: tuple[int, ...] = tuple()
    if selection_mode == "manual":
        selected_samples = parse_manual_samples(
            payload.get("samples", ""),
            population_size=population_size,
            sample_size=sample_size,
        )

    return SolveRequest(
        population_size=population_size,
        sample_size=sample_size,
        group_size=group_size,
        test_size=test_size,
        threshold=threshold,
        cover_count=cover_count,
        timeout_sec=timeout_sec,
        selection_mode=selection_mode,
        selected_samples=selected_samples,
    )


def parse_manual_samples(
    raw_samples: Any,
    *,
    population_size: int,
    sample_size: int,
) -> tuple[int, ...]:
    if isinstance(raw_samples, str):
        tokens = [token for token in re.split(r"[\s,]+", raw_samples.strip()) if token]
    elif isinstance(raw_samples, (list, tuple)):
        tokens = list(raw_samples)
    else:
        raise ValueError("samples must be a comma-separated string or a list")

    if not tokens:
        raise ValueError("Please enter sample numbers")

    try:
        samples = tuple(int(token) for token in tokens)
    except (TypeError, ValueError):
        raise ValueError("All sample values must be integers") from None

    if len(samples) != sample_size:
        raise ValueError(f"Expected {sample_size} sample numbers, got {len(samples)}")
    if len(set(samples)) != sample_size:
        raise ValueError("Each sample number must be unique")
    if any(sample < 1 or sample > population_size for sample in samples):
        raise ValueError(f"All samples must be between 1 and {population_size}")
    return tuple(sorted(samples))


def select_samples_for_request(
    request: SolveRequest,
    sample_source: random.Random | None = None,
) -> tuple[int, ...]:
    if request.selection_mode == "manual":
        return request.selected_samples
    chooser = sample_source if sample_source is not None else random
    return tuple(sorted(chooser.sample(range(1, request.population_size + 1), request.sample_size)))


def groups_for_samples(
    groups: list[list[int]] | tuple[tuple[int, ...], ...],
    samples: tuple[int, ...],
) -> list[list[int]]:
    mapped_groups: list[list[int]] = []
    for group in groups:
        mapped_group: list[int] = []
        for solver_index in group:
            index = int(solver_index)
            if index < 0 or index >= len(samples):
                raise ValueError(f"Solver group index {index} is outside selected samples")
            mapped_group.append(int(samples[index]))
        mapped_groups.append(mapped_group)
    return mapped_groups


def serialize_solver_result(
    *,
    request: SolveRequest,
    solver_result: Any,
    run_number: int,
    stop_reason: str,
) -> dict[str, Any]:
    index_groups = _solver_index_groups(solver_result)
    real_groups = groups_for_samples(index_groups, request.selected_samples)
    num_groups = int(getattr(solver_result, "num_groups", len(real_groups)))
    filename = (
        f"{request.population_size}-{request.sample_size}-{request.group_size}-"
        f"{request.test_size}-{request.threshold}-{run_number}-{num_groups}"
    )
    first_legal_elapsed = getattr(solver_result, "first_legal_elapsed", None)
    return {
        "filename": filename,
        "run_number": run_number,
        "params": request.params(),
        "selected_samples": list(request.selected_samples),
        "groups": real_groups,
        "num_groups": num_groups,
        "elapsed_sec": round(float(getattr(solver_result, "elapsed", 0.0)), 6),
        "first_legal_elapsed_sec": (
            round(float(first_legal_elapsed), 6) if first_legal_elapsed is not None else None
        ),
        "verified": bool(getattr(solver_result, "verified", False)),
        "route_module": str(getattr(solver_result, "route_module", "")),
        "route_case": getattr(solver_result, "route_case", None),
        "solution_source": str(getattr(solver_result, "solution_source", "search")),
        "stop_reason": stop_reason,
        "stored_filename": None,
        "verification": None,
    }


def _payload_int(payload: Mapping[str, Any], key: str, default: int | None = None) -> int:
    raw_value = payload.get(key, default)
    if raw_value is None:
        raise ValueError(f"{key} is required")
    if isinstance(raw_value, bool):
        raise ValueError(f"{key} must be an integer")
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        raise ValueError(f"{key} must be an integer") from None


def _solver_index_groups(solver_result: Any) -> list[list[int]]:
    if hasattr(solver_result, "preview_groups"):
        groups = solver_result.preview_groups(None)
    else:
        groups = getattr(solver_result, "groups", [])
    return [[int(value) for value in group] for group in groups]