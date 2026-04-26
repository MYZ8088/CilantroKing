# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 00:22:05
- baseline_file: `results\tmp_onecase_13_6_6_5_baseline.json`
- n_range: [13, 14)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 1
- compliant_count: 0
- non_compliant_count: 1
- runtime_fail_count: 0
- quality_fail_count: 1
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 100.665283

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 1 | 0 | 1 | 1 | 0 | 0 | 0.196721 | 100.665283 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 73 | 0.196721 | 100.665283 | j_eq_k_noncontain_medium_n | quality_over_10pct |
