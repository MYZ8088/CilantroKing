# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 02:01:51
- source_json: `results/n_lt_16_remaining24_after_opt_v6.json`

## Batch A: n<16

- total_cases: 24
- compliant_count: 2
- non_compliant_count: 22
- quality_fail_count: 22
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 677.629515
- avg_gap_ratio: 0.183831
- median_gap_ratio: 0.169028
- avg_gap_ratio_non_compliant: 0.19362
- avg_elapsed_sec: 28.234563

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 0 | 10 | 10 | 0 | 0 | 0.202109 | 21.042564 |
| general_noncontain | 5 | 1 | 4 | 4 | 0 | 0 | 0.120153 | 29.554027 |
| j_eq_k_noncontain_medium_n | 9 | 1 | 8 | 8 | 0 | 0 | 0.198897 | 35.492637 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_13_7_5_5 | L(13,7,5,5) | 78 | 103 | 0.320513 | 8.117981 | containment_s_eq_j | quality_over_10pct |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 130 | 0.3 | 53.560095 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 102 | 0.275 | 10.248504 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 239 | 0.26455 | 23.136055 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 225 | 0.25 | 28.897436 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 177 | 0.246479 | 48.506592 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 997 | 0.220318 | 36.680809 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 115 | 0.210526 | 43.136342 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 26.135104 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 25.177082 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 588 | 0.173653 | 36.704885 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 137 | 0.17094 | 8.342394 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | L(14,6,5,5) | 371 | 433 | 0.167116 | 20.226795 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 114 | 0.163265 | 48.447055 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 80 | 0.15942 | 30.554384 | j_eq_k_noncontain_medium_n | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 53.560095 | 100 | 130 | 0.3 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 48.506592 | 142 | 177 | 0.246479 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 48.447055 | 98 | 114 | 0.163265 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 43.136342 | 95 | 115 | 0.210526 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 39.492627 | 20 | 23 | 0.15 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 36.704885 | 501 | 588 | 0.173653 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 36.680809 | 817 | 997 | 0.220318 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 31.694289 | 578 | 646 | 0.117647 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 30.718657 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 30.554384 | 69 | 80 | 0.15942 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 28.897436 | 180 | 225 | 0.25 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 26.135104 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 25.177082 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | 24.860138 | 36 | 40 | 0.111111 | general_noncontain | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 24.84008 | 40 | 46 | 0.15 | general_noncontain | quality_over_10pct |

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

