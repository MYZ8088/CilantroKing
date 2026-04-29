# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-28 21:50:21
- source_json: `results\n13_full_current_v3.json`

## Batch A: n<16

- total_cases: 30
- compliant_count: 30
- non_compliant_count: 0
- quality_fail_count: 0
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 587.151408
- avg_gap_ratio: 0.014939
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: None
- avg_elapsed_sec: 19.571714

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 10 | 0 | 0 | 0 | 0 | 0.028096 | 38.122567 |
| general_noncontain | 10 | 10 | 0 | 0 | 0 | 0 | 0.009524 | 11.003128 |
| j_eq_k_noncontain_medium_n | 10 | 10 | 0 | 0 | 0 | 0 | 0.007197 | 9.589445 |

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

