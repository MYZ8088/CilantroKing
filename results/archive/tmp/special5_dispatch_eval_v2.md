# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 21:59:49
- baseline_file: `results/n_le_15_extra5_truefail_baselines_v1.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 5
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 5
- compliant_count: 0
- non_compliant_count: 5
- runtime_fail_count: 0
- quality_fail_count: 5
- verify_fail_count: 5
- status_timeout_count: 0
- status_error_count: 5
- elapsed_total_sec: 1.943876

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 1 | 0 | 1 | 1 | 0 | 1 | None | 0.074173 |
| 14 | 2 | 0 | 2 | 2 | 0 | 2 | None | 0.2885 |
| 15 | 2 | 0 | 2 | 2 | 0 | 2 | None | 0.646352 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
