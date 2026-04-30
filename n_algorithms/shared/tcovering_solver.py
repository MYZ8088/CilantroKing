"""T-Covering solver for t > 1 cases.

This module implements t-covering design where for each j-subset,
at least t different s-subsets must be covered by at least one group.

Definition: A s-subset is "covered" if at least one group contains it completely.
We count how many different s-subsets are covered (not total coverage count).

Optimizations:
- Precomputed s-subset coverage tables
- Incremental scoring updates
- Adaptive strategy selection
- Fast local search with early termination
"""

from __future__ import annotations

import math
import random
import time
from itertools import combinations
from math import comb
from typing import Callable

import numpy as np

from n_algorithms.shared.solver_core import (
    SolverProgress,
    SolverResult,
    elements_to_mask,
    mask_to_elements,
)


class TCoveringSolver:
    """Optimized solver for t-covering designs where t > 1."""

    def __init__(
        self,
        n: int,
        k: int,
        j: int,
        s: int,
        t: int,
        *,
        progress_cb: Callable[[SolverProgress], None] | None = None,
        cancel_fn: Callable[[], bool] | None = None,
        num_attempts: int = 3,
        time_budget_sec: float | None = None,
    ) -> None:
        self._t0 = time.time()
        
        self.n = n
        self.k = k
        self.j = j
        self.s = s
        self.t = t
        
        self._cb = progress_cb
        self._cancel = cancel_fn or (lambda: False)
        self._num_attempts = max(1, num_attempts)
        self._time_budget_sec = (
            float(time_budget_sec) if time_budget_sec is not None and time_budget_sec > 0 else None
        )
        # Add safety margin for t-covering
        self._time_budget_margin_sec = 0.0
        if self._time_budget_sec is not None:
            self._time_budget_margin_sec = 3.0 if n >= 16 else 1.5
        self._deadline_at = (
            self._t0 + max(0.0, self._time_budget_sec - self._time_budget_margin_sec)
            if self._time_budget_sec is not None
            else None
        )
        self._first_legal_elapsed: float | None = None

        # Validation
        if not 7 <= n <= 25:
            raise ValueError(f"n must be 7-25, got {n}")
        if not 4 <= k <= 7:
            raise ValueError(f"k must be 4-7, got {k}")
        if not 3 <= s <= 7:
            raise ValueError(f"s must be 3-7, got {s}")
        if not s <= j <= k:
            raise ValueError(f"Need s<=j<=k, got s={s} j={j} k={k}")
        if n < k:
            raise ValueError(f"Need n>=k, got n={n} k={k}")
        
        max_t = comb(j, s)
        if not 2 <= t <= max_t:
            raise ValueError(f"t must be between 2 and C({j},{s})={max_t}, got {t}")

        # Precompute all j-subsets (targets)
        elems = list(range(n))
        self.target_masks = np.array(
            [elements_to_mask(c) for c in combinations(elems, j)],
            dtype=np.uint32,
        )
        
        # Precompute all k-subsets (candidates)
        if j == k:
            self.cand_masks = self.target_masks.copy()
        else:
            self.cand_masks = np.array(
                [elements_to_mask(c) for c in combinations(elems, k)],
                dtype=np.uint32,
            )
        
        self.num_targets = len(self.target_masks)
        self.num_cands = len(self.cand_masks)
        
        # Adaptive strategy based on instance size
        self._is_large = self.num_cands > 10000 or self.num_targets > 5000
        self._is_huge = self.num_cands > 50000 or self.num_targets > 20000
        
        # Precompute s-subsets for each j-subset
        self._report("init", f"Precomputing s-subset coverage tables ({self.num_targets} targets, {self.num_cands} candidates)...")
        self._build_coverage_tables()
        
        self._report("init", f"Ready: {self.num_targets} targets, {self.num_cands} candidates")
        if self._is_huge:
            self._report("init", "Using huge instance optimizations")

    def _build_coverage_tables(self) -> None:
        """Build optimized coverage tables for fast scoring."""
        # For each j-subset, store its s-subsets
        self._s_subsets_per_j = {}
        self._j_to_s_indices = {}  # j_idx -> list of (s_idx, s_mask)
        
        all_s_masks = set()
        for j_idx in range(self.num_targets):
            j_mask = int(self.target_masks[j_idx])
            j_elems = mask_to_elements(j_mask)
            s_masks = [elements_to_mask(c) for c in combinations(j_elems, self.s)]
            self._s_subsets_per_j[j_mask] = s_masks
            self._j_to_s_indices[j_idx] = list(enumerate(s_masks))
            all_s_masks.update(s_masks)
        
        # Build candidate -> s-subsets coverage table
        # cand_covers_s[cand_idx] = set of s_masks that this candidate covers
        self._cand_covers_s = []
        for cand_idx in range(self.num_cands):
            cand_mask = int(self.cand_masks[cand_idx])
            covered_s = set()
            for s_mask in all_s_masks:
                if (s_mask & cand_mask) == s_mask:
                    covered_s.add(s_mask)
            self._cand_covers_s.append(covered_s)
        
        # Build s-subset -> j-subsets inverse index
        # s_to_j[s_mask] = list of (j_idx, s_idx_in_j)
        self._s_to_j = {}
        for j_idx in range(self.num_targets):
            j_mask = int(self.target_masks[j_idx])
            s_masks = self._s_subsets_per_j[j_mask]
            for s_idx, s_mask in enumerate(s_masks):
                if s_mask not in self._s_to_j:
                    self._s_to_j[s_mask] = []
                self._s_to_j[s_mask].append((j_idx, s_idx))

    def _report(
        self,
        phase: str,
        message: str,
        *,
        iteration: int = 0,
        sol_size: int = 0,
        remaining: int = 0,
    ) -> None:
        if self._cb is None:
            return
        elapsed = time.time() - self._t0
        prog = SolverProgress(
            phase=phase,
            message=message,
            iteration=iteration,
            solution_size=sol_size,
            remaining=remaining,
            total=self.num_targets,
            elapsed=elapsed,
        )
        self._cb(prog)

    def solve(self) -> SolverResult:
        """Solve the t-covering problem using greedy + fast local search."""
        self._report("start", f"Starting t-covering solver (t={self.t})...")
        
        best_solution = None
        best_size = float('inf')
        
        # Adaptive attempts based on instance size and time budget
        effective_attempts = self._num_attempts
        if self._is_huge:
            effective_attempts = max(1, self._num_attempts // 2)  # Reduce for huge instances
        elif self._deadline_at:
            # For time-constrained problems, reduce attempts
            effective_attempts = max(2, self._num_attempts // 2)
        
        for attempt in range(effective_attempts):
            if self._cancel():
                break
            
            # Check time budget
            if self._deadline_at and time.time() >= self._deadline_at:
                self._report("timeout", "Time budget exhausted")
                break
            
            self._report("attempt", f"Attempt {attempt + 1}/{effective_attempts}")
            
            # Greedy construction with randomization
            use_randomization = attempt > 0
            solution = self._greedy_solve(randomize=use_randomization)
            
            if solution:
                # Apply fast local search to improve
                solution = self._local_search(solution)
                
                if len(solution) < best_size:
                    best_solution = solution
                    best_size = len(solution)
                    
                    if self._first_legal_elapsed is None:
                        self._first_legal_elapsed = time.time() - self._t0
                    
                    self._report(
                        "improve",
                        f"Found solution with {best_size} groups",
                        sol_size=best_size,
                    )
        
        if best_solution is None:
            # Return empty solution if no solution found
            elapsed = time.time() - self._t0
            return SolverResult(
                groups=[],
                num_groups=0,
                elapsed=elapsed,
                verified=False,
                first_legal_elapsed=None,
            )
        
        # Convert masks to element lists
        groups = [sorted(mask_to_elements(m)) for m in best_solution]
        elapsed = time.time() - self._t0
        
        # Skip verification by default
        
        return SolverResult(
            groups=groups,
            num_groups=len(groups),
            elapsed=elapsed,
            verified=False,  # Skip verification by default
            first_legal_elapsed=self._first_legal_elapsed,
        )

    def _greedy_solve(self, randomize: bool = False) -> list[int] | None:
        """Optimized greedy algorithm with adaptive top-K for large instances."""
        selected = []
        selected_set = set()
        
        # Track which s-subsets are covered
        covered_s_masks = set()
        
        # Track coverage count for each j-subset
        j_covered_count = np.zeros(self.num_targets, dtype=np.int32)
        
        iteration = 0
        log_interval = max(1, self.num_targets // 100)
        
        # Adaptive top-K for huge instances
        use_top_k = self._is_huge
        top_k_size = min(5000, self.num_cands // 10) if use_top_k else self.num_cands
        
        while True:
            if self._cancel():
                return None
            
            # Check deadline
            if self._deadline_at and time.time() >= self._deadline_at:
                return selected if selected else None
            
            # Find unsatisfied j-subsets
            unsatisfied_j = np.where(j_covered_count < self.t)[0]
            
            if len(unsatisfied_j) == 0:
                self._report(
                    "complete",
                    f"Solution found with {len(selected)} groups",
                    sol_size=len(selected),
                )
                return selected
            
            # Fast scoring with top-K heuristic for large instances
            best_cand_idx = None
            best_score = -1
            candidate_scores = []
            
            # Sample candidates for huge instances
            if use_top_k and iteration > 0:
                # Focus on high-potential candidates
                cand_indices = self._sample_candidates(selected_set, unsatisfied_j, top_k_size)
            else:
                cand_indices = range(self.num_cands)
            
            for cand_idx in cand_indices:
                cand_mask = int(self.cand_masks[cand_idx])
                
                if cand_mask in selected_set:
                    continue
                
                # Fast score calculation
                score = self._score_candidate(cand_idx, covered_s_masks, j_covered_count)
                
                if score > 0:
                    candidate_scores.append((cand_idx, score))
                    if score > best_score:
                        best_score = score
                        best_cand_idx = cand_idx
            
            if not candidate_scores:
                return None
            
            # Select candidate with adaptive strategy
            if randomize and len(candidate_scores) > 3:
                # RCL strategy
                candidate_scores.sort(key=lambda x: x[1], reverse=True)
                threshold = max(3, len(candidate_scores) // 5)
                min_score = max(1, int(best_score * 0.8))
                rcl = [c for c in candidate_scores[:threshold] if c[1] >= min_score]
                best_cand_idx = random.choice(rcl)[0]
            
            # Add selected candidate
            best_mask = int(self.cand_masks[best_cand_idx])
            selected.append(best_mask)
            selected_set.add(best_mask)
            
            # Incremental update
            newly_covered = self._cand_covers_s[best_cand_idx] - covered_s_masks
            covered_s_masks.update(newly_covered)
            
            # Update j-subset coverage counts
            for s_mask in newly_covered:
                if s_mask in self._s_to_j:
                    for j_idx, _ in self._s_to_j[s_mask]:
                        j_covered_count[j_idx] += 1
            
            iteration += 1
            
            if iteration % log_interval == 0:
                self._report(
                    "greedy",
                    f"Iter {iteration}: {len(selected)} groups, {len(unsatisfied_j)} unsatisfied",
                    iteration=iteration,
                    sol_size=len(selected),
                    remaining=len(unsatisfied_j),
                )
        
        return None
    
    def _score_candidate(self, cand_idx: int, covered_s: set, j_covered_count: np.ndarray) -> int:
        """Fast candidate scoring."""
        score = 0
        cand_s_covers = self._cand_covers_s[cand_idx]
        
        for s_mask in cand_s_covers:
            if s_mask in covered_s:
                continue
            
            if s_mask in self._s_to_j:
                for j_idx, _ in self._s_to_j[s_mask]:
                    if j_covered_count[j_idx] < self.t:
                        score += 1
                        break
        
        return score
    
    def _sample_candidates(self, selected_set: set, unsatisfied_j: np.ndarray, k: int) -> list[int]:
        """Sample high-potential candidates for large instances."""
        # Heuristic: prefer candidates that cover elements in unsatisfied j-subsets
        candidates = []
        
        # Get elements that appear in unsatisfied j-subsets
        hot_elements = set()
        for j_idx in unsatisfied_j[:min(100, len(unsatisfied_j))]:
            j_mask = int(self.target_masks[j_idx])
            hot_elements.update(mask_to_elements(j_mask))
        
        # Score candidates by how many hot elements they contain
        for cand_idx in range(self.num_cands):
            cand_mask = int(self.cand_masks[cand_idx])
            if cand_mask in selected_set:
                continue
            
            cand_elems = mask_to_elements(cand_mask)
            overlap = len(set(cand_elems) & hot_elements)
            
            if overlap > 0:
                candidates.append((cand_idx, overlap))
        
        # Return top-K by overlap
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in candidates[:k]]

    def _local_search(self, solution: list[int]) -> list[int]:
        """Fast local search with early termination."""
        if len(solution) <= 3:
            return solution
        
        self._report("local_search", f"Optimizing {len(solution)} groups...")
        
        improved = True
        passes = 0
        max_passes = 3
        
        while improved and passes < max_passes and not self._cancel():
            improved = False
            passes += 1
            
            indices = list(range(len(solution)))
            if passes > 1:
                random.shuffle(indices)
            
            for i in indices:
                candidate = solution[:i] + solution[i+1:]
                
                if self._fast_verify(candidate):
                    solution = candidate
                    improved = True
                    self._report(
                        "local_search",
                        f"Removed redundant group -> {len(solution)} groups",
                        sol_size=len(solution),
                    )
                    break
        
        return solution
    
    def _simulated_annealing(self, solution: list[int]) -> list[int]:
        """Simulated annealing for solution improvement."""
        if len(solution) <= 5:
            return solution
        
        self._report("SA", f"Simulated annealing on {len(solution)} groups...")
        
        current = solution[:]
        best = solution[:]
        best_size = len(best)
        
        # SA parameters
        initial_temp = 10.0
        final_temp = 0.1
        cooling_rate = 0.95
        iterations_per_temp = min(20, len(solution) * 2)
        
        temp = initial_temp
        
        while temp > final_temp and not self._cancel():
            for _ in range(iterations_per_temp):
                # Try to remove a random group
                if len(current) <= 3:
                    break
                
                remove_idx = random.randint(0, len(current) - 1)
                neighbor = current[:remove_idx] + current[remove_idx+1:]
                
                # Check if neighbor is valid
                if self._fast_verify(neighbor):
                    # Accept improvement
                    current = neighbor
                    if len(current) < best_size:
                        best = current[:]
                        best_size = len(best)
                        self._report(
                            "SA",
                            f"SA improved -> {best_size} groups",
                            sol_size=best_size,
                        )
                else:
                    # Accept with probability based on temperature
                    delta = 1  # Penalty for invalid solution
                    if random.random() < math.exp(-delta / temp):
                        # Try swap instead of remove
                        neighbor = self._try_swap(current)
                        if neighbor and self._fast_verify(neighbor):
                            current = neighbor
                            if len(current) < best_size:
                                best = current[:]
                                best_size = len(best)
            
            temp *= cooling_rate
        
        return best
    
    def _try_swap(self, solution: list[int]) -> list[int] | None:
        """Try to swap one group with an unused candidate."""
        if len(solution) == 0:
            return None
        
        # Remove a random group
        remove_idx = random.randint(0, len(solution) - 1)
        removed = solution[remove_idx]
        candidate = solution[:remove_idx] + solution[remove_idx+1:]
        
        # Try to add a random unused candidate
        selected_set = set(solution)
        unused = [int(self.cand_masks[i]) for i in range(min(100, self.num_cands)) 
                  if int(self.cand_masks[i]) not in selected_set]
        
        if unused:
            new_group = random.choice(unused)
            return candidate + [new_group]
        
        return None
    
    def _fast_verify(self, masks: list[int]) -> bool:
        """Fast verification with early termination."""
        if not masks:
            return self.num_targets == 0
        
        # Build covered s-masks set
        covered_s = set()
        for mask in masks:
            # Use precomputed coverage
            mask_int = int(mask)
            for cand_idx in range(self.num_cands):
                if int(self.cand_masks[cand_idx]) == mask_int:
                    covered_s.update(self._cand_covers_s[cand_idx])
                    break
        
        # Check each j-subset
        for j_idx in range(self.num_targets):
            j_mask = int(self.target_masks[j_idx])
            s_masks = self._s_subsets_per_j[j_mask]
            
            covered_count = sum(1 for s_mask in s_masks if s_mask in covered_s)
            
            if covered_count < self.t:
                return False  # Early termination
        
        return True

    def _verify(self, masks: list[int]) -> bool:
        """
        Verify t-covering: for each j-subset, at least t different s-subsets
        must be covered by at least one group.
        """
        for j_idx in range(self.num_targets):
            j_mask = int(self.target_masks[j_idx])
            s_masks = self._s_subsets_per_j[j_mask]
            
            covered_s_count = 0
            for s_mask in s_masks:
                # Check if any group covers this s-subset
                is_covered = False
                for group_mask in masks:
                    if (s_mask & group_mask) == s_mask:
                        is_covered = True
                        break
                if is_covered:
                    covered_s_count += 1
            
            if covered_s_count < self.t:
                return False
        
        return True
