# n<=15 不合规簇自动迭代优化报告

- 生成时间: 2026-04-26 02:58:09
- 输入结果: `D:\ai2026.4\CilantroKing\results\n15_iter0_pre_patch_auto.json`

## 迭代结果

| iter | profile | total | compliant | non_compliant | avg_gap_non_compliant | output_json |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | balanced | 14 | 0 | 14 | 0.17925 | `n15_iter1_cluster_solver_balanced.json` |
| 2 | exact_first | 14 | 0 | 14 | 0.185926 | `n15_iter2_cluster_solver_exact_first.json` |
| 3 | repair_first | 14 | 0 | 14 | 0.172657 | `n15_iter3_cluster_solver_repair_first.json` |

## 逐样本最佳（跨迭代取最优）

| id | params | baseline | best_solver | gap | compliant | profile |
| --- | --- | ---: | ---: | ---: | --- | --- |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 73 | 0.196721 | False | default |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 72 | 0.180328 | False | default |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 79 | 0.144928 | False | default |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | False | default |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | False | default |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 152 | 0.101449 | False | default |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 560 | 0.117764 | False | default |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | False | default |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | False | default |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 180 | 0.267606 | False | default |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | False | default |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | False | default |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 946 | 0.157895 | False | default |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 223 | 0.238889 | False | default |
