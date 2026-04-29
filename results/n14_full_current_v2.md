# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-29 00:43:21
- baseline_file: `C:\Users\York\Desktop\CilantroKing-lbn-opt\coveringrepo_n_lt_26_baselines(1).json`
- n_range: [14, 15)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 30
- compliant_count: 29
- non_compliant_count: 1
- runtime_fail_count: 0
- quality_fail_count: 1
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 962.990745

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 14 | 30 | 29 | 1 | 1 | 0 | 0 | 0.030676 | 32.099691 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 78 | 0.130435 | 118.628769 | j_eq_k_noncontain_medium_n | quality_over_10pct |
