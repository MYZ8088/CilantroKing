# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 00:22:03
- baseline_file: `results\tmp_onecase_15_6_4_4_baseline.json`
- n_range: [15, 16)
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
- elapsed_total_sec: 99.409714

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 15 | 1 | 0 | 1 | 1 | 0 | 0 | 0.153846 | 99.409714 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 99.409714 | containment_s_eq_j | quality_over_10pct |
