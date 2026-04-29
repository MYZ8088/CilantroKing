# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 02:01:51
- baseline_file: `results/n_lt_16_remaining24_batch3_baselines.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 24
- compliant_count: 2
- non_compliant_count: 22
- runtime_fail_count: 0
- quality_fail_count: 22
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 677.629515

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 5 | 1 | 4 | 4 | 0 | 0 | 0.188016 | 17.630989 |
| 14 | 9 | 1 | 8 | 8 | 0 | 0 | 0.174523 | 30.447699 |
| 15 | 10 | 0 | 10 | 10 | 0 | 0 | 0.190115 | 31.544528 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_13_7_5_5 | 13 | 7 | 5 | 5 | 78 | 103 | 0.320513 | 8.117981 | containment_s_eq_j | quality_over_10pct |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 130 | 0.3 | 53.560095 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 102 | 0.275 | 10.248504 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 239 | 0.26455 | 23.136055 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 225 | 0.25 | 28.897436 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 177 | 0.246479 | 48.506592 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 997 | 0.220318 | 36.680809 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | 15 | 5 | 5 | 4 | 95 | 115 | 0.210526 | 43.136342 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 26.135104 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 25.177082 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 588 | 0.173653 | 36.704885 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 137 | 0.17094 | 8.342394 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | 14 | 6 | 5 | 5 | 371 | 433 | 0.167116 | 20.226795 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 114 | 0.163265 | 48.447055 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 80 | 0.15942 | 30.554384 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_5_5 | 13 | 6 | 5 | 5 | 245 | 284 | 0.159184 | 13.705133 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 159 | 0.152174 | 21.568798 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 46 | 0.15 | 24.84008 | general_noncontain | quality_over_10pct |
| L_15_7_5_4 | 15 | 7 | 5 | 4 | 20 | 23 | 0.15 | 39.492627 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 30.718657 | general_noncontain | quality_over_10pct |
| L_15_6_5_5 | 15 | 6 | 5 | 5 | 578 | 646 | 0.117647 | 31.694289 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_5 | 14 | 7 | 6 | 5 | 36 | 40 | 0.111111 | 24.860138 | general_noncontain | quality_over_10pct |
