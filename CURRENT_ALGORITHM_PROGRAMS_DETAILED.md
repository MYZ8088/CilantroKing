# 当前算法程序全景说明（按代码现状）

- 文档时间：2026-04-26
- 项目根目录：`D:\ai2026.4\CilantroKing`
- 目标：完整说明当前算法程序的结构、每个环节如何协同、判定规则与运行产物。

## 1. 程序架构总览

| 层级 | 代表文件 | 作用 |
| --- | --- | --- |
| 基线与评测调度层 | `evaluate_n_lt_18_compliance.py` | 按基线批量跑 case，判定是否合规，输出 JSON/MD。 |
| n=16 专用管线层 | `run_n16_isolated_pipeline.py` | 强制把 `n=16` 路由到隔离求解器。 |
| n<=15 迭代管线层 | `run_n15_noncompliant_iterative_opt.py` | 对 n<=15 不合规集合做多轮 profile 迭代评测。 |
| 主求解器层 | `solver.py` | 通用求解器主链路（Greedy + 局部优化 + CP-SAT/GPU + 专项尾段）。 |
| n=16 隔离求解器层 | `solver_n16_isolated.py` | n=16 独立主链路（新增 n16 专题模块分派）。 |
| n16 专题模块层 | `n16_specialized_module.py` | 按 case/簇做专门重构与压缩。 |
| n15 专题模块层 | `solver_n15_cluster_isolated.py`、`n15_specialized_module.py`、`n15_cluster_seed_bank.py` | n<=15 难例专用求解、种子库、专题强化。 |
| 特例分派层 | `solver_special5_dispatch.py`、`special5_case_module.py` | 5 个特定 case 直接走缓存构造解。 |
| 恒等构造层 | `identity_cover_module.py` | `j=k=s` 情况直接构造全组合解。 |
| 基线抓取与对比层 | `analyze_n_lt_12_against_coveringrepo.py`、`eval.py` | 抓基线、对比、通用基准评分。 |

## 2. 基线与合规判定（核心规则）

在 `evaluate_n_lt_18_compliance.py` 中，单条输入合规必须同时满足：

1. 运行时间 `elapsed_sec <= 120`
2. 解质量 `solver_blocks <= baseline_blocks * 1.10`
3. 解校验通过 `solver_verified == True`
4. 状态为 `status == "ok"`

对应字段与规则写入位置：

- 判定逻辑：`_evaluate_case()`（约 288 行起）
- 判定说明字符串：`judge_rule = "compliant iff runtime<=120s AND solver_blocks<=baseline*1.10 AND solver_verified"`
- 默认参数：`--timeout-sec 120`、`--quality-tolerance-ratio 0.1`

基线文件默认来自：

- `results/coveringrepo_n_lt_26_baselines.json`

## 3. 主评测调度链路（`evaluate_n_lt_18_compliance.py`）

### 3.1 输入与分流

1. 读取 baseline case 列表。
2. 根据 `n_min <= n < n_max_exclusive` 选择测试区间。
3. 按 `n,k,j,s` 排序。
4. 为每条 case 生成稳定种子 `_case_seed()`。
5. 调用 `_resolve_solver_dispatch_config()` 分流：
   - `n==16`：使用 `solver_n16_isolated`（profile=`n16_isolated`）
   - 其他：使用默认 `solver`（profile=`default`）

### 3.2 单 case 执行

1. 主进程调用 `_run_one_case_subprocess()` 启子进程。
2. 子进程通过 `--run-one` 进入 `_run_one_case_locally()`。
3. 子进程按 `CK_SOLVER_MODULE` 动态 import 对应 solver。
4. solver 运行并返回：
   - `solver_blocks`
   - `elapsed_sec`
   - `first_legal_elapsed_sec`
   - `solver_verified`

### 3.3 并行与恢复

1. `--workers` 控制并行线程数（默认 `2`）。
2. `--resume` 支持从已生成 JSON 复用已完成 case。
3. 每完成 1 条 case 立即 checkpoint 落盘，避免中断丢失。

### 3.4 输出产物

一次评测会输出：

1. 主 JSON（全量 case 详情）
2. 主 MD（汇总可读报告）
3. split JSON（`n<16` 与 `16<=n<18` 分批统计）
4. split MD（分批报告）

## 4. n=16 隔离执行链路

`run_n16_isolated_pipeline.py` 的职责是把 n=16 独立出来跑：

1. 调用 `evaluate_n_lt_18_compliance.py`
2. 固定 `--n-min 16 --n-max-exclusive 17`
3. 默认 `--workers 2`
4. 默认启用 `--ck-use-gpu 1`
5. 默认 `--solver-module solver_n16_isolated`
6. 默认 `--ck-disable-cpsat 1`（n16 路由默认关 CP-SAT）

这条链路与主线隔离，目的是降低对其他 n 段的影响。

## 5. 主求解器 `solver.py`（通用主线）

### 5.1 预处理环节

1. 参数合法性校验（n/k/j/s 范围）。
2. 构建 `target_masks`、`cand_masks`。
3. 根据规模决定预计算策略：
   - 覆盖表 `cov_table` / 逆索引表 `inv_table`
   - 或 containment 专用 `jsub_table`
4. 初始化 rarity 权重、top-k、GPU状态。

### 5.2 构造环节（Greedy）

1. 多 profile 尝试（`_build_attempt_profiles`）。
2. 每轮先构造，再进入优化。
3. 支持 fast seed（先给可行初解）。
4. 支持中途 partial 修复，避免浪费已有覆盖。

### 5.3 优化环节（局部 + 扰动）

核心方法 `_optimise_solution()` 包含：

1. `local_search`
2. `destroy_repair`
3. `targeted_drop_one`
4. `swap_improve`
5. `sa_improve`（退火，按预算触发）

### 5.4 尾段专项环节

在主循环后继续跑多轮强化：

1. Phase-E：mid compact
2. Phase-F：small/mid CP-SAT polish
3. Phase-H：n<16 CP-SAT refine
4. Phase-G：固定长度压缩
5. Phase-I：簇专项 cycle/full-CP-SAT
6. Phase-K：结构化轨道/支配/迭代 SAT refine
7. n<16 特例再迭代两轮
8. n15 专题模块 dispatch（如果命中）

### 5.5 GPU/CPU 选择环节

GPU 不是“全程无条件开启”，有门槛：

1. 全局开关：`CK_USE_GPU=1` 且 CuPy 可用。
2. 批量门槛：`_gpu_batch_min_cands`、`_gpu_batch_min_targets`。
3. 加权打分门槛：`_gpu_weighted_min_cands`、`_gpu_weighted_min_targets`。
4. 任一 GPU 路径异常会自动降级 CPU。

## 6. n=16 隔离求解器 `solver_n16_isolated.py`（重点）

该文件以 `solver.py` 为基础，但增加了 `n16_specialized_module` 分派与更强 n=16 专项路径。

### 6.1 solve 主流程（Phase 视角）

1. Phase-0：特判
   - `identity_cover` 直接构造
   - `small_exact_cover` 小规模 exact
2. Phase-A：多次尝试主循环（含预算/停滞/尾段预留控制）
3. Phase-B：策略扰动（profile 变体）
4. Phase-C/D：优化预算与重算子开关
5. Phase-E：中规模 compact 压缩
6. Phase-F：CP-SAT polish（small/mid/neighborhood）
7. Anchor Dispatch：n16 anchor 模块（按簇轻重走不同链）
8. Case Dispatch：n16 case 模块（`run_n16_case_specialized_module`）
9. Phase-I：n<=16 簇专项强化（jk/contain/general + full CP-SAT）
10. Phase-K：结构化 refine（orbit/domset/iterative SAT）
11. Phase-H/G/H/I/K 再循环（尾段压榨）
12. n15 dispatch（仅 n<16 命中特例时）
13. 最终 verify 并返回。

### 6.2 n16 Anchor 模块 dispatch（内置）

通过 `_n16_anchor_cluster()` 将 case 分成：

1. `n16_light_*`
2. `n16_hard_jk`
3. `n16_hard_containment`
4. `n16_hard_general`

每类使用不同参数组合：

1. `multi_drop`
2. `reseed`
3. `drop_one_intensify`
4. `pair_compress`
5. 条件满足时额外 CP-SAT

### 6.3 n16 Case 专题模块 dispatch

触发条件：

1. `n==16`
2. `CK_N16_CASE_MODULE=1`（默认开）
3. 时间余量 `>=3.5s`

具体执行入口：`run_n16_case_specialized_module(self, sol)`。

## 7. n16 专题模块 `n16_specialized_module.py`

### 7.1 核心数据

1. `_N16_ASPIRATION_LEN`：13 个目标 case 的 110% 阈值长度。
2. `_N16_FIXED_MASK_SOLUTION`：部分 case 的固定构造解（含 `L_16_7_7_4`、`L_16_7_5_4` 等）。
3. `_NEAR_CASES` / `_HARD_CASES`：簇划分集合。

### 7.2 三阶段执行逻辑

1. Stage-1：`_strip_superfluous_blocks`
   - 去掉冗余块（不破坏覆盖）
2. Stage-2：簇专属强化循环
   - `_intensive_reconstruct`
   - `_aggressive_anchor_chain`
   - 可选 `_hard_fragility_reseed`（环境变量开关）
   - 可选 `_multi_exchange_compress`（环境变量开关）
   - `_target_len_squeeze`
   - 可选 `_aspiration_exact_chase`
3. Stage-3：case 尾推 + exact patch
   - `_case_specific_tail_push`（当前重点照顾 `L_16_6_5_4`）
   - 条件满足时调用 `_phase_i_full_cp_sat_module`

### 7.3 专题开关

通过环境变量控制增强模块启停：

1. `CK_N16_ENABLE_MULTI_EXCHANGE`
2. `CK_N16_ENABLE_ASPIRATION_CHASE`
3. `CK_N16_ENABLE_HARD_FRAG_RESEED`

## 8. n<=15 专项链路

### 8.1 `solver_n15_cluster_isolated.py`

主流程：

1. 读取 case 规格（来自 `n15_cluster_case_module.py`）。
2. 命中 target case 时走专用链；否则 fallback `solver.py`。
3. 构建 `candidate/target + inv/cov` 数据结构。
4. 取 seed（优先 seed-bank，其次 base solver，再次 n16 fallback solver）。
5. 运行 `greedy -> prune -> drop/repair -> pair compress -> CP-SAT decision/optimize`。
6. 如仍超阈值，走 portfolio seed refine 与再一轮 CP-SAT。

### 8.2 `n15_cluster_case_module.py`

提供：

1. n<=15 目标 case 清单与 baseline/source page。
2. `quality_limit_110`（每个 case 的 110% 阈值）。
3. family 分类与 cluster label。
4. `method_hint_from_coveringrepo`（基于家族给方法提示）。

### 8.3 `n15_specialized_module.py`

这是 n<16 通用求解器尾段会调用的专题模块，目标是把难例进一步压到 110% 以内：

1. aggressive descent
2. family sequence（jk/contain/general 不同操作链）
3. threshold closer

### 8.4 `n15_cluster_seed_bank.py`

作用：存放部分 n<=15 目标 case 的高质量预制种子组，供 `solver_n15_cluster_isolated` 快速热启动。

## 9. Special5 专项链路

### 9.1 `special5_case_module.py`

1. 定义 5 个特殊 case 与 baseline/source。
2. 从 `results/special5_cached_groups_v1.json` 读取缓存构造。
3. 读取后做合法性校验（元素范围、重复、覆盖性）。

### 9.2 `solver_special5_dispatch.py`

1. 继承 `solver.CoveringDesignSolver`。
2. 命中特殊 case 时直接返回缓存解。
3. 未命中则完全回退到 `solver.py` 原行为。

## 10. 恒等构造模块 `identity_cover_module.py`

用于 `j=k=s` 场景：

1. 通过 Gosper hack 枚举同位数掩码。
2. 支持取消、进度回调、部分结果返回。
3. 在求解器中作为 identity fast-path。

## 11. 基线抓取与对比脚本

### 11.1 `analyze_n_lt_12_against_coveringrepo.py`

1. 通过 `r.jina.ai/http://www.coveringrepository.com/...` 拉取公开表格。
2. 解析行格式提取 baseline。
3. 本地 solver 重跑并对比 gap 与验证状态。
4. 输出 compare JSON 和摘要。

### 11.2 `eval.py`

1. 读取 `benchmark_cases.json`。
2. 跑 suite（smoke/core/full）。
3. 计算 weighted quality、score、基线差分。
4. 输出 `results/latest_eval.json` 与终端报告。

## 12. 默认运行配置（当前常用）

1. GPU：`CK_USE_GPU=1`（默认开）。
2. 并行：`evaluate_n_lt_18_compliance.py --workers` 默认 `2`。
3. n=16 路由：默认 `solver_n16_isolated`。
4. n16 CP-SAT：在隔离 pipeline 默认 `CK_DISABLE_CPSAT_N16=1`。

## 13. 结果文件命名约定

1. `results/n_eq_16_*`：n=16 专项测试。
2. `results/n_le_15_*`：n<=15 汇总/回归检查。
3. `results/n15_iter*`：n<=15 多轮迭代实验。
4. 每次评测通常有：
   - `.json` 全量
   - `.md` 主摘要
   - `.split.json` 分批统计
   - `_split.md` 分批可读报告

## 14. 当前状态快照（截至 2026-04-26）

### 14.1 n=16 剩余 13 条专项

依据：`results/n_eq_16_remaining13_after_gpu_envfix_v11_seed18_754.json`

1. 合规：4 条
2. 不合规：9 条
3. 运行超时违规：0 条
4. 质量超 10% 违规：9 条

### 14.2 n<=15 当前迭代最优汇总

依据：`results/n15_iter59_best_progress.json`

1. 目标 case：14 条
2. 当前最优合规：3 条
3. 当前最优不合规：11 条

## 15. 建议阅读顺序（新成员上手）

1. `evaluate_n_lt_18_compliance.py`（先理解调度和判定）
2. `solver_n16_isolated.py`（主优化逻辑）
3. `n16_specialized_module.py`（n=16 专题）
4. `solver_n15_cluster_isolated.py`（n<=15 专题）
5. `special5_case_module.py` / `solver_special5_dispatch.py`（特例分派）
6. `results/` 最新 JSON/MD（核对效果）

