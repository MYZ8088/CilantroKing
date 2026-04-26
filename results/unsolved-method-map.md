# 未解决项与参考方法对照（当前快照）

- 生成时间：2026-04-26
- 判定口径：以结果文件中的 `quality_ok == false` 作为“未解决/未达标（相对基线 >10%）”
- 核对数据源：
1. `results/n_le_15_noncompliant15_after_special_v5_w1.json`
2. `results/n_eq_16_remaining13_after_gpu_envfix_v2_cpsat.json`
3. `results/n_lt_16_method_hints.json`
4. `results/n_eq_16_coveringrepo_compare.json`
5. `n15_cluster_case_module.py`（家族级策略提示）

## 1. 现在还有哪些没解决

- `n<=15`：14 / 15 未达标
- `n=16`：10 / 13 未达标
- 合计：24 个未达标案例

## 2. `n<=15` 未解决清单 + 参考方法来源

| ID | family | baseline | solver | gap | source_page | method（提取结果） |
| --- | --- | ---: | ---: | ---: | --- | --- |
| L_13_6_6_5 | j_eq_k_noncontain_medium_n | 61 | 72 | 18.03% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=06&t=05 | Known design |
| L_13_7_7_6 | j_eq_k_noncontain_medium_n | 61 | 71 | 16.39% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=07&t=06 | Known design |
| L_14_5_5_4 | j_eq_k_noncontain_medium_n | 69 | 80 | 15.94% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=05&m=05&t=04 | 未提取到明确方法 |
| L_14_6_4_4 | containment_s_eq_j | 80 | 91 | 13.75% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=04&t=04 | Known design |
| L_14_6_6_5 | j_eq_k_noncontain_medium_n | 98 | 111 | 13.27% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=06&t=05 | Known design |
| L_14_7_5_5 | containment_s_eq_j | 138 | 152 | 10.14% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=05&t=05 | Known design |
| L_14_7_6_6 | containment_s_eq_j | 501 | 560 | 11.78% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=06&t=06 | Known design |
| L_15_6_4_4 | containment_s_eq_j | 117 | 130 | 11.11% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=04&t=04 | Known design |
| L_15_6_5_4 | general_noncontain | 40 | 45 | 12.50% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=05&t=04 | Known design |
| L_15_6_6_5 | j_eq_k_noncontain_medium_n | 142 | 170 | 19.72% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=06&t=05 | 未提取到明确方法 |
| L_15_7_5_5 | containment_s_eq_j | 189 | 240 | 26.98% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=05&t=05 | Known design |
| L_15_7_6_5 | general_noncontain | 58 | 65 | 12.07% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=06&t=05 | Known design |
| L_15_7_6_6 | containment_s_eq_j | 817 | 945 | 15.67% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=06&t=06 | Tabu Search started from a 818-block covering previously created by Mathias Liesener（来源引到 Dan Gordon 仓库） |
| L_15_7_7_6 | j_eq_k_noncontain_medium_n | 180 | 221 | 22.78% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=07&t=06 | Known design |

## 3. `n=16` 未解决清单 + 参考方法来源

| ID | family | baseline | solver | gap | source_page | method（提取结果） | 备注 |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| L_16_5_5_4 | j_eq_k_noncontain_medium_n | 132 | 156 | 18.18% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=05&m=05&t=04 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_6_4_4 | containment_s_eq_j | 152 | 181 | 19.08% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=04&t=04 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_6_5_4 | general_noncontain | 52 | 60 | 15.38% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=05&t=04 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_6_6_5 | j_eq_k_noncontain_medium_n | 223 | 263 | 17.94% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=06&m=06&t=05 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_7_4_4 | containment_s_eq_j | 76 | 89 | 17.11% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=04&t=04 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_7_5_4 | general_noncontain | 28 | 31 | 10.71% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=05&t=04 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_7_5_5 | containment_s_eq_j | 283 | 351 | 24.03% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=05&t=05 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_7_6_5 | general_noncontain | 78 | 99 | 26.92% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=06&t=05 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_7_7_5 | j_eq_k_noncontain_medium_n | 31 | 38 | 22.58% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=07&t=05 | 未提取到明确方法 | solver/independent 均已验证 |
| L_16_7_7_6 | j_eq_k_noncontain_medium_n | 293 | 372 | 26.96% | https://r.jina.ai/http://www.coveringrepository.com/systems.aspx?k=07&m=07&t=06 | 未提取到明确方法 | solver/independent 均已验证 |

## 4. 在哪里找到了哪些参考方法

### 4.1 覆盖库网站页（逐参数）

- 主来源：`coveringrepository.com/systems.aspx`（你现在大多数案例的方法线索都来自这里）
- 现状：多数案例只抽到了 `Known design` 或空白，缺乏可直接复现的构造步骤
- 唯一明确到搜索流程的文本线索：`L_15_7_6_6` 的 Tabu Search 描述

### 4.2 项目内已有“可落地策略”参考

来自 `n15_cluster_case_module.py` 的家族级策略映射（可作为下一轮实现参考）：

| family | 参考策略 |
| --- | --- |
| j_eq_k_noncontain_medium_n | 轨道压缩 + 支配集筛选 + 深度搜索 +（局部搜索/动态规划/迭代 SAT） |
| containment_s_eq_j | 收缩策略 + block-weight 重排 + 迭代 SAT |
| general_noncontain | 两阶段局部搜索 + SAT 抛光 |

### 4.3 你仓库里已经出现过的外部参考站点

| 站点 | 用途 |
| --- | --- |
| https://www.coveringrepository.com/systems.aspx | 每个参数组合的结果、来源页面和部分方法提示 |
| https://ljcr.dmgordon.org/cover/top.html | 历史/索引入口，辅助交叉核对 |
| https://dmgordo.github.io/ | Dan Gordon 仓库站点，个别方法说明会引用 |
| https://www.dmgordon.org/papers/cover.pdf | Covering Designs 综述，用于理解通用构造/搜索范式 |

## 5. 结论（你“现在没法解决”的核心缺口）

1. 还未达标的是 24 个案例（`n<=15` 的 14 个 + `n=16` 的 10 个）。
2. 外部页面对“具体怎么构造”给的信息不足，多数只有结果和“Known design”。
3. 当前最有价值的明确算法线索是 `L_15_7_6_6` 的 Tabu Search；其余更适合按 family 级策略做定向实现与调参。
