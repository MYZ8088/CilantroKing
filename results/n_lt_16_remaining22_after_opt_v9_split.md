# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 02:41:58
- source_json: `results/n_lt_16_remaining22_after_opt_v9.json`

## Batch A: n<16

- total_cases: 22
- compliant_count: 1
- non_compliant_count: 21
- quality_fail_count: 21
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1066.41556
- avg_gap_ratio: 0.188097
- median_gap_ratio: 0.171796
- avg_gap_ratio_non_compliant: 0.193086
- avg_elapsed_sec: 48.473435

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 0 | 10 | 10 | 0 | 0 | 0.194187 | 43.559846 |
| general_noncontain | 4 | 1 | 3 | 3 | 0 | 0 | 0.126006 | 44.322366 |
| j_eq_k_noncontain_medium_n | 8 | 0 | 8 | 8 | 0 | 0 | 0.211531 | 56.690955 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 130 | 0.3 | 83.242323 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | L(13,7,5,5) | 78 | 101 | 0.294872 | 23.3463 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 241 | 0.275132 | 47.182401 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 100 | 0.25 | 25.182753 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 225 | 0.25 | 60.413478 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 177 | 0.246479 | 68.042398 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 115 | 0.210526 | 66.422152 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 986 | 0.206854 | 59.838862 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 36.103433 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 594 | 0.185629 | 53.500593 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 36.753743 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 114 | 0.163265 | 63.385915 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_5_5 | L(13,6,5,5) | 245 | 283 | 0.155102 | 40.270505 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 29.991849 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | L(14,6,5,5) | 371 | 427 | 0.150943 | 53.521982 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 83.242323 | 100 | 130 | 0.3 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 68.042398 | 142 | 177 | 0.246479 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 66.422152 | 95 | 115 | 0.210526 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 63.385915 | 98 | 114 | 0.163265 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 62.810038 | 20 | 23 | 0.15 | general_noncontain | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 61.425833 | 578 | 650 | 0.124567 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 60.413478 | 180 | 225 | 0.25 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 59.838862 | 817 | 986 | 0.206854 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | L(14,6,5,5) | 53.521982 | 371 | 427 | 0.150943 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 53.500593 | 501 | 594 | 0.185629 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 47.182401 | 189 | 241 | 0.275132 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 41.337378 | 138 | 158 | 0.144928 | containment_s_eq_j | quality_over_10pct |
| L_13_6_5_5 | L(13,6,5,5) | 40.270505 | 245 | 283 | 0.155102 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 39.884161 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 39.164197 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |

## Batch B: 16<=n<18

- total_cases: 0
- compliant_count: 0
- non_compliant_count: 0
- quality_fail_count: 0
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 0.0
- avg_gap_ratio: None
- median_gap_ratio: None
- avg_gap_ratio_non_compliant: None
- avg_elapsed_sec: None

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |

