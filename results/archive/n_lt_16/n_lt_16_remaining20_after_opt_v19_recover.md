# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 19:32:40
- baseline_file: `results/n_lt_16_remaining20_from_v10_baselines.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 20
- compliant_count: 5
- non_compliant_count: 15
- runtime_fail_count: 0
- quality_fail_count: 15
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 2352.90066

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 4 | 2 | 2 | 2 | 0 | 0 | 0.081967 | 116.722547 |
| 14 | 7 | 1 | 6 | 6 | 0 | 0 | 0.131897 | 118.153664 |
| 15 | 9 | 2 | 7 | 7 | 0 | 0 | 0.160006 | 117.659425 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 118.667085 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 180 | 0.267606 | 117.797434 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 126 | 0.26 | 117.5293 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 220 | 0.222222 | 117.224001 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 975 | 0.19339 | 116.205684 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 71 | 0.163934 | 115.985762 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 71 | 0.163934 | 117.743786 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 80 | 0.15942 | 118.622303 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.625106 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 111 | 0.132653 | 117.376153 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 117.975065 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 118.51414 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 560 | 0.117764 | 118.45606 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 154 | 0.115942 | 118.63269 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 130 | 0.111111 | 117.579993 | containment_s_eq_j | quality_over_10pct |
