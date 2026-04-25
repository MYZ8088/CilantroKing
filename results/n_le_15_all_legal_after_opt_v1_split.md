# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 20:07:57
- source_json: `results/n_le_15_all_legal_after_opt_v1.json`

## Batch A: n<16

- total_cases: 306
- compliant_count: 279
- non_compliant_count: 27
- quality_fail_count: 24
- runtime_fail_count: 7
- verify_fail_count: 3
- elapsed_total_sec: 11641.075968
- avg_gap_ratio: 0.018355
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: 0.15161
- avg_elapsed_sec: 38.042732

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 90 | 82 | 8 | 8 | 2 | 2 | 0.020799 | 54.993669 |
| general_noncontain | 90 | 81 | 9 | 6 | 5 | 1 | 0.011292 | 35.283222 |
| identity_cover | 36 | 36 | 0 | 0 | 0 | 0 | 0.0 | 0.002022 |
| j_eq_k_noncontain_medium_n | 90 | 80 | 10 | 10 | 0 | 0 | 0.030293 | 39.067589 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 140 | 0.4 | 118.80237 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 119 | 0.252632 | 116.493235 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 234 | 0.238095 | 117.956648 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 175 | 0.232394 | 117.771556 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 118.659859 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 117.14091 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 588 | 0.173653 | 116.087579 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 210 | 0.166667 | 118.314272 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 953 | 0.166463 | 115.731159 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 46 | 0.15 | 117.238599 | general_noncontain | quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 20 | 23 | 0.15 | 117.882831 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 79 | 0.144928 | 118.631917 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 118.640103 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_7_5 | L(14,7,7,5) | 14 | 16 | 0.142857 | 116.41577 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.640047 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_12_7_6_5 | L(12,7,6,5) | 130.042708 | 16 | None | None | general_noncontain | timeout_over_120s;quality_over_10pct;verification_failed |
| L_13_7_5_5 | L(13,7,5,5) | 130.032436 | 78 | None | None | containment_s_eq_j | timeout_over_120s;quality_over_10pct;verification_failed |
| L_12_7_6_6 | L(12,7,6,6) | 130.025324 | 176 | None | None | containment_s_eq_j | timeout_over_120s;quality_over_10pct;verification_failed |
| L_13_7_6_5 | L(13,7,6,5) | 120.001438 | 24 | 24 | 0.0 | general_noncontain | timeout_over_120s |
| L_15_6_4_3 | L(15,6,4,3) | 120.000761 | 14 | 15 | 0.071429 | general_noncontain | timeout_over_120s |
| L_14_6_5_4 | L(14,6,5,4) | 120.000635 | 29 | 32 | 0.103448 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_15_7_6_4 | L(15,7,6,4) | 120.000536 | 9 | 9 | 0.0 | general_noncontain | timeout_over_120s |
| L_14_7_5_5 | L(14,7,5,5) | 118.814498 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |
| L_14_7_7_6 | L(14,7,7,6) | 118.80237 | 100 | 140 | 0.4 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 118.659859 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 118.640103 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.640047 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 118.631917 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 118.314272 | 180 | 210 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 117.956648 | 189 | 234 | 0.238095 | containment_s_eq_j | quality_over_10pct |

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

