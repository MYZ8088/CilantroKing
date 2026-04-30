from __future__ import annotations

import time

import numpy as np

from n_algorithms.n19.adaptive_strategy import build_n19_features
from n_algorithms.n19.adaptive_strategy import classify_n19_cluster
from n_algorithms.n19.adaptive_strategy import select_n19_strategy_steps
from n_algorithms.n19.containment_specialized_module import refine_n19_containment_solution
from n_algorithms.n19.general_specialized_module import refine_n19_general_solution
from n_algorithms.n19.jk_specialized_module import is_n19_jk_target_case
from n_algorithms.n19.jk_specialized_module import is_n19_jk_small_s_case
from n_algorithms.n19.jk_specialized_module import ensure_n19_jk_kminus1_sparse_tables
from n_algorithms.n19.jk_specialized_module import refine_n19_jk_solution
from n_algorithms.n19.jk_specialized_module import refine_n19_jk_small_s_solution
from n_algorithms.n19.jk_specialized_module import should_use_n19_jk_direct_lane
from n_algorithms.n19.jk_specialized_module import should_use_n19_jk_kminus1_sparse_tables
from n_algorithms.n19.jk_specialized_module import should_use_n19_jk_small_s_direct_lane
from n_algorithms.n19.jk_specialized_module import solve_n19_jk_direct_lane
from n_algorithms.n19.jk_specialized_module import solve_n19_jk_small_s_direct_lane
from n_algorithms.shared.solver_core import elements_to_mask
from n_algorithms.shared.solver_core import CoveringDesignSolver as BaseCoveringDesignSolver
from n_algorithms.shared.solver_core import SolverResult


class CoveringDesignSolver(BaseCoveringDesignSolver):
    """n=19 专属独立模块入口，不接收其他 n 的输入。"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.n != 19:
            raise ValueError(
                "solver_n19_isolated 仅服务 n=19；"
                f"当前输入为 L({self.n},{self.k},{self.j},{self.s})"
            )

    def solve(self) -> SolverResult:
        cluster = classify_n19_cluster(k=self.k, j=self.j, s=self.s)
        self._report(
            "optimize",
            (
                "n19 isolated dispatch: "
                f"use dedicated n=19 lane for L({self.n},{self.k},{self.j},{self.s}); "
                f"cluster={cluster}"
            ),
        )
        started_at = time.time()
        solved = None
        direct_masks: list[int] | None = None
        if should_use_n19_jk_kminus1_sparse_tables(self):
            ensure_n19_jk_kminus1_sparse_tables(self)
        if should_use_n19_jk_direct_lane(self):
            direct_masks = solve_n19_jk_direct_lane(self)
        elif should_use_n19_jk_small_s_direct_lane(self):
            direct_masks = solve_n19_jk_small_s_direct_lane(self)
        if direct_masks is not None:
            solved = SolverResult(
                groups=[],
                    num_groups=len(direct_masks),
                    elapsed=time.time() - started_at,
                    verified=bool(self._verify(direct_masks)),
                    first_legal_elapsed=self._first_legal_elapsed,
                    groups_complete=False,
                    group_masks=np.array(direct_masks, dtype=np.uint32),
                )
        if solved is None:
            solved = super().solve()
        masks = self._result_masks(solved)
        features = build_n19_features(
            n=self.n,
            k=self.k,
            j=self.j,
            s=self.s,
            num_targets=self.num_targets,
            num_cands=self.num_cands,
            interaction_scale=self._interaction_scale,
            solution_len=len(masks),
        )
        steps = select_n19_strategy_steps(features)
        self._report(
            "optimize",
            (
                "n19 adaptive plan: "
                f"family={features.family}, cluster={features.cluster}, "
                f"targets={features.num_targets}, cands={features.num_cands}, "
                f"plan={steps}"
            ),
        )
        refined_masks = list(masks)
        for step in steps:
            before = len(refined_masks)
            if step == "jk_bundle" and is_n19_jk_target_case(
                n=self.n, k=self.k, j=self.j, s=self.s
            ):
                refined_masks = refine_n19_jk_solution(self, refined_masks)
            elif step == "jk_bundle" and is_n19_jk_small_s_case(
                n=self.n, k=self.k, j=self.j, s=self.s
            ):
                refined_masks = refine_n19_jk_small_s_solution(self, refined_masks)
            elif step.startswith("containment"):
                refined_masks = refine_n19_containment_solution(
                    self,
                    refined_masks,
                    cluster=features.cluster,
                )
            elif step.startswith("general"):
                refined_masks = refine_n19_general_solution(
                    self,
                    refined_masks,
                    cluster=features.cluster,
                )
            if len(refined_masks) < before:
                self._report(
                    "optimize",
                    f"n19 adaptive step {step} improved to {len(refined_masks)} groups",
                )

        if len(refined_masks) < len(masks):
            solved = SolverResult(
                groups=[],
                num_groups=len(refined_masks),
                elapsed=max(float(solved.elapsed), time.time() - started_at),
                verified=bool(self._verify(refined_masks)),
                first_legal_elapsed=solved.first_legal_elapsed,
                groups_complete=False,
                group_masks=np.array(refined_masks, dtype=np.uint32),
            )
        elapsed = max(float(solved.elapsed), time.time() - started_at)
        return SolverResult(
            groups=[list(g) for g in solved.groups],
            num_groups=int(solved.num_groups),
            elapsed=elapsed,
            verified=bool(solved.verified),
            first_legal_elapsed=solved.first_legal_elapsed,
            groups_complete=solved.groups_complete,
            group_masks=solved.group_masks,
        )

    def _result_masks(self, solved: SolverResult) -> list[int]:
        if solved.group_masks is not None:
            return [int(m) for m in solved.group_masks]
        return [elements_to_mask(group) for group in solved.groups]
