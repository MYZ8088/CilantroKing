# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 14:01:05
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_after_anchor_v6_no_cpsat_full.json`

## Batch A: n<16

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

## Batch B: 16<=n<18

- total_cases: 29
- compliant_count: 16
- non_compliant_count: 13
- quality_fail_count: 13
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1935.32286
- avg_gap_ratio: 0.090655
- median_gap_ratio: 0.064516
- avg_gap_ratio_non_compliant: 0.183132
- avg_elapsed_sec: 66.735271

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 9 | 5 | 4 | 4 | 0 | 0 | 0.085563 | 55.856163 |
| general_noncontain | 10 | 7 | 3 | 3 | 0 | 0 | 0.070737 | 60.060472 |
| j_eq_k_noncontain_medium_n | 10 | 4 | 6 | 6 | 0 | 0 | 0.115155 | 83.201268 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 372 | 0.269625 | 90.352603 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 35.137206 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 92.528322 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 37 | 0.193548 | 114.631089 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 180 | 0.184211 | 90.404504 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 156 | 0.181818 | 109.229624 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 262 | 0.174888 | 80.449993 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 89 | 0.171053 | 57.256326 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 102.731751 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 60 | 0.153846 | 17.464934 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 32 | 0.142857 | 62.894922 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 72 | 0.125 | 41.581387 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 65 | 72 | 0.107692 | 7.445362 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 114.631089 | 31 | 37 | 0.193548 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 109.229624 | 132 | 156 | 0.181818 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 102.731751 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 92.528322 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 90.404504 | 152 | 180 | 0.184211 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 90.352603 | 293 | 372 | 0.269625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 80.449993 | 223 | 262 | 0.174888 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 62.894922 | 28 | 32 | 0.142857 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 57.256326 | 76 | 89 | 0.171053 | containment_s_eq_j | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 41.581387 | 64 | 72 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 35.137206 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 17.464934 | 52 | 60 | 0.153846 | general_noncontain | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 7.445362 | 65 | 72 | 0.107692 | containment_s_eq_j | quality_over_10pct |

