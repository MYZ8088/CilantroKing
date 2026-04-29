# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 22:36:30
- baseline_file: `results\tmp_onecase_14_7_5_5_baseline.json`
- n_range: [14, 15)
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
- elapsed_total_sec: 102.721013

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 14 | 1 | 0 | 1 | 1 | 0 | 0 | 0.101449 | 102.721013 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 152 | 0.101449 | 102.721013 | containment_s_eq_j | quality_over_10pct |
