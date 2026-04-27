# 当前算法架构说明

## 概述

本项目实现了一个多阶段、自适应的覆盖设计求解器，针对不同规模和类型的问题使用不同的优化策略。

**最新更新：2026-04-26 - 合并yb分支并保留t>1支持**

## 核心架构

### 1. 问题分类与路由

求解器首先根据问题特征进行分类和路由：

```
输入: L(n, k, j, s, t)
  ↓
判断问题类型:
  - t > 1 → TCoveringSolver (专用求解器)
  - s == j == k → Identity Cover (显式构造)
  - n ≤ 某阈值 → Small Exact Cover (精确求解)
  - 其他 → 主求解流程
```

### 2. 主求解流程 (solve方法)

#### Phase A: 多次尝试循环 (Multi-Attempt Loop)

```python
for attempt in range(1, hard_cap):
    # 1. 贪心构造初始解
    sol = self._greedy(profile)
    
    # 2. 优化解
    sol = self._optimise_solution(sol, profile)
    
    # 3. 更新最优解
    if len(sol) < len(best):
        best = sol
```

**关键特性：**
- 自适应尝试次数：小问题5次，大问题1-2次
- 早停机制：连续无改进时提前终止
- 时间预算管理：为后续优化阶段预留时间

#### Phase B-D: 解优化 (_optimise_solution)

```python
def _optimise_solution(sol):
    # Phase B: 策略变体选择
    profile = self._phase_b_strategy_variant(base_profile, attempt)
    
    # Phase C: 局部搜索
    sol = self._local_search(sol)
    sol = self._swap_improve(sol)
    sol = self._destroy_repair(sol)
    sol = self._simulated_annealing(sol)
    
    # Phase D: 特定问题优化
    sol = self._targeted_drop_one(sol)
    
    return sol
```

#### Phase E-K: 后处理优化阶段

合并yb分支后，增加了多个专门的优化阶段：

```python
if best is not None:
    # Phase E: 中等规模j=k紧凑搜索
    best = self._phase_e_mid_compact_search(best)
    
    # Phase F: CP-SAT精炼
    best = self._phase_f_small_cp_sat_polish(best)
    best = self._phase_f_mid_cp_sat_refine(best)
    
    # Phase N16: n=16锚点模块调度
    best = self._phase_n16_anchor_module_dispatch(best)
    
    # Phase I: n<16聚类专用精炼
    best = self._phase_i_nlt16_cluster_specialized_refine(best)
    
    # Phase K: 聚类结构精炼
    best = self._phase_k_cluster_structural_refine(best)
    
    # Phase H: n<16 CP-SAT精炼
    best = self._phase_h_nlt16_cp_sat_refine(best)
    
    # Phase G: n<16固定大小抛光
    best = self._phase_g_nlt16_fixed_size_polish(best)
    
    # 对n<16的问题，重复H/I/K阶段
    if self.n < 16:
        for _ in range(2):
            best = self._phase_h_nlt16_cp_sat_refine(best)
            best = self._phase_i_nlt16_cluster_specialized_refine(best)
            best = self._phase_k_cluster_structural_refine(best)
    
    # Phase N15: n=15困难案例模块调度
    best = self._phase_n15_hardcase_module_dispatch(best)
```

### 3. 专用模块

#### n=15 专用模块 (n15_specialized_module.py)

针对15个特殊案例的优化：
- 识别特殊案例：13-15范围内的困难问题
- 家族分类：j=k非包含、包含、一般非包含
- 定制优化序列：每个家族有专门的优化操作序列

**特殊案例列表：**
```python
(13, 6, 6, 5): 61 组
(14, 7, 6, 6): 501 组
(15, 7, 6, 6): 817 组
... 等15个案例
```

#### n=16 专用模块 (n16_specialized_module.py)

针对n=16问题的锚点优化：
- 更复杂的优化策略
- 针对大规模问题的特殊处理

### 4. 优化技术详解

#### Phase C: 局部搜索技术

1. **Swap Improve (交换改进)**
   - 尝试用更好的候选替换现有候选
   - 基于覆盖度和稀有度评分

2. **Destroy-Repair (破坏-修复)**
   - 移除部分候选
   - 用贪心方法修复
   - 探索不同的解空间区域

3. **Simulated Annealing (模拟退火)**
   - 接受概率：P = exp(-Δ/T)
   - 温度递减：T = T * cooling_rate
   - 逃离局部最优

#### Phase I: 聚类专用精炼

根据问题类型选择不同的优化模块：

1. **j=k 循环模块** (_phase_i_jk_cycle_module)
   - 针对j=k非包含问题
   - 使用循环结构优化

2. **包含循环模块** (_phase_i_containment_cycle_module)
   - 针对s=j包含问题
   - 利用包含关系优化

3. **一般小规模模块** (_phase_i_general_small_module)
   - 针对一般非包含问题
   - 通用优化策略

4. **完整CP-SAT模块** (_phase_i_full_cp_sat_module)
   - 使用约束编程求解器
   - 可选hard_case模式

#### Phase K: 结构精炼技术

1. **轨道CP-SAT精炼** (_phase_k_jk_orbit_cp_sat_refine)
   - 利用对称性
   - 减少搜索空间

2. **支配集精炼** (_phase_k_jk_kminus1_domset_refine)
   - 基于支配集理论
   - 移除冗余候选

3. **迭代SAT精炼** (_phase_k_containment_iterative_sat_refine)
   - 迭代应用约束求解
   - 逐步改进解

### 5. 时间管理策略

#### 时间预算分配

```python
# 安全边际
margin = 2.5秒 (n≥16) 或 0.8秒 (n<16)
deadline = start_time + (time_budget - margin)

# 尾部优化预留
if n < 16:
    reserve = 计算预留时间
    if remaining <= reserve:
        break  # 提前停止主循环，为cluster模块预留时间
```

#### 自适应时间分配

- 小问题：更多时间用于多次尝试
- 大问题：更多时间用于单次深度优化
- 根据剩余时间动态调整优化强度

### 6. GPU加速

```python
if self._gpu_enabled:
    # 使用CuPy进行批量评分
    scores = self._gpu_batch_score(candidates, targets)
```

**启用条件：**
- 环境变量 CK_USE_GPU=1
- 安装了CuPy
- 交互规模 ≥ gpu_min_interaction (可配置)
- GPU可用

## 算法改进历史

### yb分支的主要改进

1. **专用模块系统**
   - n15_specialized_module: 15个特殊案例
   - n16_specialized_module: n=16锚点优化
   - special5_case_module: 5个特殊案例

2. **多阶段优化流程**
   - 从原来的3个阶段扩展到10+个阶段
   - 每个阶段针对特定问题类型

3. **时间管理改进**
   - 安全边际机制
   - 尾部优化预留
   - 更精细的时间分配

4. **CP-SAT深度集成**
   - 多个CP-SAT优化阶段
   - 针对不同问题类型的CP-SAT策略

### 保留的t>1支持

虽然yb分支移除了t>1支持，但在合并时保留了：
- TCoveringSolver委托机制
- t参数验证
- 向后兼容性

## 性能特征

### 时间复杂度

- 贪心构造：O(num_cands * num_targets)
- 局部搜索：O(solution_size² * num_targets)
- 模拟退火：O(iterations * neighborhood_size)
- CP-SAT：取决于问题规模和约束复杂度

### 空间复杂度

- 覆盖表：O(num_cands * avg_coverage)
- 逆表：O(num_targets * avg_inverse)
- GPU缓存：O(num_cands + num_targets) (如果启用)

### 典型运行时间

- 小问题 (n≤12): 0.1-2秒
- 中等问题 (n=13-15): 2-30秒
- 大问题 (n=16-18): 30-120秒
- 超大问题 (n≥19): 120-600秒

## 质量保证

### 验证机制

```python
def _verify(self, solution):
    # 检查所有目标是否被覆盖
    covered = set()
    for cand in solution:
        covered.update(targets_covered_by(cand))
    return len(covered) == num_targets
```

### 质量评估

- 与理论下界比较 (Schönheim, Volume)
- 与LJCR已知值比较
- 计算质量比率 (result / baseline)

## 配置选项

### 环境变量

- `CK_USE_GPU`: 启用GPU加速 (默认1)
- `CK_GPU_MIN_INTERACTION`: GPU最小交互规模 (默认0)
- `CK_DISABLE_CPSAT`: 禁用CP-SAT (默认0)
- `CK_N16_ANCHOR_MODULE`: 启用n16锚点模块 (默认0)
- `CK_N15_HARDCASE_MODULE`: 启用n15困难案例模块 (默认1)

### 求解器参数

- `num_attempts`: 尝试次数 (默认3)
- `time_budget_sec`: 时间预算 (默认None=无限制)
- `skip_final_verify`: 跳过最终验证 (默认False)

## 相关文件

- `solver.py`: 主求解器实现
- `n15_specialized_module.py`: n=15专用模块
- `n16_specialized_module.py`: n=16专用模块
- `special5_case_module.py`: 5个特殊案例
- `tcovering_solver.py`: t>1求解器
- `identity_cover_module.py`: 显式构造模块
- `bounds.py`: 理论下界和LJCR数据
- `eval.py`: Benchmark评估工具
- `ALGORITHM_EXPLANATION.md`: 算法终止条件详解

## 未来改进方向

1. **更多专用模块**: 针对n=17-18的优化
2. **机器学习集成**: 学习最优策略选择
3. **并行化**: 多线程/多进程加速
4. **增量求解**: 利用历史解加速
5. **自适应参数**: 根据问题特征自动调整参数

---

最后更新：2026-04-26
版本：yb分支合并版 (保留t>1支持)
