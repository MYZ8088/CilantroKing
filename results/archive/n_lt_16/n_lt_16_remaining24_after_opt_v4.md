# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 01:46:13
- baseline_file: `results/n_lt_16_remaining24_batch3_baselines.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 24
- compliant_count: 1
- non_compliant_count: 23
- runtime_fail_count: 0
- quality_fail_count: 23
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 716.289886

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 5 | 1 | 4 | 4 | 0 | 0 | 0.184635 | 18.504754 |
| 14 | 9 | 0 | 9 | 9 | 0 | 0 | 0.183346 | 30.481711 |
| 15 | 10 | 0 | 10 | 10 | 0 | 0 | 0.191844 | 34.943072 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_13_7_5_5 | 13 | 7 | 5 | 5 | 78 | 102 | 0.307692 | 11.807938 | containment_s_eq_j | quality_over_10pct |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 130 | 0.3 | 64.735937 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 242 | 0.280423 | 15.690758 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 101 | 0.2625 | 14.216117 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 225 | 0.25 | 36.320714 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 177 | 0.246479 | 50.022367 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 1003 | 0.227662 | 44.409094 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | 15 | 5 | 5 | 4 | 95 | 115 | 0.210526 | 47.440399 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 22.86349 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 24.216658 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 586 | 0.169661 | 35.281271 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 114 | 0.163265 | 47.609352 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 136 | 0.162393 | 15.915299 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 80 | 0.15942 | 29.941184 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 160 | 0.15942 | 16.610082 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | 14 | 6 | 5 | 5 | 371 | 430 | 0.15903 | 20.471674 | containment_s_eq_j | quality_over_10pct |
| L_13_6_5_5 | 13 | 6 | 5 | 5 | 245 | 283 | 0.155102 | 16.94435 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_4 | 15 | 7 | 5 | 4 | 20 | 23 | 0.15 | 42.843967 | general_noncontain | quality_over_10pct |
| L_14_7_6_5 | 14 | 7 | 6 | 5 | 36 | 41 | 0.138889 | 22.052648 | general_noncontain | quality_over_10pct |
| L_14_6_5_4 | 14 | 6 | 5 | 4 | 29 | 33 | 0.137931 | 23.417131 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 66 | 0.137931 | 30.573558 | general_noncontain | quality_over_10pct |
| L_15_6_5_5 | 15 | 6 | 5 | 5 | 578 | 652 | 0.128028 | 39.556069 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 26.658497 | general_noncontain | quality_over_10pct |
