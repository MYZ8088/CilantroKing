# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 11:11:31
- baseline_file: `results/n_lt_16_remaining20_from_v10_baselines.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 20
- compliant_count: 2
- non_compliant_count: 18
- runtime_fail_count: 1
- quality_fail_count: 18
- verify_fail_count: 0
- status_timeout_count: 1
- status_error_count: 0
- elapsed_total_sec: 2373.689405

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 4 | 1 | 3 | 3 | 0 | 0 | 0.114637 | 118.700772 |
| 14 | 7 | 1 | 6 | 6 | 0 | 0 | 0.173729 | 118.883786 |
| 15 | 9 | 0 | 9 | 9 | 1 | 0 | 0.197666 | 118.522202 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 134 | 0.34 | 118.648239 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 181 | 0.274648 | 119.386173 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 120.001761 | containment_s_eq_j | timeout_over_120s;quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 227 | 0.261111 | 119.225486 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 1005 | 0.23011 | 117.37994 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | 15 | 5 | 5 | 4 | 95 | 115 | 0.210526 | 118.944852 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 117 | 0.193878 | 119.325418 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 72 | 0.180328 | 119.365271 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 162 | 0.173913 | 118.180442 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 588 | 0.173653 | 118.262904 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 71 | 0.163934 | 119.337861 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 80 | 0.15942 | 119.34714 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 118.514473 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.992841 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | 15 | 6 | 5 | 5 | 578 | 655 | 0.133218 | 118.457949 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 116.909901 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 117.879281 | general_noncontain | quality_over_10pct |
| L_13_6_5_5 | 13 | 6 | 5 | 5 | 245 | 273 | 0.114286 | 118.112749 | containment_s_eq_j | quality_over_10pct |
