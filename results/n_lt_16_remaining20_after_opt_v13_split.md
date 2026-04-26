# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 09:47:28
- source_json: `results/n_lt_16_remaining20_after_opt_v13.json`

## Batch A: n<16

- total_cases: 20
- compliant_count: 0
- non_compliant_count: 20
- quality_fail_count: 20
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 790.962103
- avg_gap_ratio: 0.195241
- median_gap_ratio: 0.182978
- avg_gap_ratio_non_compliant: 0.195241
- avg_elapsed_sec: 39.548105

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 0 | 10 | 10 | 0 | 0 | 0.194187 | 36.436952 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.135345 | 30.985742 |
| j_eq_k_noncontain_medium_n | 8 | 0 | 8 | 8 | 0 | 0 | 0.211531 | 45.577637 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 130 | 0.3 | 64.066964 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | L(13,7,5,5) | 78 | 101 | 0.294872 | 14.382892 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 241 | 0.275132 | 42.96541 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 100 | 0.25 | 16.586461 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 225 | 0.25 | 59.392963 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 177 | 0.246479 | 70.972705 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 115 | 0.210526 | 51.914801 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 986 | 0.206854 | 54.665327 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 22.176988 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 594 | 0.185629 | 43.272548 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 21.735751 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 114 | 0.163265 | 49.575569 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_5_5 | L(13,6,5,5) | 245 | 283 | 0.155102 | 23.245382 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 27.078141 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | L(14,6,5,5) | 371 | 427 | 0.150943 | 40.543829 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_6_5 | L(15,6,6,5) | 70.972705 | 142 | 177 | 0.246479 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 64.989832 | 578 | 650 | 0.124567 | containment_s_eq_j | quality_over_10pct |
| L_14_7_7_6 | L(14,7,7,6) | 64.066964 | 100 | 130 | 0.3 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 59.392963 | 180 | 225 | 0.25 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 54.665327 | 817 | 986 | 0.206854 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 51.914801 | 95 | 115 | 0.210526 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 49.575569 | 98 | 114 | 0.163265 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 43.272548 | 501 | 594 | 0.185629 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 42.96541 | 189 | 241 | 0.275132 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | L(14,6,5,5) | 40.543829 | 371 | 427 | 0.150943 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 37.101862 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 36.639703 | 138 | 158 | 0.144928 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 27.078141 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 24.869622 | 40 | 46 | 0.15 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 24.785353 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |

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

