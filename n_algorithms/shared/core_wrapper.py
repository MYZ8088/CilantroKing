from __future__ import annotations

from n_algorithms.shared.solver_core import CoveringDesignSolver as CoreCoveringDesignSolver
from n_algorithms.shared.solver_core import SolverResult


class RoutedCoreSolver:
    """Base wrapper for n-specific folders that use the shared core algorithm."""

    expected_n: int

    def __init__(self, *args, **kwargs) -> None:
        self._base = CoreCoveringDesignSolver(*args, **kwargs)
        if int(self._base.n) != int(self.expected_n):
            raise ValueError(
                f"n{self.expected_n:02d} solver only handles n={self.expected_n}, "
                f"got n={self._base.n}"
            )
        self.n = int(self._base.n)
        self.k = int(self._base.k)
        self.j = int(self._base.j)
        self.s = int(self._base.s)
        self.t = int(self._base.t)

    def solve(self) -> SolverResult:
        solved = self._base.solve()
        solved.route_module = self.__module__
        solved.route_case = f"L({self.n},{self.k},{self.j},{self.s})"
        return solved

    def __getattr__(self, name: str):
        return getattr(self._base, name)
