# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 06:59:50
- source_json: `D:\ai2026.4\CilantroKing\results\n_le_15_post_n16_iter_v10.json`

## Batch A: n<16

- total_cases: 14
- compliant_count: 1
- non_compliant_count: 13
- quality_fail_count: 13
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1446.150801
- avg_gap_ratio: 0.180935
- median_gap_ratio: 0.176899
- avg_gap_ratio_non_compliant: 0.18716
- avg_elapsed_sec: 103.296486

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 0 | 6 | 6 | 0 | 0 | 0.200699 | 117.943105 |
| general_noncontain | 2 | 1 | 1 | 1 | 0 | 0 | 0.110345 | 60.114165 |
| j_eq_k_noncontain_medium_n | 6 | 0 | 6 | 6 | 0 | 0 | 0.1847 | 103.043973 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 239 | 0.26455 | 119.666377 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 177 | 0.246479 | 117.618856 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 224 | 0.244444 | 117.883092 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 99 | 0.2375 | 116.287667 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 990 | 0.21175 | 117.080718 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 597 | 0.191617 | 117.778405 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 77.404721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 115 | 0.173469 | 117.93174 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 118.097709 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 70 | 0.147541 | 89.151896 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 158 | 0.144928 | 118.747756 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 68.980882 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 77 | 0.115942 | 98.273534 | j_eq_k_noncontain_medium_n | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 119.666377 | 189 | 239 | 0.26455 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 118.747756 | 138 | 158 | 0.144928 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 118.097709 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 117.93174 | 98 | 115 | 0.173469 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 117.883092 | 180 | 224 | 0.244444 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 117.778405 | 501 | 597 | 0.191617 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 117.618856 | 142 | 177 | 0.246479 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 117.080718 | 817 | 990 | 0.21175 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 116.287667 | 80 | 99 | 0.2375 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 98.273534 | 69 | 77 | 0.115942 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 89.151896 | 61 | 70 | 0.147541 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 77.404721 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 68.980882 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |

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

