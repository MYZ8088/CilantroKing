"""Root routing facade for covering-design solvers.

All concrete n-specific and shared algorithms live under ``n_algorithms``.
This module keeps the historical public API while only dispatching user input
values to the proper implementation module.
"""

from __future__ import annotations

import importlib
from typing import Callable

from n_algorithms.shared.solver_core import (
    SolverProgress,
    SolverResult,
    _add_windows_cuda_dll_dirs,
    cp,
    cp_model,
    elements_to_mask,
    mask_to_elements,
    popcount_uint32,
)


def solver_module_name(n: int, t: int = 1) -> str:
    n_value = int(n)
    if int(t) > 1:
        return "n_algorithms.shared.solver_core"
    if 7 <= n_value <= 19:
        return f"n_algorithms.n{n_value:02d}.solver"
    return "n_algorithms.shared.solver_core"


class CoveringDesignSolver:
    """Compatibility facade that dispatches to the selected solver module."""

    def __init__(
        self,
        n: int,
        k: int,
        j: int,
        s: int,
        t: int = 1,
        *,
        progress_cb: Callable[[SolverProgress], None] | None = None,
        cancel_fn: Callable[[], bool] | None = None,
        num_attempts: int = 3,
        time_budget_sec: float | None = None,
        skip_final_verify: bool = False,
    ) -> None:
        self.n = int(n)
        self.k = int(k)
        self.j = int(j)
        self.s = int(s)
        self.t = int(t)
        self._kwargs = {
            "n": n,
            "k": k,
            "j": j,
            "s": s,
            "t": t,
            "progress_cb": progress_cb,
            "cancel_fn": cancel_fn,
            "num_attempts": num_attempts,
            "time_budget_sec": time_budget_sec,
            "skip_final_verify": skip_final_verify,
        }
        self.route_module = solver_module_name(self.n, self.t)
        module = importlib.import_module(self.route_module)
        solver_cls = getattr(module, "CoveringDesignSolver")
        self._solver = solver_cls(**self._kwargs)

    def solve(self) -> SolverResult:
        result = self._solver.solve()
        if not result.route_module:
            result.route_module = self.route_module
        if result.route_case is None:
            result.route_case = f"L({self.n},{self.k},{self.j},{self.s})"
        return result

    def __getattr__(self, name: str):
        return getattr(self._solver, name)


__all__ = [
    "CoveringDesignSolver",
    "SolverProgress",
    "SolverResult",
    "_add_windows_cuda_dll_dirs",
    "cp",
    "cp_model",
    "elements_to_mask",
    "mask_to_elements",
    "popcount_uint32",
    "solver_module_name",
]
