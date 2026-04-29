# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 20:36:15
- baseline_file: `results/n_le_15_extra5_truefail_baselines_v1.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 5
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 5
- compliant_count: 2
- non_compliant_count: 3
- runtime_fail_count: 1
- quality_fail_count: 3
- verify_fail_count: 0
- status_timeout_count: 1
- status_error_count: 0
- elapsed_total_sec: 584.021947

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 1 | 1 | 0 | 0 | 0 | 0 | 0.083333 | 112.913838 |
| 14 | 2 | 0 | 2 | 2 | 1 | 0 | 0.107279 | 118.346415 |
| 15 | 2 | 1 | 1 | 1 | 0 | 0 | 0.075 | 117.20764 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_4 | 15 | 7 | 5 | 4 | 20 | 23 | 0.15 | 117.283974 | general_noncontain | quality_over_10pct |
| L_14_7_6_5 | 14 | 7 | 6 | 5 | 36 | 40 | 0.111111 | 116.690659 | general_noncontain | quality_over_10pct |
| L_14_6_5_4 | 14 | 6 | 5 | 4 | 29 | 32 | 0.103448 | 120.00217 | general_noncontain | timeout_over_120s;quality_over_10pct |
