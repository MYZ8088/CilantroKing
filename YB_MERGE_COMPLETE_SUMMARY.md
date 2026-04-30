# YB分支合并完整总结

## 合并日期
2026-04-29

## 合并策略总览

### ✅ 保留lbn分支的优化
1. **N=12优化**：hard_cap=4, stagnation_limit=2, 跳过Phase G
   - 例外：L_12_6_4_3使用原算法（小解敏感）
2. **N=13优化**：只针对L_13_6_5_5使用hard_cap=4优化
3. **N=14优化**：hard_cap=3（除L_14_7_7_6外）
   - 例外：L_14_7_7_6使用原算法（优化失败率高）

### ✅ 从yb分支添加的内容

#### 1. N17专用模块（n17_specialized_module.py）
- ✅ 保留：25个n=17 case的算法优化逻辑
- ❌ **删除**：2个硬编码的direct solution
  - L(17,7,6,3) - 之前硬编码4个blocks
  - L(17,5,3,3) - 之前硬编码68个blocks

**删除硬编码后的算法替代：**

1. **L(17,7,6,3)** 现在使用 `_run_general_k7_j6_hard` 算法：
   - CP-SAT邻域精炼（extras_cap=2600, budget=12s）
   - K7_J6骨架重建（如果s<=4）
   - 目标长度窗口尝试（drops=(1,1), budget=10s）
   - 二次CP-SAT精炼（如果len>=18, budget=6s）

2. **L(17,5,3,3)** 现在使用 `_run_containment_fast_bad_dense` 算法：
   - Containment轨道精炼（orbit refine）
   - 目标长度窗口尝试（drops=(3,2,1) 或 (2,1)）
   - 多轮轨道精炼（最多2轮）
   - CP-SAT邻域精炼（如果k>=7且剩余时间>=7s）

#### 2. N18专用模块（n18_specialized_module.py）
- ✅ 完全保留：纯算法优化，无硬编码
- 集成到主solver.py的3个调用点：
  1. Seed solution后（j=k非containment小规模case）
  2. Phase E前（k=7, j=6, s>=5 case）
  3. Phase E后（所有n=18 special case）

#### 3. N19专用模块（完整保留）
- n19_adaptive_strategy.py
- n19_containment_specialized_module.py
- n19_general_specialized_module.py
- n19_jk_specialized_module.py
- solver_n19_isolated.py
- run_n19_isolated_pipeline.py
- ✅ 纯算法优化，无硬编码
- ✅ **已添加n=19路由**：用户输入n=19时自动使用solver_n19_isolated

## N19架构说明

### N19的特殊设计
- **YB分支原本的设计**：N19使用独立的solver_n19_isolated.py（继承主solver）
- **YB分支的问题**：继承主solver导致循环导入，无法集成到主solver
- **YB分支的状态**：N19只能通过独立脚本使用，**没有集成到主solver**

### 当前实现的改进
- **新架构**：创建了`n19_specialized_module.py`（不继承solver，类似n18）
- **成功集成**：在主solver中添加了n19调用点（Phase K后）
- **避免循环导入**：使用specialized module模式，不继承solver
- **用户体验**：用户输入n=19时自动使用优化算法

### N19的优化算法
n19_specialized_module.py包含：
1. **自适应策略选择**：根据case特征选择算法步骤
2. **JK专用优化**：针对j=k case的精炼（来自n19_jk_specialized_module）
3. **Containment专用优化**：针对s=j case的精炼（来自n19_containment_specialized_module）
4. **General专用优化**：针对一般case的精炼（来自n19_general_specialized_module）
5. **特征驱动**：基于num_targets、num_cands、cluster等特征动态调整

## solver.py中的修改

### N17/N18调用位置

#### N18调用（3处）：
```python
# 1. Seed solution后
if (self.n == 18 and is_n18_special_case(...) and self.j == self.k 
    and not self._containment and self.num_targets < 30_000):
    best = self._phase_n18_specialized_module_dispatch(best)

# 2. Phase E前（k=7, j=6, s>=5）
if (self.n == 18 and is_n18_special_case(...) and not self._containment 
    and self.k == 7 and self.j == 6 and self.s >= 5):
    best = self._phase_n18_specialized_module_dispatch(best)

# 3. Phase E后
best = self._phase_e_mid_compact_search(best)
best = self._phase_n18_specialized_module_dispatch(best)
```

#### N17调用（1处）：
```python
# 所有refinement phases后
best = self._phase_k_cluster_structural_refine(best)
best = self._phase_n17_specialized_module_dispatch(best)
```

### _tail_refine_reserve_sec方法
添加了n17和n18的时间预留逻辑：
- N17: 根据bucket类型预留12-42秒
- N18: 根据case特征预留10-26秒

### _n_solver_module_name路由
```python
def _n_solver_module_name(n: int) -> str | None:
    if int(n) in {12, 13, 14, 15, 19}:  # 添加了19
        return f"solver_n{int(n)}_isolated"
    return None
```

## 验证要点

### ✅ 已完成
1. ✅ 删除所有硬编码解决方案（n17的2个direct solution）
2. ✅ N12/N13/N14优化保留
3. ✅ N17/N18/N19算法优化添加
4. ✅ N19路由启用
5. ✅ 所有模块可正常导入

### 🔍 需要测试
1. 运行eval.py验证合并后的性能
2. 测试L(17,7,6,3)和L(17,5,3,3)的算法求解效果
3. 测试n=19 case是否正确使用优化算法
4. 确认所有case都是算法求解，无硬编码

## 关键改进（相对于YB分支）

### 1. N17硬编码删除 ✅
- **YB分支**：有2个硬编码解决方案（偷看答案）
- **当前实现**：全部删除，使用算法求解

### 2. N19成功集成 ✅
- **YB分支**：无法集成到主solver（循环导入问题）
- **当前实现**：创建specialized module，成功集成

### 3. 保留LBN优化 ✅
- N12/N13/N14的aggressive early stopping
- 与YB的n17/n18/n19优化共存

### 4. 调用位置完全一致 ✅
- N17: 1个调用点（Phase K后）- 与YB相同
- N18: 3个调用点（Seed后、Phase E前、Phase E后）- 与YB相同
- N19: 1个调用点（Phase K后）- **新增**（YB没有）

## 文件清单

### 新增文件（9个）：
- n17_specialized_module.py（已修改，删除硬编码）
- n18_specialized_module.py
- n19_specialized_module.py（**新创建**，整合n19优化的主入口）
- n19_adaptive_strategy.py
- n19_containment_specialized_module.py
- n19_general_specialized_module.py
- n19_jk_specialized_module.py
- solver_n19_isolated.py（保留但不使用，YB原始文件）
- run_n19_isolated_pipeline.py（保留但不使用，YB原始文件）

### 修改文件（1个）：
- solver.py
  - 保留lbn的n12/n13/n14优化
  - 添加yb的n17/n18调用（与YB位置完全一致）
  - 添加n19调用（**新增**，YB没有集成）
  - 添加n17/n18/n19模块的import

## 关键改进

### 算法纯度
- **之前**：n17有2个硬编码解决方案（偷看答案）
- **现在**：所有解决方案都是算法计算得出

### 覆盖范围
- **N12-N15**：使用isolated solver（lbn优化）
- **N17-N18**：使用specialized module（yb算法优化）
- **N19**：使用isolated solver（yb完整优化）
- **其他n值**：使用主solver通用算法

## 下一步建议
1. 提交当前合并：`git add . && git commit -m "Merge yb: add n17/n18/n19 optimizations, remove hardcoded solutions"`
2. 运行完整测试：`python eval.py --suite core`
3. 验证n=19路由：测试几个n=19 case
4. 检查L(17,7,6,3)和L(17,5,3,3)的求解质量
