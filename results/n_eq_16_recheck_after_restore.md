# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-27 15:51:35
- baseline_file: `D:\ai2026.4\CilantroKing\results\coveringrepo_n_lt_26_baselines.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 1
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 29
- compliant_count: 11
- non_compliant_count: 18
- runtime_fail_count: 0
- quality_fail_count: 18
- verify_fail_count: 14
- status_timeout_count: 0
- status_error_count: 14
- elapsed_total_sec: 1412.767053

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 29 | 11 | 18 | 18 | 0 | 14 | 0.05902 | 48.716105 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 180 | 0.184211 | 116.067577 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 155 | 0.174242 | 117.207161 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 59 | 0.134615 | 67.67242 | general_noncontain | quality_over_10pct |
| L_16_6_6_4 | 16 | 6 | 6 | 4 | 25 | 28 | 0.12 | 115.99534 | j_eq_k_noncontain_medium_n | quality_over_10pct |
