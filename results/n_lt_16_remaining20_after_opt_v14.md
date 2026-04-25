# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 09:55:25
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
- elapsed_total_sec: 803.604883

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 4 | 0 | 4 | 4 | 0 | 0 | 0.206756 | 28.004304 |
| 14 | 7 | 0 | 7 | 7 | 0 | 0 | 0.191385 | 44.874814 |
| 15 | 9 | 0 | 9 | 9 | 0 | 0 | 0.193122 | 41.940441 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 130 | 0.3 | 62.471401 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | 13 | 7 | 5 | 5 | 78 | 101 | 0.294872 | 20.411177 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 241 | 0.275132 | 35.263578 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 100 | 0.25 | 23.792529 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 225 | 0.25 | 44.95165 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 177 | 0.246479 | 59.024986 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | 15 | 5 | 5 | 4 | 95 | 115 | 0.210526 | 54.050354 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 986 | 0.206854 | 42.395909 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 29.808803 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 594 | 0.185629 | 45.02653 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 29.927979 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 114 | 0.163265 | 60.210385 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_5_5 | 13 | 6 | 5 | 5 | 245 | 283 | 0.155102 | 31.869256 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 29.965417 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | 14 | 6 | 5 | 5 | 371 | 427 | 0.150943 | 50.661712 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 46 | 0.15 | 28.571333 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 33.322737 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 158 | 0.144928 | 38.638403 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | 15 | 6 | 5 | 5 | 578 | 650 | 0.124567 | 53.011716 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 30.229028 | general_noncontain | quality_over_10pct |
