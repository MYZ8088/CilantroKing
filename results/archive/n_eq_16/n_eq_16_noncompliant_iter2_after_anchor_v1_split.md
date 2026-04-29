# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 09:39:54
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_after_anchor_v1.json`

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

- total_cases: 18
- compliant_count: 4
- non_compliant_count: 14
- quality_fail_count: 14
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 830.600381
- avg_gap_ratio: 0.152528
- median_gap_ratio: 0.170777
- avg_gap_ratio_non_compliant: 0.187756
- avg_elapsed_sec: 46.144466

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 0 | 4 | 4 | 0 | 0 | 0.172833 | 23.988843 |
| general_noncontain | 6 | 2 | 4 | 4 | 0 | 0 | 0.143674 | 35.044635 |
| j_eq_k_noncontain_medium_n | 8 | 2 | 6 | 6 | 0 | 0 | 0.149016 | 65.54715 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 370 | 0.262799 | 51.525032 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 98 | 0.25641 | 25.065458 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 347 | 0.226148 | 39.40642 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 99.231845 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 158 | 0.19697 | 57.695738 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_4_3 | L(16,5,4,3) | 31 | 37 | 0.193548 | 8.729853 | general_noncontain | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 62 | 0.192308 | 11.01378 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 180 | 0.184211 | 35.968023 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 262 | 0.174888 | 41.380021 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 95.322019 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 88 | 0.157895 | 19.983554 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 32 | 0.142857 | 32.561285 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 72 | 0.125 | 22.770539 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 65 | 73 | 0.123077 | 0.597375 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 99.231845 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 95.322019 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 57.695738 | 132 | 158 | 0.19697 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 51.525032 | 293 | 370 | 0.262799 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 41.380021 | 223 | 262 | 0.174888 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 39.40642 | 283 | 347 | 0.226148 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 35.968023 | 152 | 180 | 0.184211 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 32.561285 | 28 | 32 | 0.142857 | general_noncontain | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 25.065458 | 78 | 98 | 0.25641 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 22.770539 | 64 | 72 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 19.983554 | 76 | 88 | 0.157895 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 11.01378 | 52 | 62 | 0.192308 | general_noncontain | quality_over_10pct |
| L_16_5_4_3 | L(16,5,4,3) | 8.729853 | 31 | 37 | 0.193548 | general_noncontain | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 0.597375 | 65 | 73 | 0.123077 | containment_s_eq_j | quality_over_10pct |

