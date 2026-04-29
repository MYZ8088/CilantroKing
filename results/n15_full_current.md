# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-29 02:33:44
- baseline_file: `C:\Users\York\Desktop\CilantroKing-lbn-opt\coveringrepo_n_lt_26_baselines(1).json`
- n_range: [15, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 30
- compliant_count: 19
- non_compliant_count: 11
- runtime_fail_count: 0
- quality_fail_count: 11
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1321.184879

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 15 | 30 | 19 | 11 | 11 | 0 | 0 | 0.079261 | 44.039496 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 113.222692 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 219 | 0.216667 | 116.750804 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 975 | 0.19339 | 109.797054 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_3 | 15 | 5 | 5 | 3 | 13 | 15 | 0.153846 | 5.357768 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 96.438497 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_3 | 15 | 6 | 5 | 3 | 7 | 8 | 0.142857 | 2.542893 | general_noncontain | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 72.398408 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 75.351196 | general_noncontain | quality_over_10pct |
| L_15_7_4_3 | 15 | 7 | 4 | 3 | 9 | 10 | 0.111111 | 1.304652 | general_noncontain | quality_over_10pct |
| L_15_5_3_3 | 15 | 5 | 3 | 3 | 55 | 61 | 0.109091 | 0.141102 | containment_s_eq_j | quality_over_10pct |
| L_15_7_4_4 | 15 | 7 | 4 | 4 | 57 | 63 | 0.105263 | 0.308125 | containment_s_eq_j | quality_over_10pct |
