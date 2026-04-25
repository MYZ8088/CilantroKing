# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 21:43:20
- source_json: `results/tmp_onecase_14_7_5_5_after_special_v3.json`

## Batch A: n<16

- total_cases: 1
- compliant_count: 0
- non_compliant_count: 1
- quality_fail_count: 1
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 118.621581
- avg_gap_ratio: 0.115942
- median_gap_ratio: 0.115942
- avg_gap_ratio_non_compliant: 0.115942
- avg_elapsed_sec: 118.621581

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 1 | 0 | 1 | 1 | 0 | 0 | 0.115942 | 118.621581 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 154 | 0.115942 | 118.621581 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_5_5 | L(14,7,5,5) | 118.621581 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |

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

