# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 13:47:46
- source_json: `results/n_lt_16_remaining20_after_opt_v17.json`

## Batch A: n<16

- total_cases: 20
- compliant_count: 5
- non_compliant_count: 15
- quality_fail_count: 15
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 2356.299378
- avg_gap_ratio: 0.134991
- median_gap_ratio: 0.143893
- avg_gap_ratio_non_compliant: 0.171308
- avg_elapsed_sec: 117.814969

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 4 | 6 | 6 | 0 | 0 | 0.112443 | 117.548595 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.122845 | 117.009373 |
| j_eq_k_noncontain_medium_n | 8 | 1 | 7 | 7 | 0 | 0 | 0.166212 | 118.349335 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 116.921317 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 223 | 0.238889 | 117.547504 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 123 | 0.23 | 118.221679 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 170 | 0.197183 | 118.655111 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 118.627719 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 960 | 0.175031 | 117.04154 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 588 | 0.173653 | 117.053951 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 71 | 0.163934 | 118.631943 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 116.972991 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 79 | 0.144928 | 118.65858 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 117.82141 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.650384 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | 116.991276 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 117.02747 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 154 | 0.115942 | 116.982018 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_5_5_4 | L(14,5,5,4) | 118.65858 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 118.655111 | 142 | 170 | 0.197183 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.650384 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 118.631943 | 61 | 71 | 0.163934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 118.627719 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_7_6 | L(14,7,7,6) | 118.221679 | 100 | 123 | 0.23 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 117.82141 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 117.547504 | 180 | 223 | 0.238889 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 117.053951 | 501 | 588 | 0.173653 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 117.04154 | 817 | 960 | 0.175031 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 117.02747 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 116.991276 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 116.982018 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 116.972991 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 116.921317 | 189 | 240 | 0.269841 | containment_s_eq_j | quality_over_10pct |

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

