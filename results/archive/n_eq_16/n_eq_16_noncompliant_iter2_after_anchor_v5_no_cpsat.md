# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 10:39:00
- baseline_file: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_baselines.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 18
- compliant_count: 2
- non_compliant_count: 16
- runtime_fail_count: 0
- quality_fail_count: 16
- verify_fail_count: 11
- status_timeout_count: 0
- status_error_count: 11
- elapsed_total_sec: 301.421988

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 18 | 2 | 16 | 16 | 0 | 11 | 0.113004 | 16.745666 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_5_4_3 | 16 | 5 | 4 | 3 | 31 | 37 | 0.193548 | 4.244164 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 181 | 0.190789 | 44.175246 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 155 | 0.174242 | 57.848038 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | 16 | 5 | 3 | 3 | 65 | 73 | 0.123077 | 0.494972 | containment_s_eq_j | quality_over_10pct |
| L_16_4_4_3 | 16 | 4 | 4 | 3 | 64 | 71 | 0.109375 | 21.266755 | j_eq_k_noncontain_medium_n | quality_over_10pct |
