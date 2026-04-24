"""CP-SAT 求解器 - 用于 j=k 的集合覆盖问题

使用 Google OR-Tools 的约束编程求解器，可以找到最优或接近最优的解。
特别适合 j=k 的情况，因为问题退化为经典的集合覆盖。
"""

import time
from typing import Callable, List

import numpy as np
from ortools.sat.python import cp_model


class CPSATSolver:
    """CP-SAT 约束编程求解器"""
    
    def __init__(
        self,
        cand_masks: np.ndarray,
        target_masks: np.ndarray,
        s: int,
        cov_table: List[np.ndarray],
        cancel_fn: Callable[[], bool] = None,
        progress_fn: Callable[[str], None] = None,
    ):
        self.cand_masks = cand_masks
        self.target_masks = target_masks
        self.s = s
        self.cov_table = cov_table
        self.cancel_fn = cancel_fn or (lambda: False)
        self.progress_fn = progress_fn or (lambda msg: None)
        
        self.num_cands = len(cand_masks)
        self.num_targets = len(target_masks)
    
    def solve(
        self,
        initial_solution: List[int] = None,
        time_limit: float = 60.0,
    ) -> List[int] | None:
        """
        使用 CP-SAT 求解
        
        Args:
            initial_solution: 初始解（用于设置上界）
            time_limit: 时间限制（秒）
        
        Returns:
            最优或接近最优的解，如果失败返回 None
        """
        # 早期检查：问题规模是否合理
        if self.num_cands > 10000 or self.num_targets > 5000:
            self.progress_fn(f"CP-SAT: 问题规模过大 ({self.num_cands} 候选, {self.num_targets} 目标)，跳过")
            return None
        
        start_time = time.time()
        
        self.progress_fn(f"CP-SAT: 构建模型 ({self.num_cands} 候选, {self.num_targets} 目标)")
        
        # 1. 创建模型
        model = cp_model.CpModel()
        
        # 2. 变量：x[i] = 1 表示选择候选集 i
        x = [model.NewBoolVar(f'x_{i}') for i in range(self.num_cands)]
        
        # 3. 约束：每个目标至少被一个候选集覆盖
        # 预先构建反向索引：target -> 覆盖它的候选集列表
        target_to_cands = [[] for _ in range(self.num_targets)]
        for cand_idx in range(self.num_cands):
            for target_idx in self.cov_table[cand_idx]:
                target_to_cands[target_idx].append(cand_idx)
        
        # 添加覆盖约束
        for target_idx in range(self.num_targets):
            covering_cands = target_to_cands[target_idx]
            
            if not covering_cands:
                self.progress_fn(f"CP-SAT: 警告 - 目标 {target_idx} 无法被覆盖")
                return None
            
            # 至少选择一个覆盖候选
            model.Add(sum(x[i] for i in covering_cands) >= 1)
        
        # 4. 目标：最小化选中的候选集数量
        model.Minimize(sum(x))
        
        # 5. 设置初始解作为提示（如果提供）
        if initial_solution:
            self.progress_fn(f"CP-SAT: 使用初始解 {len(initial_solution)} 组作为上界")
            # 将初始解转换为候选集索引
            initial_indices = []
            for mask in initial_solution:
                for idx in range(self.num_cands):
                    if int(self.cand_masks[idx]) == mask:
                        initial_indices.append(idx)
                        break
            
            # 设置提示
            for idx in initial_indices:
                model.AddHint(x[idx], 1)
        
        # 6. 配置求解器
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        solver.parameters.num_search_workers = 4  # 并行搜索
        solver.parameters.log_search_progress = False
        
        self.progress_fn(f"CP-SAT: 开始求解 (时间限制 {time_limit:.1f}s)")
        
        # 7. 求解
        status = solver.Solve(model)
        
        elapsed = time.time() - start_time
        
        # 8. 处理结果
        if status == cp_model.OPTIMAL:
            self.progress_fn(f"CP-SAT: 找到最优解！({elapsed:.1f}s)")
        elif status == cp_model.FEASIBLE:
            self.progress_fn(f"CP-SAT: 找到可行解 ({elapsed:.1f}s)")
        else:
            self.progress_fn(f"CP-SAT: 未找到解 (状态: {status})")
            return None
        
        # 9. 提取解
        solution = []
        for i in range(self.num_cands):
            if solver.Value(x[i]) == 1:
                solution.append(int(self.cand_masks[i]))
        
        obj_value = solver.ObjectiveValue()
        self.progress_fn(f"CP-SAT: 解的大小 = {obj_value}")
        
        # 10. 显示求解统计
        if initial_solution:
            improvement = len(initial_solution) - len(solution)
            if improvement > 0:
                self.progress_fn(f"CP-SAT: 改进 {improvement} 组 ({len(initial_solution)} → {len(solution)})")
        
        return solution
