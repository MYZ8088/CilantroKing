# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-28 22:14:03
- source_json: `results\n14_full_current.json`

## Batch A: n<16

- total_cases: 30
- compliant_count: 20
- non_compliant_count: 10
- quality_fail_count: 10
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1385.781088
- avg_gap_ratio: 0.075081
- median_gap_ratio: 0.050126
- avg_gap_ratio_non_compliant: 0.171575
- avg_elapsed_sec: 46.192703

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 7 | 3 | 3 | 0 | 0 | 0.066757 | 67.839216 |
| general_noncontain | 10 | 7 | 3 | 3 | 0 | 0 | 0.090659 | 23.184797 |
| j_eq_k_noncontain_medium_n | 10 | 6 | 4 | 4 | 0 | 0 | 0.067826 | 47.554096 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_4_3 | L(14,7,4,3) | 6 | 8 | 0.333333 | 3.900746 | general_noncontain | quality_over_10pct |
| L_14_5_5_3 | L(14,5,5,3) | 10 | 12 | 0.2 | 20.823578 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_3 | L(14,6,4,3) | 11 | 13 | 0.181818 | 3.92768 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 588 | 0.173653 | 104.065104 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 79 | 0.144928 | 118.678702 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_4 | L(14,6,6,4) | 14 | 16 | 0.142857 | 31.801967 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 105.23464 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_4 | L(14,7,6,4) | 7 | 8 | 0.142857 | 1.633519 | general_noncontain | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 82.283484 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 154 | 0.115942 | 101.768693 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_5_5_4 | L(14,5,5,4) | 118.678702 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 105.23464 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 104.065104 | 501 | 588 | 0.173653 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 101.768693 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 82.283484 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_4 | L(14,6,6,4) | 31.801967 | 14 | 16 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_3 | L(14,5,5,3) | 20.823578 | 10 | 12 | 0.2 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_3 | L(14,6,4,3) | 3.92768 | 11 | 13 | 0.181818 | general_noncontain | quality_over_10pct |
| L_14_7_4_3 | L(14,7,4,3) | 3.900746 | 6 | 8 | 0.333333 | general_noncontain | quality_over_10pct |
| L_14_7_6_4 | L(14,7,6,4) | 1.633519 | 7 | 8 | 0.142857 | general_noncontain | quality_over_10pct |

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

