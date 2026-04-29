# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-29 00:43:21
- source_json: `results\n14_full_current_v2.json`

## Batch A: n<16

- total_cases: 30
- compliant_count: 29
- non_compliant_count: 1
- quality_fail_count: 1
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 962.990745
- avg_gap_ratio: 0.030676
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: 0.130435
- avg_elapsed_sec: 32.099691

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 10 | 0 | 0 | 0 | 0 | 0.030751 | 41.356863 |
| general_noncontain | 10 | 10 | 0 | 0 | 0 | 0 | 0.033949 | 22.582204 |
| j_eq_k_noncontain_medium_n | 10 | 9 | 1 | 1 | 0 | 0 | 0.027329 | 32.360007 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 78 | 0.130435 | 118.628769 | j_eq_k_noncontain_medium_n | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_5_5_4 | L(14,5,5,4) | 118.628769 | 69 | 78 | 0.130435 | j_eq_k_noncontain_medium_n | quality_over_10pct |

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

