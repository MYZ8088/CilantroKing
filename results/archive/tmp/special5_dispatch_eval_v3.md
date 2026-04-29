# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 22:00:30
- baseline_file: `results/n_le_15_extra5_truefail_baselines_v1.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 5
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 5
- compliant_count: 5
- non_compliant_count: 0
- runtime_fail_count: 0
- quality_fail_count: 0
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1.97172

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 1 | 1 | 0 | 0 | 0 | 0 | 0.041667 | 0.065252 |
| 14 | 2 | 2 | 0 | 0 | 0 | 0 | 0.062261 | 0.299913 |
| 15 | 2 | 2 | 0 | 0 | 0 | 0 | 0.085714 | 0.653321 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
