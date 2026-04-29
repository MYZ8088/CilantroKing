# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 22:27:27
- baseline_file: `D:\ai2026.4\CilantroKing\results\n_eq_16_remaining13_baseline_from_v6.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 13
- compliant_count: 1
- non_compliant_count: 12
- runtime_fail_count: 0
- quality_fail_count: 12
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1231.48121

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 13 | 1 | 12 | 12 | 0 | 0 | 0.179962 | 94.729324 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 99 | 0.269231 | 103.121238 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 371 | 0.266212 | 118.354972 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 349 | 0.233216 | 117.128739 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 38 | 0.225806 | 115.884925 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 181 | 0.190789 | 116.221509 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 263 | 0.179372 | 115.47141 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 155 | 0.174242 | 116.599981 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 89 | 0.171053 | 114.96127 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | 16 | 7 | 7 | 4 | 6 | 7 | 0.166667 | 103.464694 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 60 | 0.153846 | 31.158648 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | 16 | 4 | 4 | 3 | 64 | 72 | 0.125 | 46.150573 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 31 | 0.107143 | 116.092198 | general_noncontain | quality_over_10pct |
