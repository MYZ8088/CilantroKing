# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-27 15:32:40
- baseline_file: `D:\ai2026.4\CilantroKing\results\coveringrepo_n_lt_26_baselines.json`
- n_range: [7, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 4
- CK_USE_GPU: 1

## summary

- total_cases: 285
- compliant_count: 235
- non_compliant_count: 50
- runtime_fail_count: 4
- quality_fail_count: 46
- verify_fail_count: 29
- status_timeout_count: 4
- status_error_count: 29
- elapsed_total_sec: 11428.180977

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 7 | 16 | 16 | 0 | 0 | 0 | 0 | 0.0 | 1.345483 |
| 8 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 1.150636 |
| 9 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 2.50874 |
| 10 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 5.942565 |
| 11 | 30 | 30 | 0 | 0 | 0 | 0 | 0.007427 | 8.806816 |
| 12 | 30 | 29 | 1 | 0 | 1 | 0 | 0.003147 | 78.34596 |
| 13 | 30 | 27 | 3 | 2 | 1 | 0 | 0.020641 | 88.138597 |
| 14 | 30 | 22 | 8 | 8 | 0 | 0 | 0.056506 | 93.627441 |
| 15 | 30 | 21 | 9 | 7 | 2 | 0 | 0.061245 | 101.290085 |
| 16 | 29 | 0 | 29 | 29 | 0 | 29 | None | 0.425106 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 128 | 0.28 | 117.304982 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 180 | 0.267606 | 116.02261 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 236 | 0.248677 | 118.305809 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 219 | 0.216667 | 117.44168 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 116.440776 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 72 | 0.180328 | 118.639278 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 960 | 0.175031 | 118.725616 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_4 | 15 | 7 | 5 | 4 | 20 | 23 | 0.15 | 117.709908 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 574 | 0.145709 | 117.551506 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 118.625238 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 117.190519 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.650883 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 117.988646 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 117.377367 | general_noncontain | quality_over_10pct |
| L_14_7_6_5 | 14 | 7 | 6 | 5 | 36 | 40 | 0.111111 | 119.035171 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 153 | 0.108696 | 118.335156 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_4 | 14 | 6 | 5 | 4 | 29 | 32 | 0.103448 | 116.846008 | general_noncontain | quality_over_10pct |
| L_12_5_4_3 | 12 | 5 | 4 | 3 | 12 | 12 | 0.0 | 120.000996 | general_noncontain | timeout_over_120s |
| L_13_5_4_3 | 13 | 5 | 4 | 3 | 16 | 16 | 0.0 | 120.000973 | general_noncontain | timeout_over_120s |
| L_15_6_4_3 | 15 | 6 | 4 | 3 | 14 | 14 | 0.0 | 120.001298 | general_noncontain | timeout_over_120s |
| L_15_7_6_4 | 15 | 7 | 6 | 4 | 9 | 9 | 0.0 | 120.002277 | general_noncontain | timeout_over_120s |
