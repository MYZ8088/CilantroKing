# n<16 不合规案例锚定分析（120s，>10%）

生成时间：2026-04-24

## 1) 聚类结论（先分群）

- 总案例：256
- `>10%` 且劣于基线（主攻）：67
- `<=10%` 但仍有误差（次攻）：23

主攻 67 组按 family 分布：

- `containment_s_eq_j`：28
- `j_eq_k_noncontain_medium_n`：21
- `general_noncontain`：18

次攻 23 组按 family 分布：

- `containment_s_eq_j`：16
- `j_eq_k_noncontain_medium_n`：5
- `general_noncontain`：2

## 2) 根因锚定（代码门槛证据）

### A. “未用满预算”的主要根因不是算不动，而是阶段进不去

- 主攻 67 组中，`51` 组在 `20s` 内结束，平均仅 `12.99s`。
- 说明多数不是 120s 算不完，而是中后期优化模块触发条件过严。

### B. 67 组中有 55 组被 CP-SAT 小规模精修门槛挡住

- `solver.py` 的 small polish 约束是 `num_cands<=1400 && num_targets<=2000`。
- 67 组里有 55 组不满足，直接跳过该阶段。

### C. `j=k,s<j` 专题曾被 “mid 阶段判定阈值”整体排除

- 旧逻辑 `mid_j=k` 要求 `num_targets>=8000`。
- 但 n<16 下该簇最大 `C(15,7)=6435`，导致整簇几乎进不到对应中后期分支。
- 本轮已修正：`_is_mid_j_equals_k_noncontainment()` 放宽到 `num_targets>=400`。

相关代码位置：

- [solver.py](D:/class/ai/666/CilantroKing_pr1_restore/solver.py#L1162)
- [solver.py](D:/class/ai/666/CilantroKing_pr1_restore/solver.py#L2380)
- [solver.py](D:/class/ai/666/CilantroKing_pr1_restore/solver.py#L2472)
- [solver.py](D:/class/ai/666/CilantroKing_pr1_restore/solver.py#L2314)

## 3) 网站公开信息调研（用于算法思路，不做答案接入）

针对有误差的 90 组（67 主攻 + 23 次攻）提取 `Method/Notes` 后：

- 主攻 67 组中，`59` 组是 `Download FREE`，`8` 组是订阅下载（非公开块内容）。
- 公开方法关键词出现：
  - `hill-climb on cyclic orbits`
  - `hill-climb on affine orbits`
  - `simulated annealing`
  - `tabu search`
  - `random greedy covering`

可见网站给出的思路与“固定组数下的局部搜索/元启发式”一致，适合我们走专题算法实现。

参考来源：

- [Covering Repository](https://www.coveringrepository.com/systems.aspx)
- [LJCR Methods Overview](https://ljcr.dmgordon.org/cover/top.html)

## 4) 本轮已落地优化（算法，不抄答案）

### 改动 1：`j=k` 专题纳入 mid 流程

- 放宽 mid 判定阈值，使 n<16 的 `j=k,s<j` 进入相应中后期模块。

### 改动 2：新增 `n<16` 固定组数可行性搜索（Phase-G）

- 新增 `_phase_g_nlt16_fixed_size_polish()`：
  - 从当前解尝试压到 `len-1`；
  - 在固定长度内执行 swap/repair（删除低关键块 + 针对未覆盖目标补块）；
  - 成功全覆盖则接受并继续压缩。
- 这是“专题专解”里的第一块，对应网站公开方法的 hill-climb/tabu 思路。

相关代码位置：

- [solver.py](D:/class/ai/666/CilantroKing_pr1_restore/solver.py#L793)
- [solver.py](D:/class/ai/666/CilantroKing_pr1_restore/solver.py#L2694)
- [solver.py](D:/class/ai/666/CilantroKing_pr1_restore/solver.py#L2725)

## 5) 代表案例效果（旧版 -> 本轮）

- `L_14_7_7_6`：`146 -> 134`（基线 100）
- `L_15_6_6_5`：`190 -> 179`（基线 142）
- `L_13_7_7_6`：`81 -> 74`（基线 61）
- `L_13_5_5_4`：`58 -> 52`（基线 48）
- `L_14_5_5_4`：`87 -> 80`（基线 69）
- `L_15_7_7_5`：`29 -> 27`（基线 24）
- `L_13_6_5_4`：`26 -> 24`（基线 21）
- `L_15_6_5_4`：`50 -> 47`（基线 40）

## 6) 顺带收益（<=10% 误差）

本轮主改围绕主攻簇，但固定组数搜索会自然覆盖部分 near-miss 输入，尤其是：

- `containment_s_eq_j` 的中等规模实例
- `j=k,s<j` 的小偏差实例

下一轮建议直接跑：

- `n<16` 全量复评，拿新的不合规清单；
- 按“剩余 8 组订阅锁 + 大 gap 样本”继续做专题 2（containment 评分强化）和专题 3（general_noncontain 按 `j-s` 分层）。
