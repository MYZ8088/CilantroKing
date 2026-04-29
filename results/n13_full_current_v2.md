# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-28 21:19:30
- baseline_file: `C:\Users\York\Desktop\CilantroKing-lbn-opt\coveringrepo_n_lt_26_baselines(1).json`
- n_range: [13, 14)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 30
- compliant_count: 28
- non_compliant_count: 2
- runtime_fail_count: 0
- quality_fail_count: 2
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 598.295935

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 30 | 28 | 2 | 2 | 0 | 0 | 0.026081 | 19.943198 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_6_4 | 13 | 6 | 6 | 4 | 10 | 12 | 0.2 | 12.63093 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_5 | 13 | 7 | 7 | 5 | 10 | 12 | 0.2 | 12.268682 | j_eq_k_noncontain_medium_n | quality_over_10pct |
