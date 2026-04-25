# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 09:39:54
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
- elapsed_total_sec: 830.600381

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 18 | 4 | 14 | 14 | 0 | 0 | 0.152528 | 46.144466 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 370 | 0.262799 | 51.525032 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 98 | 0.25641 | 25.065458 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 347 | 0.226148 | 39.40642 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 38 | 0.225806 | 99.231845 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 158 | 0.19697 | 57.695738 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_4_3 | 16 | 5 | 4 | 3 | 31 | 37 | 0.193548 | 8.729853 | general_noncontain | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 62 | 0.192308 | 11.01378 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 180 | 0.184211 | 35.968023 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 262 | 0.174888 | 41.380021 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_4 | 16 | 7 | 7 | 4 | 6 | 7 | 0.166667 | 95.322019 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 88 | 0.157895 | 19.983554 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 32 | 0.142857 | 32.561285 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | 16 | 4 | 4 | 3 | 64 | 72 | 0.125 | 22.770539 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | 16 | 5 | 3 | 3 | 65 | 73 | 0.123077 | 0.597375 | containment_s_eq_j | quality_over_10pct |
