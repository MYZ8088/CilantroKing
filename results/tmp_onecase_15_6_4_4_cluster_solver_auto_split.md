# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 00:22:03
- source_json: `results\tmp_onecase_15_6_4_4_cluster_solver_auto.json`

## Batch A: n<16

- total_cases: 1
- compliant_count: 0
- non_compliant_count: 1
- quality_fail_count: 1
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 99.409714
- avg_gap_ratio: 0.153846
- median_gap_ratio: 0.153846
- avg_gap_ratio_non_compliant: 0.153846
- avg_elapsed_sec: 99.409714

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 1 | 0 | 1 | 1 | 0 | 0 | 0.153846 | 99.409714 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 99.409714 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_4_4 | L(15,6,4,4) | 99.409714 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |

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

