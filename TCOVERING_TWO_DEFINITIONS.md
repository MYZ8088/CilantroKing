# T-Covering 两种可能的定义

## 背景

在分析 PDF Example 5 和 Example 6 后，发现有两种可能的 t-covering 定义。

## 定义对比

### 理解2：至少 t 个不同的 s-子集被覆盖

**描述：**
- 对于每个 j-子集，至少有 t 个不同的 s-子集被至少一个组覆盖
- 一个 s-子集被多个组覆盖也只算1次

**验证逻辑：**
```python
for each j-subset:
    covered_s_count = 0
    for each s-subset of this j-subset:
        if any group contains this s-subset completely:
            covered_s_count += 1
    if covered_s_count < t:
        return False
return True
```

**Example 6 验证结果（t=4）：**
- ✗ 不满足
- 有2个 j-子集只有3个 s-子集被覆盖
- 例如 {A,B,C,D,F,G}：只有3个 s-子集被覆盖

### 理解3：总覆盖次数 ≥ t

**描述：**
- 对于每个 j-子集，统计其所有 s-子集被所有组覆盖的总次数
- 如果一个 s-子集被多个组覆盖，每次都计数
- 总次数必须 ≥ t

**验证逻辑：**
```python
for each j-subset:
    total_coverage = 0
    for each s-subset of this j-subset:
        for each group:
            if group contains this s-subset completely:
                total_coverage += 1
    if total_coverage < t:
        return False
return True
```

**Example 6 验证结果（t=4）：**
- ✓ 满足
- 所有 j-子集的总覆盖次数都 ≥ 4
- 例如 {A,B,C,D,F,G}：总覆盖次数 = 0+0+0+2+1+1 = 4

## 具体例子对比

### j-子集 {A,B,C,D,F,G} 的分析

**6个 s-子集的覆盖情况：**
1. {A,B,C,D,F}: 被0个组覆盖
2. {A,B,C,D,G}: 被0个组覆盖
3. {A,B,C,F,G}: 被0个组覆盖
4. {A,B,D,F,G}: 被2个组覆盖（Group 4, 5）
5. {A,C,D,F,G}: 被1个组覆盖（Group 6）
6. {B,C,D,F,G}: 被1个组覆盖（Group 9）

**理解2的结果：**
- 被覆盖的 s-子集数量 = 3个（s-子集4, 5, 6）
- t=4 要求 ≥ 4
- 结果：✗ 不满足

**理解3的结果：**
- 总覆盖次数 = 0+0+0+2+1+1 = 4次
- t=4 要求 ≥ 4
- 结果：✓ 满足

## Example 5 (t=1) 验证

### j-子集 {A,D,E,F,G,H} 的分析

**6个 s-子集的覆盖情况：**
1. {A,D,E,F,G}: 被0个组覆盖
2. {A,D,E,F,H}: 被1个组覆盖（Group 3）
3. {A,D,E,G,H}: 被0个组覆盖
4. {A,D,F,G,H}: 被1个组覆盖（Group 2）
5. {A,E,F,G,H}: 被0个组覆盖
6. {D,E,F,G,H}: 被0个组覆盖

**理解2的结果：**
- 被覆盖的 s-子集数量 = 2个
- t=1 要求 ≥ 1
- 结果：✓ 满足

**理解3的结果：**
- 总覆盖次数 = 0+1+0+1+0+0 = 2次
- t=1 要求 ≥ 1
- 结果：✓ 满足

## 关键区别

| 特性 | 理解2 | 理解3 |
|------|-------|-------|
| 计数方式 | 被覆盖的 s-子集个数 | 总覆盖次数 |
| 重复覆盖 | 不计数（只算1次） | 计数（每次都算） |
| Example 6 (t=4) | ✗ 不满足 | ✓ 满足 |
| Example 5 (t=1) | ✓ 满足 | ✓ 满足 |

## 结论

根据 PDF 中 Example 6 是一个正确的例子，**理解3应该是正确的定义**。

**正确的 t-covering 定义：**
> 对于每个 j-子集，其所有 s-子集被所有组覆盖的总次数必须 ≥ t。
> 如果一个 s-子集被多个组覆盖，每次都计数。

## 实现影响

当前 solver.py 实现的是完全不同的定义（每个 j-子集被至少 t 个组覆盖）。

需要修改：
1. `_verify()` 方法：实现理解3的验证逻辑
2. 贪心算法：调整分数计算和目标跟踪
3. 数据结构：预计算每个 j-子集的所有 s-子集

## 验证脚本

- `verify_total_coverage_count.py`: 验证理解3（总覆盖次数）
- `verify_counting_multiplicity.py`: 验证理解2（不同s-子集数量）
- `analyze_abcdfg_detailed.py`: 详细分析 {A,B,C,D,F,G}
