# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 02:15:50
- baseline_file: `D:\ai2026.4\CilantroKing\results\coveringrepo_n_lt_26_baselines.json`
- n_range: [7, 18)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 313
- compliant_count: 240
- non_compliant_count: 73
- runtime_fail_count: 2
- quality_fail_count: 73
- verify_fail_count: 3
- status_timeout_count: 2
- status_error_count: 0
- elapsed_total_sec: 10492.81313

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 7 | 16 | 16 | 0 | 0 | 0 | 0 | 0.0 | 0.018235 |
| 8 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 0.099573 |
| 9 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 1.382729 |
| 10 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 4.972545 |
| 11 | 30 | 30 | 0 | 0 | 0 | 0 | 0.008811 | 7.929636 |
| 12 | 30 | 30 | 0 | 0 | 0 | 0 | 0.005044 | 49.432419 |
| 13 | 30 | 24 | 6 | 6 | 0 | 0 | 0.044919 | 54.549475 |
| 14 | 30 | 21 | 9 | 9 | 0 | 0 | 0.076732 | 77.0724 |
| 15 | 30 | 18 | 12 | 12 | 0 | 0 | 0.096177 | 90.355526 |
| 16 | 29 | 8 | 21 | 21 | 0 | 0 | 0.17315 | 30.500868 |
| 17 | 28 | 3 | 25 | 25 | 2 | 3 | 0.234025 | 36.93454 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_17_7_7_6 | 17 | 7 | 7 | 6 | 444 | 607 | 0.367117 | 32.28929 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_6_5_3 | 17 | 6 | 5 | 3 | 11 | 15 | 0.363636 | 17.156203 | general_noncontain | quality_over_10pct |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 106 | 0.358974 | 21.507951 | general_noncontain | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 42 | 0.354839 | 59.493029 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_6_5_4 | 17 | 6 | 5 | 4 | 66 | 89 | 0.348485 | 16.576761 | general_noncontain | quality_over_10pct |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 133 | 0.33 | 119.354657 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_5_3_3 | 17 | 5 | 3 | 3 | 68 | 90 | 0.323529 | 0.648932 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 250 | 0.322751 | 119.360449 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_3 | 16 | 6 | 4 | 3 | 16 | 21 | 0.3125 | 10.562487 | general_noncontain | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 186 | 0.309859 | 119.403804 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | 13 | 7 | 5 | 5 | 78 | 102 | 0.307692 | 49.880027 | containment_s_eq_j | quality_over_10pct |
| L_16_7_6_4 | 16 | 7 | 6 | 4 | 13 | 17 | 0.307692 | 20.490111 | general_noncontain | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 235 | 0.305556 | 119.402877 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 382 | 0.303754 | 32.799461 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_6_4_4 | 17 | 6 | 4 | 4 | 188 | 243 | 0.292553 | 0.499268 | containment_s_eq_j | quality_over_10pct |
| L_17_7_6_5 | 17 | 7 | 6 | 5 | 115 | 148 | 0.286957 | 6.21692 | general_noncontain | quality_over_10pct |
| L_17_7_4_4 | 17 | 7 | 4 | 4 | 98 | 126 | 0.285714 | 0.549736 | containment_s_eq_j | quality_over_10pct |
| L_17_7_5_5 | 17 | 7 | 5 | 5 | 398 | 510 | 0.281407 | 0.869818 | containment_s_eq_j | quality_over_10pct |
| L_17_5_5_3 | 17 | 5 | 5 | 3 | 18 | 23 | 0.277778 | 90.078873 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_7_6_4 | 17 | 7 | 6 | 4 | 18 | 23 | 0.277778 | 39.78572 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 361 | 0.275618 | 0.537422 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 102 | 0.275 | 55.030741 | containment_s_eq_j | quality_over_10pct |
| L_17_6_6_4 | 17 | 6 | 6 | 4 | 33 | 42 | 0.272727 | 47.418635 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 192 | 0.263158 | 0.37766 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 96 | 0.263158 | 1.099424 | containment_s_eq_j | quality_over_10pct |
| L_17_7_3_3 | 17 | 7 | 3 | 3 | 27 | 34 | 0.259259 | 5.220032 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_4 | 15 | 7 | 5 | 4 | 20 | 25 | 0.25 | 119.456505 | general_noncontain | quality_over_10pct |
| L_16_6_5_3 | 16 | 6 | 5 | 3 | 8 | 10 | 0.25 | 8.376649 | general_noncontain | quality_over_10pct |
| L_17_6_3_3 | 17 | 6 | 3 | 3 | 44 | 55 | 0.25 | 7.562758 | containment_s_eq_j | quality_over_10pct |
| L_17_6_4_3 | 17 | 6 | 4 | 3 | 20 | 25 | 0.25 | 15.663334 | general_noncontain | quality_over_10pct |
| L_17_5_5_4 | 17 | 5 | 5 | 4 | 175 | 218 | 0.245714 | 71.913445 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_5_4_3 | 17 | 5 | 4 | 3 | 37 | 46 | 0.243243 | 11.411059 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 276 | 0.237668 | 60.092025 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 163 | 0.234848 | 111.990211 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 64 | 0.230769 | 9.522162 | general_noncontain | quality_over_10pct |
| L_17_7_4_3 | 17 | 7 | 4 | 3 | 13 | 16 | 0.230769 | 8.865958 | general_noncontain | quality_over_10pct |
| L_17_7_7_5 | 17 | 7 | 7 | 5 | 49 | 60 | 0.22449 | 77.861409 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 998 | 0.221542 | 119.414207 | containment_s_eq_j | quality_over_10pct |
| L_17_7_5_4 | 17 | 7 | 5 | 4 | 37 | 45 | 0.216216 | 19.736515 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 34 | 0.214286 | 14.341052 | general_noncontain | quality_over_10pct |
