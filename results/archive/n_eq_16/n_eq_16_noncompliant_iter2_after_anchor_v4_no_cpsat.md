# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 10:33:08
- baseline_file: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_baselines.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 18
- compliant_count: 4
- non_compliant_count: 14
- runtime_fail_count: 0
- quality_fail_count: 14
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1021.548386

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 18 | 4 | 14 | 14 | 0 | 0 | 0.146266 | 56.752688 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 99 | 0.269231 | 35.077349 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 371 | 0.266212 | 88.013207 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 350 | 0.236749 | 35.572003 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 267 | 0.197309 | 47.221916 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_4_3 | 16 | 5 | 4 | 3 | 31 | 37 | 0.193548 | 7.124621 | general_noncontain | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 37 | 0.193548 | 99.949889 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 181 | 0.190789 | 72.382388 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 155 | 0.174242 | 88.863444 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 89 | 0.171053 | 24.777044 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | 16 | 7 | 7 | 4 | 6 | 7 | 0.166667 | 96.371705 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 60 | 0.153846 | 24.814131 | general_noncontain | quality_over_10pct |
| L_16_5_3_3 | 16 | 5 | 3 | 3 | 65 | 73 | 0.123077 | 0.85183 | containment_s_eq_j | quality_over_10pct |
| L_16_4_4_3 | 16 | 4 | 4 | 3 | 64 | 71 | 0.109375 | 35.643954 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 31 | 0.107143 | 31.267037 | general_noncontain | quality_over_10pct |
