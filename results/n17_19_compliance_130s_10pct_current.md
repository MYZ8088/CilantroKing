# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-28 15:28:54
- baseline_file: `D:\ai2026.4\CilantroKing\coveringrepo_n_lt_26_baselines(1).json`
- n_range: [17, 20)
- timeout_sec: 130.0
- hard_timeout_sec: 135.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 84
- compliant_count: 9
- non_compliant_count: 75
- runtime_fail_count: 2
- quality_fail_count: 75
- verify_fail_count: 2
- status_timeout_count: 2
- status_error_count: 0
- elapsed_total_sec: 2722.707816

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 17 | 28 | 3 | 25 | 25 | 2 | 2 | 0.236686 | 37.74118 |
| 18 | 28 | 4 | 24 | 24 | 0 | 0 | 0.220022 | 35.314492 |
| 19 | 28 | 2 | 26 | 26 | 0 | 0 | 0.258545 | 24.183893 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_19_7_7_6 | 19 | 7 | 7 | 6 | 933 | 1414 | 0.515541 | 108.073622 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_19_6_5_3 | 19 | 6 | 5 | 3 | 15 | 22 | 0.466667 | 44.342193 | general_noncontain | quality_over_10pct |
| L_19_7_7_4 | 19 | 7 | 7 | 4 | 15 | 22 | 0.466667 | 36.907063 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_18_7_7_6 | 18 | 7 | 7 | 6 | 654 | 946 | 0.446483 | 82.439104 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_18_6_5_4 | 18 | 6 | 5 | 4 | 81 | 113 | 0.395062 | 29.15921 | general_noncontain | quality_over_10pct |
| L_19_6_6_4 | 19 | 6 | 6 | 4 | 53 | 73 | 0.377358 | 67.323606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_7_7_6 | 17 | 7 | 7 | 6 | 444 | 608 | 0.369369 | 43.518127 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_6_5_3 | 17 | 6 | 5 | 3 | 11 | 15 | 0.363636 | 20.39472 | general_noncontain | quality_over_10pct |
| L_18_7_7_4 | 18 | 7 | 7 | 4 | 11 | 15 | 0.363636 | 18.706386 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_6_5_4 | 17 | 6 | 5 | 4 | 66 | 89 | 0.348485 | 17.683415 | general_noncontain | quality_over_10pct |
| L_18_5_5_4 | 18 | 5 | 5 | 4 | 214 | 288 | 0.345794 | 84.081188 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_19_7_3_3 | 19 | 7 | 3 | 3 | 35 | 47 | 0.342857 | 2.18943 | containment_s_eq_j | quality_over_10pct |
| L_17_5_5_3 | 17 | 5 | 5 | 3 | 18 | 24 | 0.333333 | 69.101304 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_18_7_4_3 | 18 | 7 | 4 | 3 | 15 | 20 | 0.333333 | 21.123436 | general_noncontain | quality_over_10pct |
| L_19_6_6_3 | 19 | 6 | 6 | 3 | 9 | 12 | 0.333333 | 13.876464 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_5_3_3 | 17 | 5 | 3 | 3 | 68 | 90 | 0.323529 | 1.43634 | containment_s_eq_j | quality_over_10pct |
| L_19_7_5_5 | 19 | 7 | 5 | 5 | 703 | 930 | 0.322902 | 3.750168 | containment_s_eq_j | quality_over_10pct |
| L_18_5_5_3 | 18 | 5 | 5 | 3 | 22 | 29 | 0.318182 | 79.019953 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_19_5_5_4 | 19 | 5 | 5 | 4 | 284 | 373 | 0.31338 | 29.261962 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_19_7_5_4 | 19 | 7 | 5 | 4 | 57 | 74 | 0.298246 | 21.343803 | general_noncontain | quality_over_10pct |
| L_19_7_4_4 | 19 | 7 | 4 | 4 | 151 | 196 | 0.298013 | 2.454474 | containment_s_eq_j | quality_over_10pct |
| L_17_6_4_4 | 17 | 6 | 4 | 4 | 188 | 243 | 0.292553 | 1.685735 | containment_s_eq_j | quality_over_10pct |
| L_18_6_4_4 | 18 | 6 | 4 | 4 | 236 | 305 | 0.292373 | 1.544135 | containment_s_eq_j | quality_over_10pct |
| L_19_5_4_3 | 19 | 5 | 4 | 3 | 52 | 67 | 0.288462 | 11.369357 | general_noncontain | quality_over_10pct |
| L_17_7_6_5 | 17 | 7 | 6 | 5 | 115 | 148 | 0.286957 | 7.778206 | general_noncontain | quality_over_10pct |
| L_17_7_4_4 | 17 | 7 | 4 | 4 | 98 | 126 | 0.285714 | 1.270058 | containment_s_eq_j | quality_over_10pct |
| L_18_6_6_3 | 18 | 6 | 6 | 3 | 7 | 9 | 0.285714 | 115.759273 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_19_7_7_5 | 19 | 7 | 7 | 5 | 92 | 118 | 0.282609 | 13.455268 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_7_5_5 | 17 | 7 | 5 | 5 | 398 | 510 | 0.281407 | 1.779258 | containment_s_eq_j | quality_over_10pct |
| L_18_7_3_3 | 18 | 7 | 3 | 3 | 32 | 41 | 0.28125 | 8.881355 | containment_s_eq_j | quality_over_10pct |
| L_19_6_5_4 | 19 | 6 | 5 | 4 | 111 | 142 | 0.279279 | 7.388238 | general_noncontain | quality_over_10pct |
| L_18_5_4_3 | 18 | 5 | 4 | 3 | 43 | 55 | 0.27907 | 17.925586 | general_noncontain | quality_over_10pct |
| L_19_7_6_5 | 19 | 7 | 6 | 5 | 233 | 298 | 0.27897 | 16.289872 | general_noncontain | quality_over_10pct |
| L_17_7_6_4 | 17 | 7 | 6 | 4 | 18 | 23 | 0.277778 | 45.797336 | general_noncontain | quality_over_10pct |
| L_19_7_4_3 | 19 | 7 | 4 | 3 | 18 | 23 | 0.277778 | 21.007754 | general_noncontain | quality_over_10pct |
| L_17_6_6_4 | 17 | 6 | 6 | 4 | 33 | 42 | 0.272727 | 56.504236 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_18_7_5_5 | 18 | 7 | 5 | 5 | 548 | 696 | 0.270073 | 2.280458 | containment_s_eq_j | quality_over_10pct |
| L_18_7_4_4 | 18 | 7 | 4 | 4 | 126 | 160 | 0.269841 | 1.647418 | containment_s_eq_j | quality_over_10pct |
| L_19_5_5_3 | 19 | 5 | 5 | 3 | 26 | 33 | 0.269231 | 39.879327 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_5_5_4 | 17 | 5 | 5 | 4 | 175 | 221 | 0.262857 | 51.726716 | j_eq_k_noncontain_medium_n | quality_over_10pct |
