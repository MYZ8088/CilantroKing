# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-28 13:06:41
- baseline_file: `C:\Users\York\Desktop\CilantroKing-lbn-opt\coveringrepo_n_lt_26_baselines(1).json`
- n_range: [12, 13)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 30
- compliant_count: 27
- non_compliant_count: 3
- runtime_fail_count: 0
- quality_fail_count: 3
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 915.833546

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 12 | 30 | 27 | 3 | 3 | 0 | 0 | 0.016657 | 30.527785 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_12_6_4_3 | 12 | 6 | 4 | 3 | 6 | 7 | 0.166667 | 0.26712 | general_noncontain | quality_over_10pct |
| L_12_7_4_4 | 12 | 7 | 4 | 4 | 24 | 27 | 0.125 | 0.090875 | containment_s_eq_j | quality_over_10pct |
| L_12_7_5_4 | 12 | 7 | 5 | 4 | 8 | 9 | 0.125 | 0.229733 | general_noncontain | quality_over_10pct |
