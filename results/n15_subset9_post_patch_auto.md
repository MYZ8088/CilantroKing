# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 01:22:37
- baseline_file: `results\n15_subset9_baseline.json`
- n_range: [13, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 9
- compliant_count: 0
- non_compliant_count: 9
- runtime_fail_count: 0
- quality_fail_count: 9
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 992.741478

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.196721 | 108.019807 |
| 14 | 3 | 0 | 3 | 3 | 0 | 0 | 0.135526 | 112.62878 |
| 15 | 4 | 0 | 4 | 4 | 0 | 0 | 0.156829 | 109.703881 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 221 | 0.227778 | 105.402085 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 74 | 0.213115 | 103.668933 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 72 | 0.180328 | 112.370681 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 101.836058 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 574 | 0.145709 | 105.235906 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 115.711146 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 115.488635 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 116.088745 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 154 | 0.115942 | 116.939289 | containment_s_eq_j | quality_over_10pct |
