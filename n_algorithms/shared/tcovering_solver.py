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
            float(time_budget_sec)
            if time_budget_sec is not None and time_budget_sec > 0
            else None
        )
        self._time_budget_margin_sec = 0.0
        if self._time_budget_sec is not None:
            self._time_budget_margin_sec = 3.0 if n >= 16 else 1.5
        self._deadline_at = (
            self._t0 + max(0.0, self._time_budget_sec - self._time_budget_margin_sec)
            if self._time_budget_sec is not None
            else None
        )
        self._first_legal_elapsed: float | None = None

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

        elems = list(range(n))
        self.target_masks = np.array(
            [elements_to_mask(c) for c in combinations(elems, j)],
            dtype=np.uint32,
        )

        if j == k:
            self.cand_masks = self.target_masks.copy()
        else:
            self.cand_masks = np.array(
                [elements_to_mask(c) for c in combinations(elems, k)],
                dtype=np.uint32,
            )

        self.num_targets = len(self.target_masks)
        self.num_cands = len(self.cand_masks)

        self._is_large = self.num_cands > 10000 or self.num_targets > 5000
        self._is_huge = self.num_cands > 50000 or self.num_targets > 20000

        self._cand_index_map = {
            int(mask): idx for idx, mask in enumerate(self.cand_masks)
        }

        self._report(
            "init",
            f"Precomputing s-subset coverage tables ({self.num_targets} targets, {self.num_cands} candidates)...",
        )
        self._build_coverage_tables()

        self._report(
            "init", f"Ready: {self.num_targets} targets, {self.num_cands} candidates"
        )
        if self._is_huge:
            self._report("init", "Using huge instance optimizations")

    def _build_coverage_tables(self) -> None:
        """Build optimized coverage tables for fast scoring."""
        self._s_subsets_per_j = {}
        self._j_to_s_indices = {}

        all_s_masks = set()
        for j_idx in range(self.num_targets):
            j_mask = int(self.target_masks[j_idx])
            j_elems = mask_to_elements(j_mask)
            s_masks = [elements_to_mask(c) for c in combinations(j_elems, self.s)]
            self._s_subsets_per_j[j_mask] = s_masks
            self._j_to_s_indices[j_idx] = list(enumerate(s_masks))
            all_s_masks.update(s_masks)

        self._cand_covers_s = []
        for cand_idx in range(self.num_cands):
            cand_mask = int(self.cand_masks[cand_idx])
            covered_s = set()
            for s_mask in all_s_masks:
                if (s_mask & cand_mask) == s_mask:
                    covered_s.add(s_mask)
            self._cand_covers_s.append(covered_s)

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
        """Solve the t-covering problem using multiple strategies."""
        self._report("start", f"Starting t-covering solver (t={self.t})...")

        best_solution = None
        best_size = float("inf")

        # Strategy 1: Iterative shrinking (try to reduce from a larger solution)
        if not self._is_huge:
            self._report("shrink", "Trying iterative shrinking strategy...")
            shrink_solution = self._iterative_shrink()
            if shrink_solution and len(shrink_solution) < best_size:
                best_solution = shrink_solution
                best_size = len(shrink_solution)
                if self._first_legal_elapsed is None:
                    self._first_legal_elapsed = time.time() - self._t0
                self._report("improve", f"Shrink strategy: {best_size} groups", sol_size=best_size)

        # Strategy 2: Multiple greedy attempts with different strategies
        effective_attempts = self._num_attempts * 3
        if self._is_huge:
            effective_attempts = max(5, self._num_attempts * 2)
        elif self._deadline_at:
            effective_attempts = max(10, self._num_attempts * 2)

        for attempt in range(effective_attempts):
            if self._cancel():
                break

            if self._deadline_at and time.time() >= self._deadline_at:
                self._report("timeout", "Time budget exhausted")
                break

            self._report("attempt", f"Attempt {attempt + 1}/{effective_attempts}")

            # Vary strategies
            use_randomization = attempt > 0
            use_weighted_scoring = attempt % 3 == 1
            
            solution = self._greedy_solve(
                randomize=use_randomization,
                use_weighted=use_weighted_scoring
            )

            if solution:
                # Apply all local search methods
                solution = self._fast_local_search(solution)
                solution = self._swap_local_search(solution)
                solution = self._merge_local_search(solution)

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
            elapsed = time.time() - self._t0
            return SolverResult(
                groups=[],
                num_groups=0,
                elapsed=elapsed,
                verified=False,
                first_legal_elapsed=None,
            )

        groups = [sorted(mask_to_elements(m)) for m in best_solution]
        elapsed = time.time() - self._t0

        return SolverResult(
            groups=groups,
            num_groups=len(groups),
            elapsed=elapsed,
            verified=False,
            first_legal_elapsed=self._first_legal_elapsed,
        )

    def _greedy_solve(self, randomize: bool = False, use_weighted: bool = False) -> list[int] | None:
        """Optimized greedy algorithm with adaptive top-K for large instances."""
        selected = []
        selected_set = set()

        covered_s_masks = set()
        j_covered_count = np.zeros(self.num_targets, dtype=np.int32)

        iteration = 0
        log_interval = max(1, self.num_targets // 100)

        use_top_k = self._is_huge
        top_k_size = min(5000, self.num_cands // 10) if use_top_k else self.num_cands

        while True:
            if self._cancel():
                return None

            if self._deadline_at and time.time() >= self._deadline_at:
                return selected if selected else None

            unsatisfied_j = np.where(j_covered_count < self.t)[0]

            if len(unsatisfied_j) == 0:
                self._report(
                    "complete",
                    f"Solution found with {len(selected)} groups",
                    sol_size=len(selected),
                )
                return selected

            best_cand_idx = None
            best_score = -1
            candidate_scores = []

            if use_top_k and iteration > 0:
                cand_indices = self._sample_candidates(
                    selected_set, unsatisfied_j, top_k_size
                )
            else:
                cand_indices = range(self.num_cands)

            for cand_idx in cand_indices:
                cand_mask = int(self.cand_masks[cand_idx])

                if cand_mask in selected_set:
                    continue

                if use_weighted:
                    score = self._score_candidate_weighted(
                        cand_idx, covered_s_masks, j_covered_count
                    )
                else:
                    score = self._score_candidate(
                        cand_idx, covered_s_masks, j_covered_count
                    )

                if score > 0:
                    candidate_scores.append((cand_idx, score))
                    if score > best_score:
                        best_score = score
                        best_cand_idx = cand_idx

            if not candidate_scores:
                return None

            if randomize and len(candidate_scores) > 3:
                candidate_scores.sort(key=lambda x: x[1], reverse=True)
                threshold = max(3, len(candidate_scores) // 5)
                min_score = max(1, int(best_score * 0.8))
                rcl = [c for c in candidate_scores[:threshold] if c[1] >= min_score]
                best_cand_idx = random.choice(rcl)[0]

            best_mask = int(self.cand_masks[best_cand_idx])
            selected.append(best_mask)
            selected_set.add(best_mask)

            newly_covered = self._cand_covers_s[best_cand_idx] - covered_s_masks
            covered_s_masks.update(newly_covered)

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

    def _score_candidate(
        self, cand_idx: int, covered_s: set, j_covered_count: np.ndarray
    ) -> int:
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

    def _score_candidate_weighted(
        self, cand_idx: int, covered_s: set, j_covered_count: np.ndarray
    ) -> float:
        """Weighted scoring that prioritizes rare coverage."""
        cand_s_covers = self._cand_covers_s[cand_idx]
        
        score = 0.0
        
        for s_mask in cand_s_covers:
            if s_mask in covered_s:
                continue
            
            if s_mask in self._s_to_j:
                for j_idx, _ in self._s_to_j[s_mask]:
                    if j_covered_count[j_idx] < self.t:
                        # Weight by gap: prioritize j-subsets furthest from target
                        gap = self.t - j_covered_count[j_idx]
                        # Quadratic penalty for larger gaps
                        score += gap * gap
                        break
        
        return score

    def _sample_candidates(
        self, selected_set: set, unsatisfied_j: np.ndarray, k: int
    ) -> list[int]:
        """Sample high-potential candidates for large instances."""
        candidates = []

        hot_elements = set()
        for j_idx in unsatisfied_j[: min(100, len(unsatisfied_j))]:
            j_mask = int(self.target_masks[j_idx])
            hot_elements.update(mask_to_elements(j_mask))

        for cand_idx in range(self.num_cands):
            cand_mask = int(self.cand_masks[cand_idx])
            if cand_mask in selected_set:
                continue

            cand_elems = mask_to_elements(cand_mask)
            overlap = len(set(cand_elems) & hot_elements)

            if overlap > 0:
                candidates.append((cand_idx, overlap))

        candidates.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in candidates[:k]]

    def _fast_local_search(self, solution: list[int]) -> list[int]:
        """Optimized local search with incremental verification."""
        if len(solution) <= 3:
            return solution

        self._report("local_search", f"Optimizing {len(solution)} groups...")

        covered_s_masks = set()
        for mask in solution:
            mask_int = int(mask)
            cand_idx = self._cand_index_map.get(mask_int)
            if cand_idx is not None:
                covered_s_masks.update(self._cand_covers_s[cand_idx])

        j_covered_count = np.zeros(self.num_targets, dtype=np.int32)
        for s_mask in covered_s_masks:
            if s_mask in self._s_to_j:
                for j_idx, _ in self._s_to_j[s_mask]:
                    j_covered_count[j_idx] += 1

        improved = True
        passes = 0
        max_passes = 2

        while improved and passes < max_passes and not self._cancel():
            improved = False
            passes += 1

            if self._deadline_at and time.time() >= self._deadline_at:
                break

            indices = list(range(len(solution)))
            if passes > 1:
                random.shuffle(indices)

            for i in indices:
                removed_mask = solution[i]
                removed_idx = self._cand_index_map.get(int(removed_mask))

                if removed_idx is None:
                    continue

                removed_s = self._cand_covers_s[removed_idx]

                can_remove = True
                for s_mask in removed_s:
                    if s_mask not in covered_s_masks:
                        continue

                    if s_mask in self._s_to_j:
                        for j_idx, _ in self._s_to_j[s_mask]:
                            other_count = 0
                            for other_s in self._s_subsets_per_j[
                                int(self.target_masks[j_idx])
                            ]:
                                if other_s != s_mask and other_s in covered_s_masks:
                                    is_covered_by_others = False
                                    for j, other_mask in enumerate(solution):
                                        if j == i:
                                            continue
                                        other_idx = self._cand_index_map.get(
                                            int(other_mask)
                                        )
                                        if (
                                            other_idx is not None
                                            and other_s
                                            in self._cand_covers_s[other_idx]
                                        ):
                                            is_covered_by_others = True
                                            break
                                    if is_covered_by_others:
                                        other_count += 1

                            if (
                                j_covered_count[j_idx] - 1 < self.t
                                and other_count < self.t
                            ):
                                can_remove = False
                                break

                    if not can_remove:
                        break

                if can_remove:
                    candidate = solution[:i] + solution[i + 1 :]
                    if self._incremental_verify(candidate, covered_s_masks, removed_s):
                        solution = candidate
                        covered_s_masks -= removed_s
                        for s_mask in removed_s:
                            if s_mask in self._s_to_j:
                                for j_idx, _ in self._s_to_j[s_mask]:
                                    j_covered_count[j_idx] -= 1

                        improved = True
                        self._report(
                            "local_search",
                            f"Removed redundant group -> {len(solution)} groups",
                            sol_size=len(solution),
                        )
                        break

        return solution

    def _incremental_verify(
        self, masks: list[int], current_covered: set, removed_s: set
    ) -> bool:
        """Fast incremental verification."""
        if not masks:
            return self.num_targets == 0

        new_covered = current_covered - removed_s

        for j_idx in range(self.num_targets):
            j_mask = int(self.target_masks[j_idx])
            s_masks = self._s_subsets_per_j[j_mask]

            covered_count = sum(1 for s_mask in s_masks if s_mask in new_covered)

            if covered_count < self.t:
                return False

        return True

    def _fast_verify(self, masks: list[int]) -> bool:
        """Fast verification with early termination."""
        if not masks:
            return self.num_targets == 0

        covered_s = set()
        for mask in masks:
            mask_int = int(mask)
            cand_idx = self._cand_index_map.get(mask_int)
            if cand_idx is not None:
                covered_s.update(self._cand_covers_s[cand_idx])

        for j_idx in range(self.num_targets):
            j_mask = int(self.target_masks[j_idx])
            s_masks = self._s_subsets_per_j[j_mask]

            covered_count = sum(1 for s_mask in s_masks if s_mask in covered_s)

            if covered_count < self.t:
                return False

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

    def _swap_local_search(self, solution: list[int]) -> list[int]:
        """1-1 swap local search: try replacing each group with a better one."""
        if len(solution) <= 2:
            return solution
        
        if self._deadline_at and time.time() >= self._deadline_at:
            return solution
        
        self._report("swap_search", f"Trying 1-1 swaps on {len(solution)} groups...")
        
        improved = True
        passes = 0
        max_passes = 1  # One pass is usually enough
        
        while improved and passes < max_passes and not self._cancel():
            improved = False
            passes += 1
            
            if self._deadline_at and time.time() >= self._deadline_at:
                break
            
            # Try replacing each group
            for i in range(len(solution)):
                if self._cancel():
                    break
                
                # Remove group i temporarily
                removed_mask = solution[i]
                temp_solution = solution[:i] + solution[i+1:]
                
                # Find what coverage is lost
                removed_idx = self._cand_index_map.get(int(removed_mask))
                if removed_idx is None:
                    continue
                
                # Build coverage state without this group
                covered_s = set()
                for mask in temp_solution:
                    mask_int = int(mask)
                    cand_idx = self._cand_index_map.get(mask_int)
                    if cand_idx is not None:
                        covered_s.update(self._cand_covers_s[cand_idx])
                
                j_covered_count = np.zeros(self.num_targets, dtype=np.int32)
                for s_mask in covered_s:
                    if s_mask in self._s_to_j:
                        for j_idx, _ in self._s_to_j[s_mask]:
                            j_covered_count[j_idx] += 1
                
                # Find best replacement
                best_replacement_idx = None
                best_replacement_score = -1
                
                for cand_idx in range(self.num_cands):
                    cand_mask = int(self.cand_masks[cand_idx])
                    
                    # Skip if already in solution
                    if cand_mask in [int(m) for m in temp_solution]:
                        continue
                    
                    # Score this candidate
                    score = self._score_candidate_weighted(
                        cand_idx, covered_s, j_covered_count
                    )
                    
                    if score > best_replacement_score:
                        best_replacement_score = score
                        best_replacement_idx = cand_idx
                
                # Try the replacement
                if best_replacement_idx is not None:
                    new_mask = int(self.cand_masks[best_replacement_idx])
                    new_solution = temp_solution + [new_mask]
                    
                    # Verify it's still valid
                    if self._fast_verify(new_solution):
                        solution = new_solution
                        improved = True
                        self._report(
                            "swap_search",
                            f"Swapped group {i} -> better solution still {len(solution)} groups",
                            sol_size=len(solution),
                        )
                        break  # Start over after improvement
        
        return solution

    def _merge_local_search(self, solution: list[int]) -> list[int]:
        """2-1 merge local search: try replacing two groups with one better group."""
        if len(solution) <= 3:
            return solution
        
        if self._deadline_at and time.time() >= self._deadline_at:
            return solution
        
        self._report("merge_search", f"Trying 2-1 merges on {len(solution)} groups...")
        
        improved = True
        passes = 0
        max_passes = 1
        
        while improved and passes < max_passes and not self._cancel():
            improved = False
            passes += 1
            
            if self._deadline_at and time.time() >= self._deadline_at:
                break
            
            # Try removing pairs of groups
            for i in range(len(solution)):
                for j in range(i + 1, min(i + 10, len(solution))):  # Limit search
                    if self._cancel():
                        break
                    
                    # Remove groups i and j
                    temp_solution = [solution[k] for k in range(len(solution)) if k != i and k != j]
                    
                    # Build coverage state without these groups
                    covered_s = set()
                    for mask in temp_solution:
                        mask_int = int(mask)
                        cand_idx = self._cand_index_map.get(mask_int)
                        if cand_idx is not None:
                            covered_s.update(self._cand_covers_s[cand_idx])
                    
                    j_covered_count = np.zeros(self.num_targets, dtype=np.int32)
                    for s_mask in covered_s:
                        if s_mask in self._s_to_j:
                            for j_idx, _ in self._s_to_j[s_mask]:
                                j_covered_count[j_idx] += 1
                    
                    # Find best single replacement
                    best_replacement_idx = None
                    best_replacement_score = -1
                    
                    for cand_idx in range(self.num_cands):
                        cand_mask = int(self.cand_masks[cand_idx])
                        
                        # Skip if already in solution
                        if cand_mask in [int(m) for m in temp_solution]:
                            continue
                        
                        # Score this candidate
                        score = self._score_candidate_weighted(
                            cand_idx, covered_s, j_covered_count
                        )
                        
                        if score > best_replacement_score:
                            best_replacement_score = score
                            best_replacement_idx = cand_idx
                    
                    # Try the replacement
                    if best_replacement_idx is not None:
                        new_mask = int(self.cand_masks[best_replacement_idx])
                        new_solution = temp_solution + [new_mask]
                        
                        # Verify it's still valid
                        if self._fast_verify(new_solution):
                            solution = new_solution
                            improved = True
                            self._report(
                                "merge_search",
                                f"Merged 2 groups into 1 -> {len(solution)} groups",
                                sol_size=len(solution),
                            )
                            break  # Start over after improvement
                
                if improved:
                    break
        
        return solution

    def _iterative_shrink(self) -> list[int] | None:
        """
        Iterative shrinking: start with all candidates, then iteratively remove groups.
        This explores from a different direction than greedy construction.
        """
        if self._deadline_at and time.time() >= self._deadline_at:
            return None
        
        # Start with a large solution (all candidates or a subset)
        if self.num_cands > 50:
            # For larger problems, start with a random subset
            initial_size = min(self.num_cands, max(20, self.num_targets // 2))
            indices = random.sample(range(self.num_cands), initial_size)
            current_solution = [int(self.cand_masks[i]) for i in indices]
        else:
            # For small problems, start with all candidates
            current_solution = [int(m) for m in self.cand_masks]
        
        # Verify it's valid
        if not self._fast_verify(current_solution):
            # If not valid, add more groups greedily
            return None
        
        self._report("shrink", f"Starting with {len(current_solution)} groups, shrinking...")
        
        # Iteratively try to remove groups
        improved = True
        iterations = 0
        max_iterations = len(current_solution)
        
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            
            if self._cancel() or (self._deadline_at and time.time() >= self._deadline_at):
                break
            
            # Try to remove each group
            indices = list(range(len(current_solution)))
            random.shuffle(indices)  # Random order
            
            for i in indices:
                candidate = current_solution[:i] + current_solution[i+1:]
                
                if self._fast_verify(candidate):
                    current_solution = candidate
                    improved = True
                    self._report(
                        "shrink",
                        f"Removed group -> {len(current_solution)} groups",
                        sol_size=len(current_solution),
                    )
                    break  # Restart after each removal
        
        # Apply local search to polish
        if current_solution:
            current_solution = self._swap_local_search(current_solution)
            current_solution = self._merge_local_search(current_solution)
        
        return current_solution
