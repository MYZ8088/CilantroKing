# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 20:49:03
- baseline_file: `results/n_le_15_noncompliant15_baselines_v19.json`
- n_range: [13, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 15
- compliant_count: 1
- non_compliant_count: 14
- runtime_fail_count: 0
- quality_fail_count: 14
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1760.548479

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.163934 | 118.618213 |
| 14 | 6 | 1 | 5 | 5 | 0 | 0 | 0.120547 | 117.552385 |
| 15 | 7 | 0 | 7 | 7 | 0 | 0 | 0.169126 | 116.85682 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 118.63938 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 170 | 0.197183 | 117.044728 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 975 | 0.19339 | 116.522171 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 210 | 0.166667 | 118.629081 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 71 | 0.163934 | 118.617213 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 71 | 0.163934 | 118.619213 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 80 | 0.15942 | 118.643856 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.618808 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 111 | 0.132653 | 115.719904 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 113.282888 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 116.580427 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 560 | 0.117764 | 117.463786 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 154 | 0.115942 | 118.646874 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 130 | 0.111111 | 117.299065 | containment_s_eq_j | quality_over_10pct |
