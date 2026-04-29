# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 20:07:57
- baseline_file: `results/n_le_15_all_legal_baselines_filled_v1.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 12
- CK_USE_GPU: 0

## summary

- total_cases: 306
- compliant_count: 279
- non_compliant_count: 27
- runtime_fail_count: 7
- quality_fail_count: 24
- verify_fail_count: 3
- status_timeout_count: 7
- status_error_count: 0
- elapsed_total_sec: 11641.075968

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 7 | 34 | 34 | 0 | 0 | 0 | 0 | 0.0 | 0.021791 |
| 8 | 34 | 34 | 0 | 0 | 0 | 0 | 0.0 | 0.149848 |
| 9 | 34 | 34 | 0 | 0 | 0 | 0 | 0.0 | 1.554751 |
| 10 | 34 | 34 | 0 | 0 | 0 | 0 | 0.0 | 4.967985 |
| 11 | 34 | 34 | 0 | 0 | 0 | 0 | 0.012169 | 7.955871 |
| 12 | 34 | 32 | 2 | 2 | 2 | 2 | 0.001352 | 74.266152 |
| 13 | 34 | 29 | 5 | 4 | 2 | 1 | 0.025737 | 79.416213 |
| 14 | 34 | 25 | 9 | 9 | 1 | 0 | 0.060435 | 83.651032 |
| 15 | 34 | 23 | 11 | 9 | 2 | 0 | 0.064722 | 90.400945 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 140 | 0.4 | 118.80237 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | 15 | 5 | 5 | 4 | 95 | 119 | 0.252632 | 116.493235 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 234 | 0.238095 | 117.956648 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 175 | 0.232394 | 117.771556 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 118.659859 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 117.14091 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 588 | 0.173653 | 116.087579 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 210 | 0.166667 | 118.314272 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 953 | 0.166463 | 115.731159 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 46 | 0.15 | 117.238599 | general_noncontain | quality_over_10pct |
| L_15_7_5_4 | 15 | 7 | 5 | 4 | 20 | 23 | 0.15 | 117.882831 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 118.631917 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 118.640103 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_7_5 | 14 | 7 | 7 | 5 | 14 | 16 | 0.142857 | 116.41577 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.640047 | containment_s_eq_j | quality_over_10pct |
| L_13_5_5_4 | 13 | 5 | 5 | 4 | 48 | 54 | 0.125 | 114.916148 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 117.464256 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 154 | 0.115942 | 118.814498 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | 15 | 6 | 5 | 5 | 578 | 645 | 0.115917 | 116.670766 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_5 | 14 | 7 | 6 | 5 | 36 | 40 | 0.111111 | 115.941588 | general_noncontain | quality_over_10pct |
| L_14_6_5_4 | 14 | 6 | 5 | 4 | 29 | 32 | 0.103448 | 120.000635 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_15_6_4_3 | 15 | 6 | 4 | 3 | 14 | 15 | 0.071429 | 120.000761 | general_noncontain | timeout_over_120s |
| L_13_7_6_5 | 13 | 7 | 6 | 5 | 24 | 24 | 0.0 | 120.001438 | general_noncontain | timeout_over_120s |
| L_15_7_6_4 | 15 | 7 | 6 | 4 | 9 | 9 | 0.0 | 120.000536 | general_noncontain | timeout_over_120s |
