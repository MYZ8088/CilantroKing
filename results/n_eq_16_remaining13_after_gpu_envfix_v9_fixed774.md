# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 03:11:44
- baseline_file: `D:\ai2026.4\CilantroKing\results\n_eq_16_remaining13_baseline_from_v6.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 13
- compliant_count: 3
- non_compliant_count: 10
- runtime_fail_count: 0
- quality_fail_count: 10
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1350.337777

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 13 | 3 | 10 | 10 | 0 | 0 | 0.167892 | 103.872137 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 372 | 0.269625 | 116.30131 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 99 | 0.269231 | 115.556886 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 351 | 0.240283 | 116.414916 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 38 | 0.225806 | 117.263231 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 181 | 0.190789 | 115.557301 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 157 | 0.189394 | 115.924497 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 263 | 0.179372 | 115.794511 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 89 | 0.171053 | 114.7387 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 60 | 0.153846 | 71.251566 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 31 | 0.107143 | 117.425393 | general_noncontain | quality_over_10pct |
