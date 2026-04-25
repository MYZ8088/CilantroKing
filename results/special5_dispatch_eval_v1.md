# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 21:58:37
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
- runtime_fail_count: 2
- quality_fail_count: 4
- verify_fail_count: 0
- status_timeout_count: 2
- status_error_count: 0
- elapsed_total_sec: 588.572476

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 1 | 0 | 1 | 1 | 0 | 0 | 0.125 | 115.759238 |
| 14 | 2 | 0 | 2 | 2 | 0 | 0 | 0.107279 | 116.405778 |
| 15 | 2 | 0 | 2 | 1 | 2 | 0 | 0.075 | 120.000841 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_4 | 15 | 7 | 5 | 4 | 20 | 23 | 0.15 | 120.001446 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_13_5_5_4 | 13 | 5 | 5 | 4 | 48 | 54 | 0.125 | 115.759238 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_5 | 14 | 7 | 6 | 5 | 36 | 40 | 0.111111 | 117.000318 | general_noncontain | quality_over_10pct |
| L_14_6_5_4 | 14 | 6 | 5 | 4 | 29 | 32 | 0.103448 | 115.811239 | general_noncontain | quality_over_10pct |
| L_15_6_4_3 | 15 | 6 | 4 | 3 | 14 | 14 | 0.0 | 120.000235 | general_noncontain | timeout_over_120s |
