# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 09:30:10
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
- verify_fail_count: 4
- status_timeout_count: 0
- status_error_count: 4
- elapsed_total_sec: 506.084045

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 4 | 0 | 4 | 4 | 0 | 0 | 0.206756 | 19.460081 |
| 14 | 7 | 0 | 7 | 7 | 0 | 0 | 0.191385 | 33.255881 |
| 15 | 9 | 0 | 9 | 9 | 0 | 4 | 0.177084 | 21.71695 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 130 | 0.3 | 55.868824 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | 13 | 7 | 5 | 5 | 78 | 101 | 0.294872 | 13.494504 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 100 | 0.25 | 15.256999 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 177 | 0.246479 | 45.908062 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | 15 | 5 | 5 | 4 | 95 | 115 | 0.210526 | 42.800049 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 20.903105 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 594 | 0.185629 | 38.877163 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 20.929227 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 114 | 0.163265 | 38.757606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_5_5 | 13 | 6 | 5 | 5 | 245 | 283 | 0.155102 | 22.513489 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 20.99309 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | 14 | 6 | 5 | 5 | 371 | 427 | 0.150943 | 31.963396 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 46 | 0.15 | 18.989491 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 23.126727 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 158 | 0.144928 | 28.940454 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | 15 | 6 | 5 | 5 | 578 | 650 | 0.124567 | 39.943336 | containment_s_eq_j | quality_over_10pct |
