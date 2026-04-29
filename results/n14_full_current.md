# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-28 22:14:03
- baseline_file: `C:\Users\York\Desktop\CilantroKing-lbn-opt\coveringrepo_n_lt_26_baselines(1).json`
- n_range: [14, 15)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 30
- compliant_count: 20
- non_compliant_count: 10
- runtime_fail_count: 0
- quality_fail_count: 10
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1385.781088

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 14 | 30 | 20 | 10 | 10 | 0 | 0 | 0.075081 | 46.192703 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_4_3 | 14 | 7 | 4 | 3 | 6 | 8 | 0.333333 | 3.900746 | general_noncontain | quality_over_10pct |
| L_14_5_5_3 | 14 | 5 | 5 | 3 | 10 | 12 | 0.2 | 20.823578 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_3 | 14 | 6 | 4 | 3 | 11 | 13 | 0.181818 | 3.92768 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 588 | 0.173653 | 104.065104 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 118.678702 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_4 | 14 | 6 | 6 | 4 | 14 | 16 | 0.142857 | 31.801967 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 105.23464 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_4 | 14 | 7 | 6 | 4 | 7 | 8 | 0.142857 | 1.633519 | general_noncontain | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 82.283484 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 154 | 0.115942 | 101.768693 | containment_s_eq_j | quality_over_10pct |
