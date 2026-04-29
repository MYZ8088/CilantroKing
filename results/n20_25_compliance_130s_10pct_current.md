# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-28 16:18:05
- baseline_file: `D:\ai2026.4\CilantroKing\coveringrepo_n_lt_26_baselines(1).json`
- n_range: [20, 26)
- timeout_sec: 130.0
- hard_timeout_sec: 135.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 145
- compliant_count: 10
- non_compliant_count: 135
- runtime_fail_count: 2
- quality_fail_count: 135
- verify_fail_count: 2
- status_timeout_count: 2
- status_error_count: 0
- elapsed_total_sec: 5333.533781

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 20 | 26 | 2 | 24 | 24 | 0 | 0 | 0.274597 | 25.272298 |
| 21 | 24 | 2 | 22 | 22 | 0 | 0 | 0.320606 | 23.566252 |
| 22 | 24 | 1 | 23 | 23 | 0 | 0 | 0.37756 | 33.132447 |
| 23 | 24 | 2 | 22 | 22 | 0 | 0 | 0.4658 | 43.087603 |
| 24 | 24 | 2 | 22 | 22 | 0 | 0 | 0.474474 | 43.608649 |
| 25 | 23 | 1 | 22 | 22 | 2 | 2 | 0.511554 | 53.694575 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_25_7_6_4 | 25 | 7 | 6 | 4 | 82 | 229 | 1.792683 | 20.585019 | general_noncontain | quality_over_10pct |
| L_24_7_6_4 | 24 | 7 | 6 | 4 | 72 | 186 | 1.583333 | 25.856695 | general_noncontain | quality_over_10pct |
| L_23_7_6_4 | 23 | 7 | 6 | 4 | 62 | 153 | 1.467742 | 10.102854 | general_noncontain | quality_over_10pct |
| L_24_7_6_3 | 24 | 7 | 6 | 3 | 12 | 24 | 1.0 | 29.872965 | general_noncontain | quality_over_10pct |
| L_23_7_6_5 | 23 | 7 | 6 | 5 | 685 | 1348 | 0.967883 | 91.478846 | general_noncontain | quality_over_10pct |
| L_23_7_6_3 | 23 | 7 | 6 | 3 | 10 | 19 | 0.9 | 18.109101 | general_noncontain | quality_over_10pct |
| L_24_7_6_5 | 24 | 7 | 6 | 5 | 895 | 1666 | 0.861453 | 93.252846 | general_noncontain | quality_over_10pct |
| L_25_7_6_3 | 25 | 7 | 6 | 3 | 14 | 26 | 0.857143 | 12.093625 | general_noncontain | quality_over_10pct |
| L_23_7_7_3 | 23 | 7 | 7 | 3 | 6 | 11 | 0.833333 | 105.105841 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_25_7_7_3 | 25 | 7 | 7 | 3 | 9 | 16 | 0.777778 | 70.215674 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_25_6_6_3 | 25 | 6 | 6 | 3 | 22 | 38 | 0.727273 | 121.335894 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_25_6_6_4 | 25 | 6 | 6 | 4 | 166 | 284 | 0.710843 | 121.055056 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_23_6_6_3 | 23 | 6 | 6 | 3 | 17 | 29 | 0.705882 | 121.682702 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_24_6_6_3 | 24 | 6 | 6 | 3 | 20 | 34 | 0.7 | 63.657936 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_24_6_5_4 | 24 | 6 | 5 | 4 | 267 | 446 | 0.670412 | 48.363949 | general_noncontain | quality_over_10pct |
| L_22_6_6_3 | 22 | 6 | 6 | 3 | 15 | 25 | 0.666667 | 83.801761 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_22_6_6_4 | 22 | 6 | 6 | 4 | 101 | 167 | 0.653465 | 11.721532 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_24_6_6_4 | 24 | 6 | 6 | 4 | 143 | 235 | 0.643357 | 89.827287 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_25_6_5_4 | 25 | 6 | 5 | 4 | 334 | 539 | 0.613772 | 98.262831 | general_noncontain | quality_over_10pct |
| L_23_6_5_4 | 23 | 6 | 5 | 4 | 229 | 366 | 0.598253 | 25.450279 | general_noncontain | quality_over_10pct |
| L_25_7_5_4 | 25 | 7 | 5 | 4 | 166 | 265 | 0.596386 | 61.524231 | general_noncontain | quality_over_10pct |
| L_25_7_7_4 | 25 | 7 | 7 | 4 | 54 | 86 | 0.592593 | 116.061425 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_23_6_6_4 | 23 | 6 | 6 | 4 | 121 | 191 | 0.578512 | 49.001208 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_22_6_5_4 | 22 | 6 | 5 | 4 | 189 | 298 | 0.57672 | 17.199368 | general_noncontain | quality_over_10pct |
| L_21_7_6_3 | 21 | 7 | 6 | 3 | 7 | 11 | 0.571429 | 13.061226 | general_noncontain | quality_over_10pct |
| L_25_7_5_3 | 25 | 7 | 5 | 3 | 21 | 33 | 0.571429 | 43.231489 | general_noncontain | quality_over_10pct |
| L_22_6_5_3 | 22 | 6 | 5 | 3 | 22 | 34 | 0.545455 | 21.337121 | general_noncontain | quality_over_10pct |
| L_21_7_7_4 | 21 | 7 | 7 | 4 | 24 | 37 | 0.541667 | 46.933916 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_22_7_5_3 | 22 | 7 | 5 | 3 | 13 | 20 | 0.538462 | 7.607763 | general_noncontain | quality_over_10pct |
| L_24_5_5_4 | 24 | 5 | 5 | 4 | 731 | 1118 | 0.529412 | 108.586764 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_24_7_5_3 | 24 | 7 | 5 | 3 | 19 | 29 | 0.526316 | 35.534267 | general_noncontain | quality_over_10pct |
| L_25_5_5_3 | 25 | 5 | 5 | 3 | 63 | 95 | 0.507937 | 45.024312 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_20_7_7_4 | 20 | 7 | 7 | 4 | 20 | 30 | 0.5 | 96.663422 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_22_7_5_4 | 22 | 7 | 5 | 4 | 98 | 147 | 0.5 | 11.806308 | general_noncontain | quality_over_10pct |
| L_23_7_5_3 | 23 | 7 | 5 | 3 | 16 | 24 | 0.5 | 11.613678 | general_noncontain | quality_over_10pct |
| L_24_5_5_3 | 24 | 5 | 5 | 3 | 54 | 81 | 0.5 | 70.744837 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_24_7_7_3 | 24 | 7 | 7 | 3 | 8 | 12 | 0.5 | 63.902838 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_22_7_4_4 | 22 | 7 | 4 | 4 | 252 | 377 | 0.496032 | 7.86828 | containment_s_eq_j | quality_over_10pct |
| L_23_7_5_4 | 23 | 7 | 5 | 4 | 121 | 180 | 0.487603 | 26.552603 | general_noncontain | quality_over_10pct |
| L_22_5_5_3 | 22 | 5 | 5 | 3 | 40 | 59 | 0.475 | 45.707785 | j_eq_k_noncontain_medium_n | quality_over_10pct |
