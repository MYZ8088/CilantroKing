# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-28 21:19:30
- source_json: `results\n13_full_current_v2.json`

## Batch A: n<16

- total_cases: 30
- compliant_count: 28
- non_compliant_count: 2
- quality_fail_count: 2
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 598.295935
- avg_gap_ratio: 0.026081
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: 0.2
- avg_elapsed_sec: 19.943198

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 10 | 0 | 0 | 0 | 0 | 0.024552 | 37.33143 |
| general_noncontain | 10 | 10 | 0 | 0 | 0 | 0 | 0.009524 | 10.930886 |
| j_eq_k_noncontain_medium_n | 10 | 8 | 2 | 2 | 0 | 0 | 0.044167 | 11.567277 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_6_4 | L(13,6,6,4) | 10 | 12 | 0.2 | 12.63093 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_5 | L(13,7,7,5) | 10 | 12 | 0.2 | 12.268682 | j_eq_k_noncontain_medium_n | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_6_4 | L(13,6,6,4) | 12.63093 | 10 | 12 | 0.2 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_5 | L(13,7,7,5) | 12.268682 | 10 | 12 | 0.2 | j_eq_k_noncontain_medium_n | quality_over_10pct |

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

