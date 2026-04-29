# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 00:51:55
- source_json: `.\results\tmp_parallel_n7.json`

## Batch A: n<16

- total_cases: 16
- compliant_count: 16
- non_compliant_count: 0
- quality_fail_count: 0
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 3.671834
- avg_gap_ratio: 0.0
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: None
- avg_elapsed_sec: 0.22949

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 6 | 0 | 0 | 0 | 0 | 0.0 | 0.236345 |
| general_noncontain | 4 | 4 | 0 | 0 | 0 | 0 | 0.0 | 0.218611 |
| j_eq_k_noncontain_medium_n | 6 | 6 | 0 | 0 | 0 | 0 | 0.0 | 0.229886 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |

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

