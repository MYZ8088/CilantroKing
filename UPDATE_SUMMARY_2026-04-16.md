# 本次更新说明

更新时间：2026-04-16 12:15:18 +0800

提交分支：`yb`

提交哈希：`61e2d13`

提交说明：`重构求解器主流程并同步界面与数据层优化`

## 1. 本次更新概览

本次更新主要完成了三类工作：

1. 对求解器主流程进行了内部重构，优化整体实现逻辑。
2. 在不丢失原有功能的前提下，补充了界面层和数据层的可用性优化。
3. 同步落地了一部分能够提升解质量的算法优化改动。

本次更新后，项目的外部使用方式保持不变：

- GUI 启动入口仍为 [`main.py`](/D:/class/ai/666/CilantroKing_pr1_restore/main.py)
- 求解器核心入口仍为 [`solver.py`](/D:/class/ai/666/CilantroKing_pr1_restore/solver.py)
- 数据库存储接口仍由 [`database.py`](/D:/class/ai/666/CilantroKing_pr1_restore/database.py) 提供

## 2. 变更文件

本次提交涉及以下文件：

- [`solver.py`](/D:/class/ai/666/CilantroKing_pr1_restore/solver.py)
- [`app_clean.py`](/D:/class/ai/666/CilantroKing_pr1_restore/app_clean.py)
- [`database.py`](/D:/class/ai/666/CilantroKing_pr1_restore/database.py)
- [`tests/test_app_database.py`](/D:/class/ai/666/CilantroKing_pr1_restore/tests/test_app_database.py)
- [`results/latest_eval.json`](/D:/class/ai/666/CilantroKing_pr1_restore/results/latest_eval.json)

## 3. 求解器重构内容

### 3.1 主流程重构

对 [`solver.py`](/D:/class/ai/666/CilantroKing_pr1_restore/solver.py) 的内部结构进行了分层整理，重点是把原来比较集中的求解过程拆成更清晰的几部分：

- 策略调度
- 贪心构造
- 局部优化
- repair 修复
- 最终验证

新增了 `GreedyStrategy` 数据类，用于描述不同 attempt 的求解策略，使得求解流程从“单一路径 + 轻随机化”升级为“多策略调度”。

### 3.2 多策略 attempt 机制

现在不同 attempt 不再只是简单换一个随机扰动，而是可以采用不同的构造偏好，例如：

- 覆盖优先
- 稀缺目标加权
- repair 导向
- 更强探索型 top-k 策略

这使得求解器更容易探索不同结构的解，降低了陷入单一路径局部最优的概率。

### 3.3 支持从部分解继续构造

重构后的 greedy 流程支持基于 partial solution 继续求解。这个改动主要服务于两类场景：

- 中途 repair 修复
- destroy-repair 类型的局部重构

这让已有解可以被“拆一部分再修回来”，而不是只能从零开始重跑。

## 4. 算法优化内容

### 4.1 稀缺目标加权评分

在构造阶段新增了 target 稀缺度权重。核心思想是：

- 越难覆盖的 target，权重越高
- 候选组不只按“新增覆盖数”评分，还会考虑“覆盖了多少高价值 target”

这项改动已经在中等规模 non-containment case 上带来了实际收益。

### 4.2 destroy-repair 局部重构

新增了 destroy-repair 机制：

1. 先从当前解中删除一小批边际贡献较低的组
2. 再用新的 greedy / repair 流程把缺口补回来
3. 如果得到更小的合法解，则接受这个新解

这让后处理不再局限于“删冗余”或“单点替换”，开始具备结构性压缩能力。

### 4.3 大实例策略回稳

在超大规模 heuristic case 上，保留了更稳的 `coverage-topk` 作为默认首策略，避免激进加权直接导致质量回退。

也就是说，本次优化不是盲目增强启发式，而是在“提升质量”和“避免大例子退化”之间做了平衡。

## 5. 界面层优化内容

[`app_clean.py`](/D:/class/ai/666/CilantroKing_pr1_restore/app_clean.py) 本次更新的重点是验证流程的可用性优化。

### 5.1 验证改为后台执行

`Verify` 相关逻辑不再阻塞主线程，而是改为后台线程执行，并通过消息队列把结果回传到主界面。

这样可以避免：

- 点击验证后界面卡顿
- 用户误以为按钮无响应

### 5.2 状态管理更明确

新增了验证中的状态控制逻辑，在验证期间会合理禁用部分按钮，验证完成后再统一恢复可交互状态。

### 5.3 验证结果展示更完整

验证成功或失败后，界面会更明确地刷新：

- 当前结果状态
- 对应文件名
- 结果文本展示区域

## 6. 数据层优化内容

[`database.py`](/D:/class/ai/666/CilantroKing_pr1_restore/database.py) 本次主要做了轻量查询优化。

### 6.1 新增摘要查询

新增 `SavedResultSummary` 和 `list_summaries()`，用于列表页只读取必要字段，避免无意义地反序列化全部结果内容。

### 6.2 新增参数计数查询

新增 `count_by_params()`，用于按参数统计历史运行次数，替代原先更重的全量读取方式。

### 6.3 补充索引

新增数据库索引：

- 参数维度索引
- 时间排序索引

这对历史数据变多后的界面响应会更友好。

## 7. 新增测试

新增测试文件 [`tests/test_app_database.py`](/D:/class/ai/666/CilantroKing_pr1_restore/tests/test_app_database.py)，覆盖了以下内容：

- 数据库摘要查询
- 参数计数查询
- `_build_verified_result()` 的结果结构保持

## 8. 验证结果

### 8.1 功能验证

已执行：

- `python -m py_compile solver.py eval.py identity_cover_module.py main.py`
- `python tests/test_solver.py`
- 内联脚本复现 `tests/test_app_database.py` 关键断言

结果：

- `tests/test_solver.py`：`10/10` 通过
- 数据层 / GUI 辅助逻辑：通过

说明：

- 当前本地环境缺少 `pytest`
- 因此数据库与 GUI 辅助测试通过等价脚本完成补偿验证

### 8.2 Benchmark 验证

已执行：

- `python eval.py --suite smoke`
- `python eval.py --suite core`
- `python eval.py --suite full`

关键结果如下。

#### smoke

- `verified=4/4`

#### core

- `verified=10/10`
- `weighted_quality=0.825199`
- `weighted_ratio_verified_only=1.314359`
- 相比 baseline，无质量回退
- `nc_12654` 从 `15` 组优化到 `14` 组

#### full

- `verified=13/13`
- `weighted_quality=0.715122`
- `weighted_ratio_verified_only=1.682300`
- `delta_weighted_quality=+0.003214`
- `delta_total_elapsed_sec=-14.327852`
- `quality_regressed_case_ids=[]`

## 9. 实际收益

本次更新带来的直接收益主要有：

1. 求解器内部结构更清晰，后续继续做专题专解或进一步重构会更容易。
2. 中等规模 non-containment 问题已经出现实际质量提升。
3. `full` 基准没有质量回退，且整体运行时间更快。
4. GUI 验证体验更平滑，数据库查询在数据量上升后会更稳。

## 10. 云端同步信息

本次更新已经同步到远端：

- 远端：`origin`
- 分支：`yb`
- 远端提交：`61e2d13`

## 11. 后续建议

下一步最值得继续推进的方向有两个：

1. 针对 `ljcr_12655` 做 containment 专题优化。
2. 针对 `nc_15664` 继续增强 non-containment 的结构感知构造策略。

如果后续继续迭代，建议继续沿着“通用重构 + 专题专解”两条线推进，而不是只在单一超参上反复微调。
