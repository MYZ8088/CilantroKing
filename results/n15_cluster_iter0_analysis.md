# Iter0 输入不合规聚类分析

- 样本数: 14

## 聚类统计

| cluster | count |
| --- | ---: |
| containment_s_eq_j__edge | 2 |
| containment_s_eq_j__medium | 3 |
| containment_s_eq_j__severe | 1 |
| general_noncontain__medium | 2 |
| j_eq_k_noncontain_medium_n__medium | 2 |
| j_eq_k_noncontain_medium_n__severe | 4 |

## 分族策略（借鉴 coveringrepository 公开方法）

- `containment_s_eq_j`: 6 例
  - 方法线索: shrink+block-weight+iterative SAT（借鉴 WSC 手册中的 shrinking / weight / deep search 线索）
- `general_noncontain`: 2 例
  - 方法线索: two-stage local-search + SAT polish（借鉴局部搜索+后处理组合）
- `j_eq_k_noncontain_medium_n`: 6 例
  - 方法线索: orbit+domset+deep-search（借鉴 history 中 local-search / dynamic-programming / iterative SAT 思路）

## 样本明细

| id | params | family | baseline | solver | gap | cluster |
| --- | --- | --- | ---: | ---: | ---: | --- |
| L_13_6_6_5 | L(13,6,6,5) | j_eq_k_noncontain_medium_n | 61 | 74 | 0.213115 | j_eq_k_noncontain_medium_n__severe |
| L_13_7_7_6 | L(13,7,7,6) | j_eq_k_noncontain_medium_n | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n__severe |
| L_14_5_5_4 | L(14,5,5,4) | j_eq_k_noncontain_medium_n | 69 | 81 | 0.173913 | j_eq_k_noncontain_medium_n__medium |
| L_14_6_4_4 | L(14,6,4,4) | containment_s_eq_j | 80 | 91 | 0.1375 | containment_s_eq_j__medium |
| L_14_6_6_5 | L(14,6,6,5) | j_eq_k_noncontain_medium_n | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n__medium |
| L_14_7_5_5 | L(14,7,5,5) | containment_s_eq_j | 138 | 152 | 0.101449 | containment_s_eq_j__edge |
| L_14_7_6_6 | L(14,7,6,6) | containment_s_eq_j | 501 | 560 | 0.117764 | containment_s_eq_j__edge |
| L_15_6_4_4 | L(15,6,4,4) | containment_s_eq_j | 117 | 135 | 0.153846 | containment_s_eq_j__medium |
| L_15_6_5_4 | L(15,6,5,4) | general_noncontain | 40 | 45 | 0.125 | general_noncontain__medium |
| L_15_6_6_5 | L(15,6,6,5) | j_eq_k_noncontain_medium_n | 142 | 180 | 0.267606 | j_eq_k_noncontain_medium_n__severe |
| L_15_7_5_5 | L(15,7,5,5) | containment_s_eq_j | 189 | 240 | 0.269841 | containment_s_eq_j__severe |
| L_15_7_6_5 | L(15,7,6,5) | general_noncontain | 58 | 65 | 0.12069 | general_noncontain__medium |
| L_15_7_6_6 | L(15,7,6,6) | containment_s_eq_j | 817 | 960 | 0.175031 | containment_s_eq_j__medium |
| L_15_7_7_6 | L(15,7,7,6) | j_eq_k_noncontain_medium_n | 180 | 224 | 0.244444 | j_eq_k_noncontain_medium_n__severe |
