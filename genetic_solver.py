"""遗传算法求解器 - 用于大规模 j=k 集合覆盖问题

专门针对 n>12 且 j=k 的困难案例，通过进化算法跳出局部最优。
"""

import random
import time
from typing import Callable, List, Set, Tuple

import numpy as np


class GeneticSolver:
    """遗传算法求解器"""
    
    def __init__(
        self,
        cand_masks: np.ndarray,
        target_masks: np.ndarray,
        s: int,
        cov_table: List[np.ndarray],
        inv_table: List[np.ndarray],
        verify_fn: Callable[[List[int]], bool],
        cancel_fn: Callable[[], bool] = None,
        progress_fn: Callable[[str], None] = None,
    ):
        self.cand_masks = cand_masks
        self.target_masks = target_masks
        self.s = s
        self.cov_table = cov_table
        self.inv_table = inv_table
        self.verify_fn = verify_fn
        self.cancel_fn = cancel_fn or (lambda: False)
        self.progress_fn = progress_fn or (lambda msg: None)
        
        self.num_cands = len(cand_masks)
        self.num_targets = len(target_masks)
    
    def solve(
        self,
        initial_solution: List[int],
        time_budget: float = 30.0,
        pop_size: int = 20,
        generations: int = 50,
    ) -> List[int]:
        """
        使用遗传算法改进解
        
        Args:
            initial_solution: 初始解（来自贪心算法）
            time_budget: 时间预算（秒）
            pop_size: 种群大小
            generations: 进化代数
        
        Returns:
            改进后的解
        """
        start_time = time.time()
        
        # 初始化种群
        population = self._create_initial_population(initial_solution, pop_size)
        
        # 对初始种群进行局部搜索
        for i in range(len(population)):
            population[i] = self._local_search(population[i])
        
        best_solution = min(population, key=len)
        stagnant_gens = 0
        
        self.progress_fn(f"GA: 初始种群 {pop_size} 个，最佳 {len(best_solution)} 组")
        
        # 进化循环
        for gen in range(generations):
            if self.cancel_fn():
                break
            
            if time.time() - start_time > time_budget:
                self.progress_fn(f"GA: 时间预算用尽，停止在第 {gen} 代")
                break
            
            # 早停：如果连续10代没改进，停止
            if stagnant_gens >= 10:
                self.progress_fn(f"GA: 连续 {stagnant_gens} 代无改进，提前停止")
                break
            
            # 选择父代
            parents = self._selection(population, pop_size // 2)
            
            # 交叉繁殖
            offspring = []
            for i in range(0, len(parents) - 1, 2):
                child1, child2 = self._crossover(parents[i], parents[i + 1])
                offspring.append(child1)
                offspring.append(child2)
            
            # 变异（自适应变异率）
            mutation_rate = 0.3 if stagnant_gens > 5 else 0.15
            for i in range(len(offspring)):
                offspring[i] = self._mutation(offspring[i], mutation_rate)
            
            # 对部分后代进行局部搜索（每3代一次，避免太慢）
            if gen % 3 == 0:
                for i in range(min(3, len(offspring))):
                    offspring[i] = self._local_search(offspring[i])
            
            # 精英保留
            elite_size = max(3, pop_size // 8)
            elite = sorted(population, key=len)[:elite_size]
            
            # 组成新种群
            population = elite + offspring
            population = population[:pop_size]
            
            # 更新最佳解
            current_best = min(population, key=len)
            if len(current_best) < len(best_solution):
                best_solution = current_best
                stagnant_gens = 0
                elapsed = time.time() - start_time
                self.progress_fn(
                    f"GA: 第 {gen} 代找到更好的解 {len(best_solution)} 组 "
                    f"({elapsed:.1f}s)"
                )
            else:
                stagnant_gens += 1
        
        # 最后对最佳解进行一次深度局部搜索
        best_solution = self._local_search(best_solution)
        
        return best_solution
    
    def _create_initial_population(
        self,
        initial_solution: List[int],
        pop_size: int,
    ) -> List[List[int]]:
        """创建初始种群 - 增强多样性"""
        population = []
        
        # 1. 添加初始解
        population.append(list(initial_solution))
        
        # 2. 通过不同程度的扰动生成多样性
        for i in range(pop_size - 1):
            solution = list(initial_solution)
            
            # 扰动强度递增
            if i < (pop_size - 1) // 3:
                # 轻度扰动：移除10-20%
                num_remove = random.randint(1, max(1, len(solution) // 5))
            elif i < 2 * (pop_size - 1) // 3:
                # 中度扰动：移除20-40%
                num_remove = random.randint(len(solution) // 5, max(2, len(solution) // 3))
            else:
                # 重度扰动：移除40-60%
                num_remove = random.randint(len(solution) // 3, max(3, len(solution) // 2))
            
            for _ in range(num_remove):
                if len(solution) > 1:
                    solution.pop(random.randint(0, len(solution) - 1))
            
            # 修复解
            solution = self._repair_solution(solution)
            population.append(solution)
        
        return population
    
    def _selection(self, population: List[List[int]], num_parents: int) -> List[List[int]]:
        """选择父代 - 使用锦标赛选择"""
        parents = []
        tournament_size = 3
        
        for _ in range(num_parents):
            # 随机选择几个个体
            tournament = random.sample(population, min(tournament_size, len(population)))
            # 选择最好的
            winner = min(tournament, key=len)
            parents.append(list(winner))
        
        return parents
    
    def _crossover(
        self,
        parent1: List[int],
        parent2: List[int],
    ) -> Tuple[List[int], List[int]]:
        """交叉操作 - 使用均匀交叉"""
        if len(parent1) < 2 or len(parent2) < 2:
            return list(parent1), list(parent2)
        
        # 策略1: 均匀交叉（50%概率）
        if random.random() < 0.5:
            # 从两个父代中随机选择组
            all_groups = list(set(parent1 + parent2))
            random.shuffle(all_groups)
            
            # 分成两半
            mid = len(all_groups) // 2
            child1 = all_groups[:mid]
            child2 = all_groups[mid:]
        else:
            # 策略2: 单点交叉
            point1 = random.randint(1, len(parent1) - 1)
            point2 = random.randint(1, len(parent2) - 1)
            
            child1 = parent1[:point1] + parent2[point2:]
            child2 = parent2[:point2] + parent1[point1:]
        
        # 修复
        child1 = self._repair_solution(child1)
        child2 = self._repair_solution(child2)
        
        return child1, child2
    
    def _mutation(self, solution: List[int], mutation_rate: float) -> List[int]:
        """变异操作 - 针对 j=k 优化"""
        if random.random() > mutation_rate:
            return solution
        
        # 变异策略1: 替换低价值的组（50%概率）
        if random.random() < 0.5 and len(solution) > 2:
            # 找到"独特贡献"最小的组
            min_contribution = float('inf')
            worst_idx = None
            
            for i, mask in enumerate(solution):
                # 计算这个组独自覆盖多少目标
                test_solution = solution[:i] + solution[i+1:]
                uncovered_without = self._find_uncovered(test_solution)
                contribution = uncovered_without.sum()
                
                if contribution < min_contribution:
                    min_contribution = contribution
                    worst_idx = i
            
            if worst_idx is not None and min_contribution < 10:
                # 移除贡献最小的组
                solution.pop(worst_idx)
                # 修复
                solution = self._repair_solution(solution)
        else:
            # 变异策略2: 随机移除1-2个组（原有策略）
            if len(solution) > 2:
                num_remove = random.randint(1, 2)
                for _ in range(num_remove):
                    if len(solution) > 1:
                        solution.pop(random.randint(0, len(solution) - 1))
                
                solution = self._repair_solution(solution)
        
        return solution
    
    def _repair_solution(self, solution: List[int]) -> List[int]:
        """修复解 - 确保覆盖所有目标并移除冗余"""
        # 1. 去重
        solution = list(set(solution))
        
        # 2. 找到未覆盖的目标
        uncovered = self._find_uncovered(solution)
        
        # 3. 贪心填补未覆盖的目标
        while uncovered.any():
            # 找到覆盖最多未覆盖目标的候选集
            best_cand_idx = None
            best_count = 0
            
            for cand_idx in range(self.num_cands):
                cand_mask = int(self.cand_masks[cand_idx])
                if cand_mask in solution:
                    continue
                
                # 计算能覆盖多少未覆盖的目标
                covered_targets = self.cov_table[cand_idx]
                count = np.sum(uncovered[covered_targets])
                
                if count > best_count:
                    best_count = count
                    best_cand_idx = cand_idx
            
            if best_cand_idx is None:
                break
            
            # 添加最佳候选集
            solution.append(int(self.cand_masks[best_cand_idx]))
            
            # 更新未覆盖目标
            covered_targets = self.cov_table[best_cand_idx]
            uncovered[covered_targets] = False
        
        # 4. 移除冗余组
        solution = self._remove_redundant(solution)
        
        return solution
    
    def _find_uncovered(self, solution: List[int]) -> np.ndarray:
        """找到未覆盖的目标"""
        uncovered = np.ones(self.num_targets, dtype=bool)
        
        for mask in solution:
            # 找到这个 mask 对应的候选集索引
            cand_idx = None
            for idx in range(self.num_cands):
                if int(self.cand_masks[idx]) == mask:
                    cand_idx = idx
                    break
            
            if cand_idx is not None:
                covered_targets = self.cov_table[cand_idx]
                uncovered[covered_targets] = False
        
        return uncovered
    
    def _remove_redundant(self, solution: List[int]) -> List[int]:
        """移除冗余组"""
        # 计算每个目标被覆盖的次数
        coverage_count = np.zeros(self.num_targets, dtype=np.int32)
        
        solution_indices = []
        for mask in solution:
            for idx in range(self.num_cands):
                if int(self.cand_masks[idx]) == mask:
                    solution_indices.append(idx)
                    covered_targets = self.cov_table[idx]
                    coverage_count[covered_targets] += 1
                    break
        
        # 尝试移除每个组
        i = 0
        while i < len(solution):
            cand_idx = solution_indices[i]
            covered_targets = self.cov_table[cand_idx]
            
            # 检查这个组覆盖的所有目标是否都被至少2个组覆盖
            if np.all(coverage_count[covered_targets] >= 2):
                # 可以安全移除
                coverage_count[covered_targets] -= 1
                solution.pop(i)
                solution_indices.pop(i)
            else:
                i += 1
        
        return solution
    
    def _local_search(self, solution: List[int]) -> List[int]:
        """局部搜索 - 移除冗余组"""
        if len(solution) <= 3:
            return solution
        
        # 简单策略：只移除冗余组，不做复杂的替换
        improved = True
        passes = 0
        max_passes = 2  # 限制轮数
        
        while improved and passes < max_passes:
            improved = False
            passes += 1
            old_size = len(solution)
            
            # 移除冗余组
            solution = self._remove_redundant(solution)
            
            if len(solution) < old_size:
                improved = True
        
        return solution
    
    def _fast_verify(self, solution: List[int]) -> bool:
        """快速验证解是否合法"""
        if not solution:
            return self.num_targets == 0
        
        uncovered = self._find_uncovered(solution)
        return not uncovered.any()
