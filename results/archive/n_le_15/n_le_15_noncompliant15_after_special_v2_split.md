# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 20:49:03
- source_json: `results/n_le_15_noncompliant15_after_special_v2.json`

## Batch A: n<16

- total_cases: 15
- compliant_count: 1
- non_compliant_count: 14
- quality_fail_count: 14
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1760.548479
- avg_gap_ratio: 0.149002
- median_gap_ratio: 0.1375
- avg_gap_ratio_non_compliant: 0.155359
- avg_elapsed_sec: 117.369899

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 0 | 6 | 6 | 0 | 0 | 0.157591 | 117.865014 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.122845 | 114.931658 |
| j_eq_k_noncontain_medium_n | 7 | 1 | 6 | 6 | 0 | 0 | 0.149113 | 117.642154 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 118.63938 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 170 | 0.197183 | 117.044728 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 975 | 0.19339 | 116.522171 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 210 | 0.166667 | 118.629081 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 71 | 0.163934 | 118.617213 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 71 | 0.163934 | 118.619213 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 80 | 0.15942 | 118.643856 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.618808 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 111 | 0.132653 | 115.719904 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | 113.282888 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 116.580427 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 560 | 0.117764 | 117.463786 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 154 | 0.115942 | 118.646874 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 130 | 0.111111 | 117.299065 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_5_5 | L(14,7,5,5) | 118.646874 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 118.643856 | 69 | 80 | 0.15942 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 118.63938 | 189 | 240 | 0.269841 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 118.629081 | 180 | 210 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 118.619213 | 61 | 71 | 0.163934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.618808 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 118.617213 | 61 | 71 | 0.163934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 117.463786 | 501 | 560 | 0.117764 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117.299065 | 117 | 130 | 0.111111 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 117.044728 | 142 | 170 | 0.197183 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 116.580427 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 116.522171 | 817 | 975 | 0.19339 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 115.719904 | 98 | 111 | 0.132653 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 113.282888 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |

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

