# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 20:28:47
- baseline_file: `results/n_le_15_extra13_baselines_v1.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 13
- compliant_count: 8
- non_compliant_count: 5
- runtime_fail_count: 2
- quality_fail_count: 4
- verify_fail_count: 0
- status_timeout_count: 2
- status_error_count: 0
- elapsed_total_sec: 1522.968816

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 12 | 2 | 2 | 0 | 0 | 0 | 0 | 0.022728 | 116.676662 |
| 13 | 3 | 2 | 1 | 1 | 0 | 0 | 0.041667 | 116.980853 |
| 14 | 3 | 1 | 2 | 2 | 1 | 0 | 0.07152 | 116.664507 |
| 15 | 5 | 3 | 2 | 1 | 1 | 0 | 0.054684 | 117.735882 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_4 | 15 | 7 | 5 | 4 | 20 | 23 | 0.15 | 116.960636 | general_noncontain | quality_over_10pct |
| L_13_5_5_4 | 13 | 5 | 5 | 4 | 48 | 54 | 0.125 | 116.189023 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_5 | 14 | 7 | 6 | 5 | 36 | 40 | 0.111111 | 113.629628 | general_noncontain | quality_over_10pct |
| L_14_6_5_4 | 14 | 6 | 5 | 4 | 29 | 32 | 0.103448 | 120.000771 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_15_6_4_3 | 15 | 6 | 4 | 3 | 14 | 14 | 0.0 | 120.001955 | general_noncontain | timeout_over_120s |
