"""N19 specialized optimization module.

This module provides specialized algorithms for n=19 cases without inheriting from solver.
It follows the same pattern as n18_specialized_module.py to avoid circular imports.

This module includes:
1. Direct solve attempts (before main greedy loop)
2. Refinement steps (after main solve)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from n19_adaptive_strategy import build_n19_features
from n19_adaptive_strategy import classify_n19_cluster
from n19_adaptive_strategy import select_n19_strategy_steps
from n19_containment_specialized_module import refine_n19_containment_solution
from n19_general_specialized_module import refine_n19_general_solution
from n19_jk_specialized_module import is_n19_jk_target_case
from n19_jk_specialized_module import is_n19_jk_small_s_case
from n19_jk_specialized_module import ensure_n19_jk_kminus1_sparse_tables
from n19_jk_specialized_module import refine_n19_jk_solution
from n19_jk_specialized_module import refine_n19_jk_small_s_solution
from n19_jk_specialized_module import should_use_n19_jk_direct_lane
from n19_jk_specialized_module import should_use_n19_jk_kminus1_sparse_tables
from n19_jk_specialized_module import should_use_n19_jk_small_s_direct_lane
from n19_jk_specialized_module import solve_n19_jk_direct_lane
from n19_jk_specialized_module import solve_n19_jk_small_s_direct_lane

if TYPE_CHECKING:
    from solver import CoveringDesignSolver


def is_n19_special_case(n: int, k: int, j: int, s: int) -> bool:
    """Check if this is an n=19 case that can benefit from specialized optimization."""
    return int(n) == 19 and 4 <= int(k) <= 7 and 3 <= int(s) <= int(j) <= int(k)


def try_n19_direct_solve(solver: "CoveringDesignSolver") -> list[int] | None:
    """Try direct solve for n=19 cases before main greedy loop.
    
    This replicates the logic from solver_n19_isolated.py's solve() method.
    
    Returns:
        List of masks if direct solve succeeds, None otherwise
    """
    if not is_n19_special_case(solver.n, solver.k, solver.j, solver.s):
        return None
    
    cluster = classify_n19_cluster(k=solver.k, j=solver.j, s=solver.s)
    solver._report(
        "optimize",
        (
            f"N19 direct solve attempt: "
            f"L({solver.n},{solver.k},{solver.j},{solver.s}) -> cluster={cluster}"
        ),
    )
    
    # Ensure sparse tables if needed
    if should_use_n19_jk_kminus1_sparse_tables(solver):
        ensure_n19_jk_kminus1_sparse_tables(solver)
    
    # Try direct solve
    direct_masks: list[int] | None = None
    if should_use_n19_jk_direct_lane(solver):
        direct_masks = solve_n19_jk_direct_lane(solver)
    elif should_use_n19_jk_small_s_direct_lane(solver):
        direct_masks = solve_n19_jk_small_s_direct_lane(solver)
    
    if direct_masks is not None:
        if solver._verify(direct_masks):
            solver._report(
                "optimize",
                f"N19 direct solve succeeded: {len(direct_masks)} groups",
            )
            return direct_masks
        else:
            solver._report(
                "optimize",
                "N19 direct solve produced invalid solution, falling back to main solver",
            )
    
    return None


def run_n19_specialized_module(solver: "CoveringDesignSolver", sol: list[int]) -> list[int]:
    """Main entry point for n=19 specialized refinement.
    
    This function:
    1. Classifies the n=19 case by cluster
    2. Builds feature profile
    3. Selects adaptive strategy steps
    4. Applies specialized refinement algorithms
    
    Args:
        solver: The main solver instance (not inherited, just used for access to data)
        sol: Current solution as list of masks
        
    Returns:
        Refined solution (may be same as input if no improvement found)
    """
    if not is_n19_special_case(solver.n, solver.k, solver.j, solver.s):
        return sol
    
    remaining = solver._time_remaining_sec()
    if remaining is None or remaining < 2.0:
        return sol
    
    cluster = classify_n19_cluster(k=solver.k, j=solver.j, s=solver.s)
    solver._report(
        "optimize",
        (
            f"Phase-N19 specialized dispatch: "
            f"L({solver.n},{solver.k},{solver.j},{solver.s}) -> cluster={cluster}, "
            f"remaining={None if remaining is None else round(remaining, 3)}"
        ),
    )
    
    # Build feature profile for adaptive strategy selection
    features = build_n19_features(
        n=solver.n,
        k=solver.k,
        j=solver.j,
        s=solver.s,
        num_targets=solver.num_targets,
        num_cands=solver.num_cands,
        interaction_scale=solver._interaction_scale,
        solution_len=len(sol),
    )
    
    # Select strategy steps based on features
    steps = select_n19_strategy_steps(features)
    solver._report(
        "optimize",
        (
            f"Phase-N19 adaptive plan: "
            f"family={features.family}, cluster={features.cluster}, "
            f"targets={features.num_targets}, cands={features.num_cands}, "
            f"plan={steps}"
        ),
    )
    
    # Apply refinement steps
    refined_masks = list(sol)
    for step in steps:
        remaining = solver._time_remaining_sec()
        if remaining is None or remaining < 1.5:
            break
            
        before = len(refined_masks)
        
        if step == "jk_bundle" and is_n19_jk_target_case(
            n=solver.n, k=solver.k, j=solver.j, s=solver.s
        ):
            refined_masks = refine_n19_jk_solution(solver, refined_masks)
        elif step == "jk_bundle" and is_n19_jk_small_s_case(
            n=solver.n, k=solver.k, j=solver.j, s=solver.s
        ):
            refined_masks = refine_n19_jk_small_s_solution(solver, refined_masks)
        elif step.startswith("containment"):
            refined_masks = refine_n19_containment_solution(
                solver,
                refined_masks,
                cluster=features.cluster,
            )
        elif step.startswith("general"):
            refined_masks = refine_n19_general_solution(
                solver,
                refined_masks,
                cluster=features.cluster,
            )
        
        if len(refined_masks) < before:
            solver._report(
                "optimize",
                f"Phase-N19 adaptive step {step} improved to {len(refined_masks)} groups",
            )
    
    # Verify and return
    if len(refined_masks) < len(sol) and solver._verify(refined_masks):
        return refined_masks
    return sol
