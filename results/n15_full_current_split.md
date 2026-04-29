# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-29 02:33:44
- source_json: `results\n15_full_current.json`

## Batch A: n<16

- total_cases: 30
- compliant_count: 19
- non_compliant_count: 11
- quality_fail_count: 11
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1321.184879
- avg_gap_ratio: 0.079261
- median_gap_ratio: 0.077381
- avg_gap_ratio_non_compliant: 0.154691
- avg_elapsed_sec: 44.039496

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 5 | 5 | 5 | 0 | 0 | 0.112195 | 47.919162 |
| general_noncontain | 10 | 6 | 4 | 4 | 0 | 0 | 0.071275 | 26.855569 |
| j_eq_k_noncontain_medium_n | 10 | 8 | 2 | 2 | 0 | 0 | 0.054312 | 57.343757 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 113.222692 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 219 | 0.216667 | 116.750804 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 975 | 0.19339 | 109.797054 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_3 | L(15,5,5,3) | 13 | 15 | 0.153846 | 5.357768 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 96.438497 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_3 | L(15,6,5,3) | 7 | 8 | 0.142857 | 2.542893 | general_noncontain | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | 72.398408 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 75.351196 | general_noncontain | quality_over_10pct |
| L_15_7_4_3 | L(15,7,4,3) | 9 | 10 | 0.111111 | 1.304652 | general_noncontain | quality_over_10pct |
| L_15_5_3_3 | L(15,5,3,3) | 55 | 61 | 0.109091 | 0.141102 | containment_s_eq_j | quality_over_10pct |
| L_15_7_4_4 | L(15,7,4,4) | 57 | 63 | 0.105263 | 0.308125 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_7_6 | L(15,7,7,6) | 116.750804 | 180 | 219 | 0.216667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 113.222692 | 189 | 240 | 0.269841 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 109.797054 | 817 | 975 | 0.19339 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 96.438497 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 75.351196 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 72.398408 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |
| L_15_5_5_3 | L(15,5,5,3) | 5.357768 | 13 | 15 | 0.153846 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_3 | L(15,6,5,3) | 2.542893 | 7 | 8 | 0.142857 | general_noncontain | quality_over_10pct |
| L_15_7_4_3 | L(15,7,4,3) | 1.304652 | 9 | 10 | 0.111111 | general_noncontain | quality_over_10pct |
| L_15_7_4_4 | L(15,7,4,4) | 0.308125 | 57 | 63 | 0.105263 | containment_s_eq_j | quality_over_10pct |
| L_15_5_3_3 | L(15,5,3,3) | 0.141102 | 55 | 61 | 0.109091 | containment_s_eq_j | quality_over_10pct |

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

