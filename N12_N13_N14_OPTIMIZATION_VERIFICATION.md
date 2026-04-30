# N12/N13/N14优化验证报告

## 验证时间
2026-04-30

## 验证结果：✅ 所有优化已保留

MYZ重构后的代码结构完整保留了所有n12/n13/n14优化，并且采用了更清晰的模块化架构。

---

## N12优化详情

### 位置
`n_algorithms/shared/solver_core.py`

### 优化内容

#### 1. 主循环优化（激进早停）
```python
# Line 824-826
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    hard_cap = min(hard_cap, 4)  # 最多4次尝试
    stagnation_limit_override = 2  # 停滞2次就停止
```

**例外情况**：`L_12_6_4_3` 使用原始算法（太敏感，不适合优化）

#### 2. 跳过Phase G（贪婪后处理）
```python
# Line 1053-1055
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    pass  # Skip Phase G for optimized n=12 cases
```

#### 3. 减少最终精炼轮数
```python
# Line 1067-1070
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    final_rounds = 1  # 只做1轮精炼
    final_time_threshold = 2.0  # 时间阈值2秒
```

#### 4. Phase F时间预算优化
```python
# Line 3793-3800
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    if self.num_cands <= 320:
        cap = 2.0  # 小实例：2秒
    elif self.num_cands <= 500:
        cap = 3.0  # 中实例：3秒
    else:
        cap = 4.0  # 大实例：4秒
```

#### 5. Phase H时间预算优化
```python
# Line 4242-4257
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    if self._containment:
        frac = 0.08  # 包含情况：8%时间
        cap = 5.0
    else:
        frac = 0.06  # 非包含情况：6%时间
        cap = 3.0
    budget = max(floor, min(cap, remaining_sec * frac))
    return max(0.0, min(remaining_sec - 0.8, budget))
```

#### 6. Phase H轮数优化
```python
# Line 4583-4585
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    rounds = 4  # 4轮迭代
```

#### 7. Phase I时间预算优化
```python
# Line 4691-4706
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    if self._containment:
        frac = 0.10  # 包含情况：10%时间
        cap = 6.0
    else:
        frac = 0.06  # 非包含情况：6%时间
        cap = 3.0
    budget = max(floor, min(cap, remaining_sec * frac))
    return max(0.0, min(remaining_sec - 0.8, budget))
```

#### 8. Phase I轮数优化
```python
# Line 4793-4795
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    rounds = 2  # 2轮迭代
```

#### 9. Phase K时间预算优化
```python
# Line 4869-4879
if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
    if self._containment:
        budget_cap = min(budget_cap, 5.0)
        ratio = min(ratio, 0.08)
    else:
        budget_cap = min(budget_cap, 3.0)
        ratio = min(ratio, 0.06)
```

### N12优化策略总结
- **目标**：10%误差容忍度，快速收敛
- **方法**：激进早停 + 跳过耗时阶段 + 减少精炼轮数
- **例外**：L_12_6_4_3（太敏感，使用原始算法）

---

## N13优化详情

### 位置
`n_algorithms/shared/solver_core.py`

### 优化内容

#### 1. 主循环优化（仅L_13_6_5_5）
```python
# Line 827-829
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    hard_cap = min(hard_cap, 4)  # 最多4次尝试
    stagnation_limit_override = 2  # 停滞2次就停止
```

**注意**：只有 `L_13_6_5_5` 使用优化，其他n=13情况使用原始算法

#### 2. 跳过Phase G（仅L_13_6_5_5）
```python
# Line 1055-1057
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    pass  # Skip Phase G for L_13_6_5_5
```

#### 3. 减少最终精炼轮数（仅L_13_6_5_5）
```python
# Line 1070-1073
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    final_rounds = 1  # 只做1轮精炼
    final_time_threshold = 2.0  # 时间阈值2秒
```

#### 4. Phase F时间预算优化（仅L_13_6_5_5）
```python
# Line 3800-3807
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    if self.num_cands <= 320:
        cap = 2.0
    elif self.num_cands <= 500:
        cap = 3.0
    else:
        cap = 4.0
```

#### 5. Phase H时间预算优化（仅L_13_6_5_5）
```python
# Line 4257-4264
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    # L_13_6_5_5: j≠k case
    frac = 0.06
    cap = 3.0
    floor = 0.5
    budget = max(floor, min(cap, remaining_sec * frac))
    return max(0.0, min(remaining_sec - 0.8, budget))
```

#### 6. Phase H轮数优化（仅L_13_6_5_5）
```python
# Line 4585-4587
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    rounds = 4
```

#### 7. Phase I时间预算优化（仅L_13_6_5_5）
```python
# Line 4706-4713
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    # L_13_6_5_5: j≠k case
    frac = 0.06
    cap = 3.0
    floor = 0.5
    budget = max(floor, min(cap, remaining_sec * frac))
    return max(0.0, min(remaining_sec - 0.8, budget))
```

#### 8. Phase I轮数优化（仅L_13_6_5_5）
```python
# Line 4795-4797
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    rounds = 2
```

#### 9. Phase K时间预算优化（仅L_13_6_5_5）
```python
# Line 4879-4883
elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
    # L_13_6_5_5: j≠k case
    budget_cap = min(budget_cap, 3.0)
    ratio = min(ratio, 0.06)
```

### N13优化策略总结
- **目标**：针对特定困难情况（L_13_6_5_5）优化
- **方法**：与n=12相同的优化策略
- **范围**：仅 `L_13_6_5_5`，其他情况使用原始算法

---

## N14优化详情

### 位置
`n_algorithms/shared/solver_core.py`

### 优化内容

#### 1. 主循环优化（除L_14_7_7_6外）
```python
# Line 830-833
elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
    # All n=14 except L_14_7_7_6: use hard_cap=3
    hard_cap = min(hard_cap, 3)  # 最多3次尝试
    stagnation_limit_override = 2  # 停滞2次就停止
```

**例外情况**：`L_14_7_7_6` 使用原始算法（太困难，不适合优化）

#### 2. Phase F时间预算优化（除L_14_7_7_6外）
```python
# Line 3807-3815
elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
    # N=14 except L_14_7_7_6: moderate time budget
    if self.num_cands <= 320:
        cap = 2.5
    elif self.num_cands <= 500:
        cap = 3.5
    else:
        cap = 5.0
```

#### 3. Phase H时间预算优化（除L_14_7_7_6外）
```python
# Line 4264-4271
elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
    # Other n=14 except L_14_7_7_6: simple fast iteration (like n=12)
    frac = 0.06
    cap = 3.0
    floor = 0.5
    budget = max(floor, min(cap, remaining_sec * frac))
    return max(0.0, min(remaining_sec - 0.8, budget))
```

#### 4. Phase H轮数优化（除L_14_7_7_6外）
```python
# Line 4587-4590
elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
    # N=14 except L_14_7_7_6: simple fast iteration (like n=12)
    rounds = 4
```

#### 5. Phase I时间预算优化（除L_14_7_7_6外）
```python
# Line 4713-4720
elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
    # Other n=14 except L_14_7_7_6: simple fast iteration (like n=12)
    frac = 0.06
    cap = 3.0
    floor = 0.5
    budget = max(floor, min(cap, remaining_sec * frac))
    return max(0.0, min(remaining_sec - 0.8, budget))
```

#### 6. Phase I轮数优化（除L_14_7_7_6外）
```python
# Line 4797-4800
elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
    # N=14 except L_14_7_7_6: simple fast iteration (like n=12)
    rounds = 2
```

#### 7. Phase K时间预算优化（除L_14_7_7_6外）
```python
# Line 4883-4887
elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
    # N=14 except L_14_7_7_6: simple fast iteration (like n=12)
    budget_cap = min(budget_cap, 3.0)
    ratio = min(ratio, 0.06)
```

### N14优化策略总结
- **目标**：最小化主循环，最大化精炼阶段
- **方法**：hard_cap=3 + 快速迭代（类似n=12）
- **例外**：L_14_7_7_6（太困难，使用原始算法）

---

## N17/N18/N19优化验证

### N17优化（已保留）

#### 1. 专用模块导入
```python
# Line 39-53
from n_algorithms.n17.specialized_module import (
    is_n17_special_case,
    run_n17_specialized_module,
    classify_n17_special_case,
    get_n17_case_spec,
    make_n17_case_key,
    should_short_circuit_n17_tiny_legal_solution,
)
```

#### 2. N17初始化
```python
# Line 543-547
self._n17_special_case_key = make_n17_case_key(n, k, j, s)
self._n17_special_case_family = classify_n17_special_case(n, k, j, s)
self._n17_special_case_enabled = is_n17_special_case(n, k, j, s)
n17_spec = get_n17_case_spec(n, k, j, s)
self._n17_special_case_bucket = None if n17_spec is None else n17_spec.bucket
```

#### 3. 跳过密集覆盖表（tiny_baseline_exactish情况）
```python
# Line 621-625
skip_dense_cov_tables = bool(
    self._n17_special_case_enabled
    and self._n17_special_case_bucket == "tiny_baseline_exactish"
    and self.j == self.k == 7
    and self.s <= 4
)
```

#### 4. N17专用模块调度
```python
# Line 1062, 1264-1267
best = self._phase_n17_specialized_module_dispatch(best)

def _phase_n17_specialized_module_dispatch(self, sol: list[int]) -> list[int]:
    if not self._n17_special_case_enabled:
        return sol
    return run_n17_specialized_module(self, sol)
```

#### 5. Tail Refine Reserve时间（N17专用）
```python
# Line 1702-1716
if self._n17_special_case_enabled:
    if self._n17_special_case_bucket == "tiny_baseline_exactish":
        if self.k >= 7:
            return 42.0
        if self.k >= 6:
            return 36.0
        return 30.0
    if self._n17_special_case_bucket == "general_k7_j6_hard":
        return 24.0
    if self._n17_special_case_bucket == "jk_large_delta_dense":
        return 18.0
    if self._n17_special_case_bucket == "containment_fast_bad_dense":
        return 18.0
    if self._n17_special_case_bucket == "general_j5_guidance_weak":
        return 16.0
```

#### 6. Hard Attempt Cap调整（N17专用）
```python
# Line 1298-1306
if (
    self._deadline_at is not None
    and self._n17_special_case_enabled
    and self._n17_special_case_bucket == "tiny_baseline_exactish"
    and self.num_targets <= 2_500
):
    max_cap = 7 if self.k <= 4 else 8
    return max(profile_attempts, min(max_cap, base_attempts + 4))
```

### N18优化（已保留）

#### 1. 专用模块导入
```python
# Line 56-59
from n_algorithms.n18.specialized_module import is_n18_special_case, run_n18_specialized_module
```

#### 2. 种子精炼（小j=k非包含情况）
```python
# Line 863-874
if (
    best is not None
    and self.n == 18
    and is_n18_special_case is not None
    and run_n18_specialized_module is not None
    and is_n18_special_case(self.n, self.k, self.j, self.s)
    and best is not None
    and self.j == self.k
    and not self._containment
    and self.num_targets < 30_000
):
    best = run_n18_specialized_module(self, best)
```

#### 3. Phase E前精炼（k=7, j=6, s≥5情况）
```python
# Line 1023-1032
if (
    self.n == 18
    and is_n18_special_case is not None
    and run_n18_specialized_module is not None
    and is_n18_special_case(self.n, self.k, self.j, self.s)
    and best is not None
    and not self._containment
    and self.k == 7
    and self.j == 6
    and self.s >= 5
):
    best = run_n18_specialized_module(self, best)
```

#### 4. Phase E后精炼（所有n=18特殊情况）
```python
# Line 1038-1043
if (
    self.n == 18
    and is_n18_special_case is not None
    and run_n18_specialized_module is not None
    and is_n18_special_case(self.n, self.k, self.j, self.s)
):
    best = run_n18_specialized_module(self, best)
```

#### 5. Tail Refine Reserve时间（N18专用）
```python
# Line 1717-1733
if self.n == 18 and is_n18_special_case is not None and is_n18_special_case(self.n, self.k, self.j, self.s):
    if self.j == self.k and not self._containment:
        if self.s == self.k - 1 and self.num_targets <= 4_000:
            return 24.0
        if self.s == self.k - 1 and self.num_targets >= 30_000:
            return 26.0
        if self.num_targets >= 18_000:
            return 18.0
        return 12.0
    if (
        not self._containment
        and self.k == 7
        and self.j == 6
        and self.s >= 5
    ):
        return 12.0
    if self._containment:
        return 12.0
```

### N19优化（已保留）

#### 目录结构
```
n_algorithms/n19/
├── __init__.py
├── solver.py                           # 独立求解器（隔离委托）
├── specialized_module.py               # 主专用模块
├── adaptive_strategy.py                # 自适应策略
├── containment_specialized_module.py   # 包含情况专用
├── general_specialized_module.py       # 通用情况专用
└── jk_specialized_module.py            # j=k情况专用
```

#### 特点
- **隔离求解器**：n19使用独立的solver.py（不是wrapper）
- **多专用模块**：针对不同情况有不同的专用模块
- **自适应策略**：根据问题特征选择最佳策略

---

## 模块化架构优势

### 1. 清晰分离
```
n_algorithms/
├── n12/solver.py          # N12专用（wrapper）
├── n13/solver.py          # N13专用（wrapper）
├── n14/solver.py          # N14专用（wrapper）
├── n17/specialized_module.py  # N17专用模块
├── n18/specialized_module.py  # N18专用模块
├── n19/solver.py          # N19独立求解器
└── shared/
    └── solver_core.py     # 核心算法（包含所有优化）
```

### 2. Wrapper模式
```python
# n_algorithms/n12/solver.py
from n_algorithms.shared.core_wrapper import RoutedCoreSolver

class CoveringDesignSolver(RoutedCoreSolver):
    expected_n = 12
```

- **简洁**：每个n值的solver.py只有3-4行代码
- **统一**：所有优化在solver_core.py中统一管理
- **易维护**：修改优化只需改一个文件

### 3. 易于扩展
- 添加新n值优化：创建新目录 + 添加wrapper
- 添加专用模块：在对应目录添加specialized_module.py
- 修改核心算法：只需修改solver_core.py

---

## T-Covering优化（已应用）

### 位置
`n_algorithms/shared/tcovering_solver.py`

### 优化内容

#### 1. 时间安全边界
```python
# Line 42-45
self._time_budget_margin_sec = 0.0
if self._time_budget_sec is not None:
    self._time_budget_margin_sec = 3.0 if n >= 16 else 1.5
```

#### 2. 减少尝试次数
```python
# Line 109-114
effective_attempts = self._num_attempts
if self._is_huge:
    effective_attempts = max(1, self._num_attempts // 2)
elif self._deadline_at:
    effective_attempts = max(2, self._num_attempts // 2)
```

#### 3. 移除SA（模拟退火）
- 原代码中有`_simulated_annealing`方法但未调用
- SA太慢且效果不明显
- 节省大量时间

#### 4. 时间检查点
```python
# Line 119-122
if self._deadline_at and time.time() >= self._deadline_at:
    self._report("timeout", "Time budget exhausted")
    break
```

#### 5. 快速本地搜索
```python
# Line 131
solution = self._local_search(solution)
```

- 早期终止
- 最多3轮
- 增量验证

---

## 测试建议

### 1. 回归测试
```bash
# 完整测试套件
python eval.py --suite smoke
python eval.py --suite core
python eval.py --suite full
```

### 2. N12/N13/N14专项测试
```bash
# 测试n12/n13/n14路由
python test_n15_n16_routing.py

# 测试n13问题情况
python test_n13_problem_cases.py
```

### 3. N17/N18/N19专项测试
```bash
# 测试n17/n18/n19集成
python test_n17_n18_n19_integration.py

# 快速测试n19
python test_n19_quick.py
```

### 4. T-Covering优化测试
```bash
# T-Covering优化测试
python test_tcovering_optimization.py
```

---

## 总结

### ✅ 已验证保留的优化

1. **N12优化**：9个优化点，例外L_12_6_4_3
2. **N13优化**：9个优化点，仅L_13_6_5_5
3. **N14优化**：7个优化点，例外L_14_7_7_6
4. **N17优化**：6个优化点，完整保留
5. **N18优化**：5个优化点，完整保留
6. **N19优化**：独立求解器 + 多专用模块
7. **T-Covering优化**：4个优化点，已应用

### 架构改进

- **模块化**：清晰的目录结构
- **Wrapper模式**：简洁的n值专用求解器
- **统一管理**：所有优化在solver_core.py
- **易于扩展**：添加新优化更简单

### 下一步

1. ✅ 验证完成
2. 🔄 运行测试套件
3. 📊 性能基准测试
4. 📝 更新文档

---

## 文件位置参考

### 核心文件
- `n_algorithms/shared/solver_core.py` - 核心求解器（5931行）
- `n_algorithms/shared/tcovering_solver.py` - T-Covering求解器
- `n_algorithms/shared/core_wrapper.py` - Wrapper基类

### N12/N13/N14
- `n_algorithms/n12/solver.py` - N12 wrapper
- `n_algorithms/n13/solver.py` - N13 wrapper
- `n_algorithms/n14/solver.py` - N14 wrapper

### N17/N18/N19
- `n_algorithms/n17/specialized_module.py` - N17专用模块
- `n_algorithms/n18/specialized_module.py` - N18专用模块
- `n_algorithms/n19/solver.py` - N19独立求解器
- `n_algorithms/n19/specialized_module.py` - N19主专用模块
- `n_algorithms/n19/adaptive_strategy.py` - N19自适应策略
- `n_algorithms/n19/containment_specialized_module.py` - N19包含专用
- `n_algorithms/n19/general_specialized_module.py` - N19通用专用
- `n_algorithms/n19/jk_specialized_module.py` - N19 j=k专用

### 测试文件
- `test_n15_n16_routing.py` - N15/N16路由测试
- `test_n13_problem_cases.py` - N13问题情况测试
- `test_n17_n18_n19_integration.py` - N17/N18/N19集成测试
- `test_n19_quick.py` - N19快速测试
- `test_tcovering_optimization.py` - T-Covering优化测试

---

**验证人员**：Kiro AI Assistant  
**验证日期**：2026-04-30  
**验证结果**：✅ 所有优化已完整保留
