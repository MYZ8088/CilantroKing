# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 01:22:37
- source_json: `results\n15_subset9_post_patch_auto.json`

## Batch A: n<16

- total_cases: 9
- compliant_count: 0
- non_compliant_count: 9
- quality_fail_count: 9
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 992.741478
- avg_gap_ratio: 0.158593
- median_gap_ratio: 0.145709
- avg_gap_ratio_non_compliant: 0.158593
- avg_elapsed_sec: 110.304609

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 3 | 0 | 3 | 3 | 0 | 0 | 0.138499 | 108.003751 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.122845 | 115.78869 |
| j_eq_k_noncontain_medium_n | 4 | 0 | 4 | 4 | 0 | 0 | 0.191537 | 109.288211 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 221 | 0.227778 | 105.402085 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 74 | 0.213115 | 103.668933 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 72 | 0.180328 | 112.370681 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 101.836058 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 574 | 0.145709 | 105.235906 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 79 | 0.144928 | 115.711146 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | 115.488635 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 116.088745 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 154 | 0.115942 | 116.939289 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_5_5 | L(14,7,5,5) | 116.939289 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 116.088745 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 115.711146 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 115.488635 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 112.370681 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 105.402085 | 180 | 221 | 0.227778 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 105.235906 | 501 | 574 | 0.145709 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 103.668933 | 61 | 74 | 0.213115 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 101.836058 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |

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

