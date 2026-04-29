from __future__ import annotations

import os

from solver import CoveringDesignSolver as BaseCoveringDesignSolver
from solver import SolverResult


class CoveringDesignSolver:
    """Isolated routing wrapper for n=13 cases."""

    def __init__(
        self,
        n: int,
        k: int,
        j: int,
        s: int,
        t: int = 1,
        *,
        progress_cb: callable | None = None,
        cancel_fn: callable | None = None,
        num_attempts: int = 3,
        time_budget_sec: float | None = None,
        skip_final_verify: bool = False,
    ) -> None:
        if int(n) != 13:
            raise ValueError(f"solver_n13_isolated only handles n=13, got n={n}")
        self.n = int(n)
        self.k = int(k)
        self.j = int(j)
        self.s = int(s)
        self.t = int(t)
        self._base = self._build_base_solver(
            n=n,
            k=k,
            j=j,
            s=s,
            t=t,
            progress_cb=progress_cb,
            cancel_fn=cancel_fn,
            num_attempts=num_attempts,
            time_budget_sec=time_budget_sec,
            skip_final_verify=skip_final_verify,
        )

    def _build_base_solver(self, **kwargs) -> BaseCoveringDesignSolver:
        prev = os.environ.get("CK_DISABLE_N_ROUTING")
        os.environ["CK_DISABLE_N_ROUTING"] = "1"
        try:
            return BaseCoveringDesignSolver(**kwargs)
        finally:
            if prev is None:
                os.environ.pop("CK_DISABLE_N_ROUTING", None)
            else:
                os.environ["CK_DISABLE_N_ROUTING"] = prev

    def solve(self) -> SolverResult:
        solved = self._base.solve()
        solved.route_module = __name__
        solved.route_case = f"L({self.n},{self.k},{self.j},{self.s})"
        return solved
