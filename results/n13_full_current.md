# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-28 20:15:23
- baseline_file: `C:\Users\York\Desktop\CilantroKing-lbn-opt\coveringrepo_n_lt_26_baselines(1).json`
- n_range: [13, 14)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 30
- compliant_count: 23
- non_compliant_count: 7
- runtime_fail_count: 0
- quality_fail_count: 7
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 750.882905

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 30 | 23 | 7 | 7 | 0 | 0 | 0.042089 | 25.02943 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_3_3 | 13 | 6 | 3 | 3 | 21 | 24 | 0.142857 | 0.133393 | containment_s_eq_j | quality_over_10pct |
| L_13_6_5_4 | 13 | 6 | 5 | 4 | 21 | 24 | 0.142857 | 88.977411 | general_noncontain | quality_over_10pct |
| L_13_5_4_3 | 13 | 5 | 4 | 3 | 16 | 18 | 0.125 | 0.439481 | general_noncontain | quality_over_10pct |
| L_13_5_5_3 | 13 | 5 | 5 | 3 | 8 | 9 | 0.125 | 0.390013 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_4_3 | 13 | 6 | 4 | 3 | 9 | 10 | 0.111111 | 0.367657 | general_noncontain | quality_over_10pct |
| L_13_6_4_4 | 13 | 6 | 4 | 4 | 66 | 73 | 0.106061 | 65.626409 | containment_s_eq_j | quality_over_10pct |
| L_13_4_3_3 | 13 | 4 | 3 | 3 | 78 | 86 | 0.102564 | 0.445961 | containment_s_eq_j | quality_over_10pct |
