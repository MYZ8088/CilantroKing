# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 10:42:48
- baseline_file: `D:\ai2026.4\CilantroKing\results\tmp_onecase_16_6_5_4.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
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
- elapsed_total_sec: 13.632235

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 1 | 0 | 1 | 1 | 0 | 0 | 0.153846 | 13.632235 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 60 | 0.153846 | 13.632235 | general_noncontain | quality_over_10pct |
