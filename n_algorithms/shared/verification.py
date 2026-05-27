from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Iterable

from solver import CoveringDesignSolver, elements_to_mask


@dataclass(frozen=True)
class VerificationOutcome:
    verified: bool
    method: str
    elapsed_sec: float


def result_masks(result: Any) -> tuple[int, ...]:
    if result.group_masks is not None:
        return tuple(int(mask) for mask in result.group_masks)
    return tuple(elements_to_mask(group) for group in result.groups)


def verify_masks_with_solver(
    *,
    n: int,
    k: int,
    j: int,
    s: int,
    masks: Iterable[int],
    t: int = 1,
) -> VerificationOutcome:
    started_at = time.time()
    mask_list = [int(mask) for mask in masks]
    temp_solver = CoveringDesignSolver(
        n=n,
        k=k,
        j=j,
        s=s,
        t=t,
        num_attempts=1,
        skip_final_verify=True,
    )
    if int(t) > 1 and hasattr(temp_solver, "_tcovering_solver"):
        verified = bool(temp_solver._tcovering_solver._verify(mask_list))
        method = "tcovering_solver._verify"
    else:
        verified = bool(temp_solver._verify(mask_list))
        method = "CoveringDesignSolver._verify"
    return VerificationOutcome(
        verified=verified,
        method=method,
        elapsed_sec=time.time() - started_at,
    )