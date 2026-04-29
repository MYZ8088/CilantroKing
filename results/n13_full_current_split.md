# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-28 20:15:23
- source_json: `results\n13_full_current.json`

## Batch A: n<16

- total_cases: 30
- compliant_count: 23
- non_compliant_count: 7
- quality_fail_count: 7
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 750.882905
- avg_gap_ratio: 0.042089
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: 0.122207
- avg_elapsed_sec: 25.02943

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 7 | 3 | 3 | 0 | 0 | 0.048674 | 42.853326 |
| general_noncontain | 10 | 7 | 3 | 3 | 0 | 0 | 0.037897 | 19.779018 |
| j_eq_k_noncontain_medium_n | 10 | 9 | 1 | 1 | 0 | 0 | 0.039697 | 12.455946 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_3_3 | L(13,6,3,3) | 21 | 24 | 0.142857 | 0.133393 | containment_s_eq_j | quality_over_10pct |
| L_13_6_5_4 | L(13,6,5,4) | 21 | 24 | 0.142857 | 88.977411 | general_noncontain | quality_over_10pct |
| L_13_5_4_3 | L(13,5,4,3) | 16 | 18 | 0.125 | 0.439481 | general_noncontain | quality_over_10pct |
| L_13_5_5_3 | L(13,5,5,3) | 8 | 9 | 0.125 | 0.390013 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_4_3 | L(13,6,4,3) | 9 | 10 | 0.111111 | 0.367657 | general_noncontain | quality_over_10pct |
| L_13_6_4_4 | L(13,6,4,4) | 66 | 73 | 0.106061 | 65.626409 | containment_s_eq_j | quality_over_10pct |
| L_13_4_3_3 | L(13,4,3,3) | 78 | 86 | 0.102564 | 0.445961 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_5_4 | L(13,6,5,4) | 88.977411 | 21 | 24 | 0.142857 | general_noncontain | quality_over_10pct |
| L_13_6_4_4 | L(13,6,4,4) | 65.626409 | 66 | 73 | 0.106061 | containment_s_eq_j | quality_over_10pct |
| L_13_4_3_3 | L(13,4,3,3) | 0.445961 | 78 | 86 | 0.102564 | containment_s_eq_j | quality_over_10pct |
| L_13_5_4_3 | L(13,5,4,3) | 0.439481 | 16 | 18 | 0.125 | general_noncontain | quality_over_10pct |
| L_13_5_5_3 | L(13,5,5,3) | 0.390013 | 8 | 9 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_4_3 | L(13,6,4,3) | 0.367657 | 9 | 10 | 0.111111 | general_noncontain | quality_over_10pct |
| L_13_6_3_3 | L(13,6,3,3) | 0.133393 | 21 | 24 | 0.142857 | containment_s_eq_j | quality_over_10pct |

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

