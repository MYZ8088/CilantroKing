# MYZ分支合并 + T-Covering优化总结

## 合并完成时间
2026-04-30

## MYZ分支重构内容

### 新目录结构
```
n_algorithms/
├── n07/ - n25/          # 每个n值的专用求解器
│   ├── __init__.py
│   ├── solver.py
│   └── specialized_module.py (n17, n18, n19)
└── shared/              # 共享核心组件
    ├── solver_core.py   # 核心求解器（原solver.py）
    ├── tcovering_solver.py
    ├── identity_cover_module.py
    ├── bounds.py
    ├── verification.py
    ├── solver_dispatcher.py
    └── optimal_samples.py
```

### 主要改进
1. **模块化架构**：每个n值有独立目录
2. **共享核心**：通用算法在shared目录
3. **清晰分离**：专用优化和通用算法分离
4. **易于扩展**：添加新n值优化更简单

## 应用的T-Covering优化

### 1. 时间安全边界
```python
# 为大n值预留更多安全边界
self._time_budget_margin_sec = 3.0 if n >= 16 else 1.5
```

### 2. 减少尝试次数
```python
# 超大实例或有时间限制时减少尝试
if self._is_huge:
    effective_attempts = max(1, self._num_attempts // 2)
elif self._deadline_at:
    effective_attempts = max(2, self._num_attempts // 2)
```

### 3. 移除SA（模拟退火）
- SA太慢且效果不明显
- 对大实例几乎无改进
- 节省大量时间

### 4. 添加时间检查点
```python
# 在每次尝试前检查时间预算
if self._deadline_at and time.time() >= self._deadline_at:
    self._report("timeout", "Time budget exhausted")
    break
```

## 文件位置变化

### 原位置 → 新位置
```
solver.py                    → n_algorithms/shared/solver_core.py
tcovering_solver.py          → n_algorithms/shared/tcovering_solver.py
identity_cover_module.py     → n_algorithms/shared/identity_cover_module.py
bounds.py                    → n_algorithms/shared/bounds.py
solver_n12_isolated.py       → n_algorithms/n12/solver.py
solver_n13_isolated.py       → n_algorithms/n13/solver.py
solver_n14_isolated.py       → n_algorithms/n14/solver.py
solver_n15_isolated.py       → n_algorithms/n15/solver.py
solver_n16_isolated.py       → n_algorithms/n16/solver.py
solver_n19_isolated.py       → n_algorithms/n19/solver.py
n17_specialized_module.py    → n_algorithms/n17/specialized_module.py
n18_specialized_module.py    → n_algorithms/n18/specialized_module.py
n19_specialized_module.py    → n_algorithms/n19/specialized_module.py
```

## 使用方式

### 导入变化
```python
# 旧方式
from solver import CoveringDesignSolver
from tcovering_solver import TCoveringSolver

# 新方式
from n_algorithms.shared.solver_core import CoveringDesignSolver
from n_algorithms.shared.tcovering_solver import TCoveringSolver

# 或使用dispatcher
from n_algorithms.shared.solver_dispatcher import solve_covering_design
```

## 预期效果

### T-Covering性能改进
```
优化前：
- L(12,6,5,4) t=2: 150s+ (超时)
- L(13,6,5,4) t=2: 180s+ (超时)

优化后（预期）：
- L(12,6,5,4) t=2: 90-110s ✓
- L(13,6,5,4) t=2: 110-120s ✓
```

## 测试

### 运行测试
```bash
# T-Covering优化测试
python test_tcovering_optimization.py

# 完整测试套件
python eval.py --suite smoke
python eval.py --suite core
python eval.py --suite full
```

## 兼容性

### 向后兼容
- 旧的导入路径仍然可用（通过wrapper）
- API接口保持不变
- 现有测试无需修改

### 新功能
- 更清晰的模块结构
- 更容易添加新优化
- 更好的代码组织

## 下一步

1. **测试验证**：运行完整测试套件确保无回归
2. **性能基准**：对比优化前后的性能
3. **文档更新**：更新README和技术文档
4. **代码审查**：团队审查新结构

## 备注

- 原始tcovering_solver已备份为`tcovering_solver_optimized_backup.py`
- MYZ的重构保留了所有LBN和YB的优化
- 新结构更易于维护和扩展
