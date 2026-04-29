# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-28 13:06:41
- source_json: `results\n12_full_current.json`

## Batch A: n<16

- total_cases: 30
- compliant_count: 27
- non_compliant_count: 3
- quality_fail_count: 3
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 915.833546
- avg_gap_ratio: 0.016657
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: 0.138889
- avg_elapsed_sec: 30.527785

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 9 | 1 | 1 | 0 | 0 | 0.018172 | 50.610671 |
| general_noncontain | 10 | 8 | 2 | 2 | 0 | 0 | 0.029167 | 8.09923 |
| j_eq_k_noncontain_medium_n | 10 | 10 | 0 | 0 | 0 | 0 | 0.002632 | 32.873453 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_12_6_4_3 | L(12,6,4,3) | 6 | 7 | 0.166667 | 0.26712 | general_noncontain | quality_over_10pct |
| L_12_7_4_4 | L(12,7,4,4) | 24 | 27 | 0.125 | 0.090875 | containment_s_eq_j | quality_over_10pct |
| L_12_7_5_4 | L(12,7,5,4) | 8 | 9 | 0.125 | 0.229733 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_12_6_4_3 | L(12,6,4,3) | 0.26712 | 6 | 7 | 0.166667 | general_noncontain | quality_over_10pct |
| L_12_7_5_4 | L(12,7,5,4) | 0.229733 | 8 | 9 | 0.125 | general_noncontain | quality_over_10pct |
| L_12_7_4_4 | L(12,7,4,4) | 0.090875 | 24 | 27 | 0.125 | containment_s_eq_j | quality_over_10pct |

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

