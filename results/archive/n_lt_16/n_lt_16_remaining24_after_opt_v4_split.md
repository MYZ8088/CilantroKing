# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 01:46:13
- source_json: `results/n_lt_16_remaining24_after_opt_v4.json`

## Batch A: n<16

- total_cases: 24
- compliant_count: 1
- non_compliant_count: 23
- quality_fail_count: 23
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 716.289886
- avg_gap_ratio: 0.187156
- median_gap_ratio: 0.162829
- avg_gap_ratio_non_compliant: 0.19167
- avg_elapsed_sec: 29.845412

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 0 | 10 | 10 | 0 | 0 | 0.201191 | 23.090265 |
| general_noncontain | 5 | 0 | 5 | 5 | 0 | 0 | 0.13795 | 29.10916 |
| j_eq_k_noncontain_medium_n | 9 | 1 | 8 | 8 | 0 | 0 | 0.198897 | 37.760159 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_13_7_5_5 | L(13,7,5,5) | 78 | 102 | 0.307692 | 11.807938 | containment_s_eq_j | quality_over_10pct |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 130 | 0.3 | 64.735937 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 242 | 0.280423 | 15.690758 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 101 | 0.2625 | 14.216117 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 225 | 0.25 | 36.320714 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 177 | 0.246479 | 50.022367 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 1003 | 0.227662 | 44.409094 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 115 | 0.210526 | 47.440399 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 22.86349 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 24.216658 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 586 | 0.169661 | 35.281271 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 114 | 0.163265 | 47.609352 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 136 | 0.162393 | 15.915299 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 80 | 0.15942 | 29.941184 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 160 | 0.15942 | 16.610082 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 64.735937 | 100 | 130 | 0.3 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 50.022367 | 142 | 177 | 0.246479 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 47.609352 | 98 | 114 | 0.163265 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 47.440399 | 95 | 115 | 0.210526 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 44.409094 | 817 | 1003 | 0.227662 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 42.843967 | 20 | 23 | 0.15 | general_noncontain | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 39.556069 | 578 | 652 | 0.128028 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 36.320714 | 180 | 225 | 0.25 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 35.281271 | 501 | 586 | 0.169661 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 30.573558 | 58 | 66 | 0.137931 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 29.941184 | 69 | 80 | 0.15942 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 26.658497 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 24.216658 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_5_4 | L(14,6,5,4) | 23.417131 | 29 | 33 | 0.137931 | general_noncontain | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 22.86349 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |

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

