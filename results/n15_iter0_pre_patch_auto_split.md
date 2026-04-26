# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 01:00:08
- source_json: `results\n15_iter0_pre_patch_auto.json`

## Batch A: n<16

- total_cases: 14
- compliant_count: 0
- non_compliant_count: 14
- quality_fail_count: 14
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1531.951971
- avg_gap_ratio: 0.17427
- median_gap_ratio: 0.16388
- avg_gap_ratio_non_compliant: 0.17427
- avg_elapsed_sec: 109.425141

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 0 | 6 | 6 | 0 | 0 | 0.159239 | 108.043902 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.122845 | 119.26007 |
| j_eq_k_noncontain_medium_n | 6 | 0 | 6 | 6 | 0 | 0 | 0.206443 | 107.52807 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 100.952524 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 180 | 0.267606 | 102.224921 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 224 | 0.244444 | 104.010061 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 74 | 0.213115 | 100.344409 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 100.58893 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 960 | 0.175031 | 108.104027 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 81 | 0.173913 | 118.958632 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 99.40024 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 119.041466 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.957107 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | 119.202057 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 119.318083 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 560 | 0.117764 | 101.880094 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 152 | 0.101449 | 118.96942 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_6_5 | L(15,7,6,5) | 119.318083 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 119.202057 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 119.041466 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 118.96942 | 138 | 152 | 0.101449 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 118.958632 | 69 | 81 | 0.173913 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.957107 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 108.104027 | 817 | 960 | 0.175031 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 104.010061 | 180 | 224 | 0.244444 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 102.224921 | 142 | 180 | 0.267606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 101.880094 | 501 | 560 | 0.117764 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 100.952524 | 189 | 240 | 0.269841 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 100.58893 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 100.344409 | 61 | 74 | 0.213115 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 99.40024 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |

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

