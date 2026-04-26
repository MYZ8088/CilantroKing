# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 09:47:28
- baseline_file: `results/n_lt_16_remaining20_from_v10_baselines.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 20
- compliant_count: 0
- non_compliant_count: 20
- runtime_fail_count: 0
- quality_fail_count: 20
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 790.962103

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 4 | 0 | 4 | 4 | 0 | 0 | 0.206756 | 20.385253 |
| 14 | 7 | 0 | 7 | 7 | 0 | 0 | 0.191385 | 39.352918 |
| 15 | 9 | 0 | 9 | 9 | 0 | 0 | 0.193122 | 48.21674 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 130 | 0.3 | 64.066964 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | 13 | 7 | 5 | 5 | 78 | 101 | 0.294872 | 14.382892 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 241 | 0.275132 | 42.96541 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 100 | 0.25 | 16.586461 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 225 | 0.25 | 59.392963 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 177 | 0.246479 | 70.972705 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | 15 | 5 | 5 | 4 | 95 | 115 | 0.210526 | 51.914801 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 986 | 0.206854 | 54.665327 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 22.176988 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 594 | 0.185629 | 43.272548 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 21.735751 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 114 | 0.163265 | 49.575569 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_5_5 | 13 | 6 | 5 | 5 | 245 | 283 | 0.155102 | 23.245382 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 27.078141 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | 14 | 6 | 5 | 5 | 371 | 427 | 0.150943 | 40.543829 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 46 | 0.15 | 24.869622 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 24.785353 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 158 | 0.144928 | 36.639703 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | 15 | 6 | 5 | 5 | 578 | 650 | 0.124567 | 64.989832 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 37.101862 | general_noncontain | quality_over_10pct |
