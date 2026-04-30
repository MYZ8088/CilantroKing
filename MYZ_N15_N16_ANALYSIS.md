# MYZ分支N15/N16优化分析

## 架构差异

### MYZ分支架构
```
optimal_samples.py (主入口)
  ↓
solver_dispatcher.py (分发器)
  ↓
n15_solver.py / n16_solver.py (专用solver)
```

### 当前架构
```
solver.py (统一solver)
  ↓
各种phase方法
  ↓
specialized modules (n17/n18)
isolated solvers (n12/n13/n14/n15/n19)
```

## MYZ的N15/N16优化方法

### 核心算法
1. **Orbit-based ILP** (Integer Linear Programming)
   - 使用循环对称性减少变量数
   - 适用于某些特定case

2. **Bitmask Random Greedy + LNS + ILP**
   - Bitmask greedy: 位掩码加速的贪心算法
   - LNS (Large Neighborhood Search): 大邻域搜索
   - ILP: 整数线性规划精炼

3. **配置驱动**
   ```python
   N_SOLVER_CONFIGS = {
       15: NSolverConfig(15, 50.0, 140, 36.0, 4.0, 65.0, 10_000_000),
       16: NSolverConfig(16, 60.0, 150, 40.0, 4.0, 70.0, 12_000_000),
   }
   ```

### 性能结果

#### N=15 (30 cases)
- 完全验证: 30/30
- 比例≤1.21: 26/30
- 最差比例: L_15_6_6_5 = 1.3380 (33.80% over baseline)
- 最慢case: L_15_7_5_3 = 1503.231s

#### N=16 (29 cases)
- 完全验证: 29/29
- 比例≤1.21: 20/29
- 最差比例: L_16_7_7_5 = 1.3548 (35.48% over baseline)
- 最慢case: L_16_7_7_6 = 145.976s

## 集成挑战

### 1. API不兼容
MYZ使用完全不同的API：
```python
def solve_n_15(problem, oracle, rng, deadline, tools) -> tuple[tuple[tuple[int, ...], ...], str]
```

当前solver使用：
```python
class CoveringDesignSolver:
    def solve(self) -> SolverResult
```

### 2. 依赖不同
MYZ需要：
- `oracle` 对象（验证和掩码操作）
- `tools` 对象（各种工具函数）
- `rng` 随机数生成器
- 完全不同的数据结构

### 3. 算法完全不同
- MYZ: ILP-based, orbit-based
- 当前: Greedy + SA + CP-SAT

## 集成方案

### 方案1：创建Isolated Solver（推荐）
类似n19的方式，创建：
- `solver_n15_isolated.py`
- `solver_n16_isolated.py`

在主solver中委托：
```python
if self.__class__ is CoveringDesignSolver and self.n == 15:
    from solver_n15_isolated import CoveringDesignSolver as N15IsolatedSolver
    delegated = N15IsolatedSolver(...)
    return delegated.solve()
```

**优点**：
- 保持架构一致性
- 可以逐步迁移

**缺点**：
- 需要适配API
- 需要实现oracle和tools

### 方案2：直接使用MYZ的solver
将n15_solver.py和n16_solver.py复制过来，创建适配层。

**优点**：
- 保留MYZ的所有优化

**缺点**：
- 需要大量适配工作
- 维护两套代码

### 方案3：提取算法，重写
提取MYZ的核心算法思想，用当前架构重写。

**优点**：
- 架构统一

**缺点**：
- 工作量巨大
- 可能丢失优化细节

## 建议

### 短期（当前合并）
**暂不集成MYZ的n15/n16优化**，原因：
1. 架构完全不兼容
2. 需要大量适配工作
3. 当前已有n12/n13/n14优化

### 中期（后续优化）
1. 创建solver_n15_isolated.py和solver_n16_isolated.py
2. 适配MYZ的算法到当前API
3. 在主solver中添加委托

### 长期（架构统一）
考虑是否要统一所有n≤16的solver到isolated模式。

## 当前状态

**已集成的优化**：
- ✅ N12 (LBN)
- ✅ N13 (LBN)
- ✅ N14 (LBN)
- ✅ N17 (YB)
- ✅ N18 (YB)
- ✅ N19 (YB)

**待集成的优化**：
- ⏳ N15 (MYZ) - 需要适配
- ⏳ N16 (MYZ) - 需要适配

## 结论

MYZ的n15/n16优化使用了完全不同的架构和算法，无法直接集成到当前合并中。建议：

1. **当前合并**：完成n12/n13/n14/n17/n18/n19的集成
2. **后续工作**：单独创建task来适配n15/n16优化

这样可以：
- 保证当前合并的质量
- 避免引入过多复杂性
- 为后续优化留出空间
