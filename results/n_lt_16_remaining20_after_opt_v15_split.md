# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 10:27:39
- source_json: `results/n_lt_16_remaining20_after_opt_v15.json`

## Batch A: n<16

- total_cases: 20
- compliant_count: 0
- non_compliant_count: 20
- quality_fail_count: 20
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 2377.946525
- avg_gap_ratio: 0.231231
- median_gap_ratio: 0.210006
- avg_gap_ratio_non_compliant: 0.231231
- avg_elapsed_sec: 118.897326

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 0 | 10 | 10 | 0 | 0 | 0.21297 | 118.401062 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.203449 | 119.401367 |
| j_eq_k_noncontain_medium_n | 8 | 0 | 8 | 8 | 0 | 0 | 0.261003 | 119.391646 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 138 | 0.38 | 119.354302 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 251 | 0.328042 | 119.430572 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 187 | 0.316901 | 119.439246 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 235 | 0.305556 | 119.428843 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | L(13,7,5,5) | 78 | 101 | 0.294872 | 113.481165 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 103 | 0.2875 | 119.363566 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 119 | 0.252632 | 119.396831 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 121 | 0.234694 | 119.345199 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 996 | 0.219094 | 119.38997 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 74 | 0.213115 | 119.392075 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 70 | 0.206897 | 119.413224 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 166 | 0.202899 | 119.372961 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 48 | 0.2 | 119.38951 | general_noncontain | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 119.419669 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 599 | 0.195609 | 117.635396 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_4_4 | L(15,6,4,4) | 119.515774 | 117 | 138 | 0.179487 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 119.439246 | 142 | 187 | 0.316901 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 119.430572 | 189 | 251 | 0.328042 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 119.428843 | 180 | 235 | 0.305556 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 119.419669 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 119.416029 | 578 | 660 | 0.141869 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 119.413224 | 58 | 70 | 0.206897 | general_noncontain | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 119.396831 | 95 | 119 | 0.252632 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 119.392075 | 61 | 74 | 0.213115 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 119.38997 | 817 | 996 | 0.219094 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 119.38951 | 40 | 48 | 0.2 | general_noncontain | quality_over_10pct |
| L_13_6_5_5 | L(13,6,5,5) | 119.374322 | 245 | 280 | 0.142857 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 119.372961 | 138 | 166 | 0.202899 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 119.363566 | 80 | 103 | 0.2875 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 119.357004 | 69 | 82 | 0.188406 | j_eq_k_noncontain_medium_n | quality_over_10pct |

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

