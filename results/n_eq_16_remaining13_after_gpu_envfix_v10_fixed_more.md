# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 06:45:22
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
- elapsed_total_sec: 1245.466826

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 13 | 3 | 10 | 10 | 0 | 0 | 0.164293 | 95.80514 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 99 | 0.269231 | 114.688586 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 370 | 0.262799 | 114.729031 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 351 | 0.240283 | 114.519515 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 38 | 0.225806 | 115.176577 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 181 | 0.190789 | 115.578914 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 156 | 0.181818 | 115.586696 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 263 | 0.179372 | 116.267999 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 88 | 0.157895 | 85.636213 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 59 | 0.134615 | 43.826068 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 31 | 0.107143 | 117.292924 | general_noncontain | quality_over_10pct |
