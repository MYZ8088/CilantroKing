# N17/N18/N19集成对比：YB分支 vs 当前实现

## 对比日期
2026-04-29

## YB分支的实现

### N17模块
- **文件**: `n17_specialized_module.py`
- **调用位置**: 1个
  ```python
  best = self._phase_k_cluster_structural_refine(best)
  best = self._phase_n17_specialized_module_dispatch(best)
  ```
- **调用时机**: 所有结构化refinement phases之后
- **硬编码**: ❌ **有2个硬编码解决方案**
  - L(17,7,6,3) - 4个blocks
  - L(17,5,3,3) - 68个blocks

### N18模块
- **文件**: `n18_specialized_module.py`
- **调用位置**: 3个
  1. **Seed后**:
     ```python
     if (self.n == 18 and is_n18_special_case(...) 
         and self.j == self.k and not self._containment 
         and self.num_targets < 30_000):
         best = self._phase_n18_specialized_module_dispatch(best)
     ```
  2. **Phase E前** (k=7, j=6, s>=5):
     ```python
     if (self.n == 18 and is_n18_special_case(...) 
         and not self._containment and self.k == 7 
         and self.j == 6 and self.s >= 5):
         best = self._phase_n18_specialized_module_dispatch(best)
     ```
  3. **Phase E后**:
     ```python
     best = self._phase_e_mid_compact_search(best)
     best = self._phase_n18_specialized_module_dispatch(best)
     ```
- **硬编码**: ✅ 无硬编码，纯算法优化

### N19模块
- **文件**: `solver_n19_isolated.py`（继承主solver）
- **调用位置**: ❌ **没有集成到主solver**
- **使用方式**: 只能通过独立的`run_n19_isolated_pipeline.py`使用
- **问题**: 继承主solver会导致循环导入，无法集成
- **硬编码**: ✅ 无硬编码，纯算法优化

---

## 当前实现（LBN分支合并后）

### N17模块
- **文件**: `n17_specialized_module.py`
- **调用位置**: 1个（与YB相同）
  ```python
  best = self._phase_k_cluster_structural_refine(best)
  # N17 optimization: refine after all structural phases
  if (self.n == 17 and is_n17_special_case is not None 
      and run_n17_specialized_module is not None 
      and is_n17_special_case(self.n, self.k, self.j, self.s)):
      best = run_n17_specialized_module(self, best)
  ```
- **改进**: ✅ **删除了所有硬编码**
  - L(17,7,6,3) → 使用`_run_general_k7_j6_hard`算法
  - L(17,5,3,3) → 使用`_run_containment_fast_bad_dense`算法

### N18模块
- **文件**: `n18_specialized_module.py`
- **调用位置**: 3个（与YB完全相同）
  1. **Seed后** - ✅ 相同条件
  2. **Phase E前** - ✅ 相同条件
  3. **Phase E后** - ✅ 相同位置
- **实现**: ✅ 与YB完全一致

### N19模块
- **文件**: `n19_specialized_module.py`（**新创建，不继承solver**）
- **调用位置**: 1个（**新增，YB没有**）
  ```python
  # N19 optimization: refine after all structural phases
  if (self.n == 19 and is_n19_special_case is not None 
      and run_n19_specialized_module is not None 
      and is_n19_special_case(self.n, self.k, self.j, self.s)):
      best = run_n19_specialized_module(self, best)
  ```
- **改进**: ✅ **成功集成到主solver**
  - 创建了不继承solver的specialized module
  - 避免了循环导入问题
  - 用户输入n=19时会自动使用优化算法

---

## 关键改进总结

### 相对于YB分支的改进

1. **N17硬编码删除** ✅
   - YB有2个硬编码解决方案（偷看答案）
   - 当前实现：全部删除，使用算法求解

2. **N19成功集成** ✅
   - YB无法集成（循环导入问题）
   - 当前实现：创建specialized module，成功集成

3. **保留LBN优化** ✅
   - N12/N13/N14的aggressive early stopping
   - 与YB的n17/n18/n19优化共存

### 架构对比

| 模块 | YB分支 | 当前实现 | 改进 |
|------|--------|----------|------|
| N17 | ✅ 集成 | ✅ 集成 | 删除硬编码 |
| N18 | ✅ 集成 | ✅ 集成 | 完全一致 |
| N19 | ❌ 未集成 | ✅ 集成 | 新增集成 |

### 调用位置对比

| 位置 | YB分支 | 当前实现 |
|------|--------|----------|
| Seed后 | N18 | N18 ✅ |
| Phase E前 | N18 | N18 ✅ |
| Phase E后 | N18 | N18 ✅ |
| Phase K后 | N17 | N17 + N19 ✅ |

---

## 验证要点

### ✅ 已完成
1. N17/N18/N19模块可正常导入
2. N17删除了所有硬编码
3. N18调用位置与YB完全一致
4. N19成功创建specialized module并集成

### 🔍 需要测试
1. 运行`python eval.py --suite core`验证性能
2. 测试L(17,7,6,3)和L(17,5,3,3)的算法求解效果
3. 测试n=19 case是否正确使用优化算法
4. 确认所有case都是算法求解，无硬编码

---

## 结论

**当前实现优于YB分支：**
1. ✅ N17删除了硬编码（更纯粹的算法求解）
2. ✅ N18完全一致（保留YB优化）
3. ✅ N19成功集成（YB未能做到）
4. ✅ 保留LBN的n12/n13/n14优化

**当前实现是YB和LBN的最佳合并版本。**
