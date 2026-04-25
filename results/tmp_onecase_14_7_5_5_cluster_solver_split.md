# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 22:33:49
- source_json: `results\tmp_onecase_14_7_5_5_cluster_solver.json`

## Batch A: n<16

- total_cases: 1
- compliant_count: 0
- non_compliant_count: 1
- quality_fail_count: 1
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 96.020749
- avg_gap_ratio: 0.115942
- median_gap_ratio: 0.115942
- avg_gap_ratio_non_compliant: 0.115942
- avg_elapsed_sec: 96.020749

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 1 | 0 | 1 | 1 | 0 | 0 | 0.115942 | 96.020749 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 154 | 0.115942 | 96.020749 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_5_5 | L(14,7,5,5) | 96.020749 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |

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

