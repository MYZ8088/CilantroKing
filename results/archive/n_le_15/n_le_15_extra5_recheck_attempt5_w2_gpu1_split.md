# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 20:36:15
- source_json: `results/n_le_15_extra5_recheck_attempt5_w2_gpu1.json`

## Batch A: n<16

- total_cases: 5
- compliant_count: 2
- non_compliant_count: 3
- quality_fail_count: 3
- runtime_fail_count: 1
- verify_fail_count: 0
- elapsed_total_sec: 584.021947
- avg_gap_ratio: 0.089578
- median_gap_ratio: 0.103448
- avg_gap_ratio_non_compliant: 0.12152
- avg_elapsed_sec: 116.804389

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| general_noncontain | 4 | 1 | 3 | 3 | 1 | 0 | 0.09114 | 117.777027 |
| j_eq_k_noncontain_medium_n | 1 | 1 | 0 | 0 | 0 | 0 | 0.083333 | 112.913838 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_4 | L(15,7,5,4) | 20 | 23 | 0.15 | 117.283974 | general_noncontain | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | 36 | 40 | 0.111111 | 116.690659 | general_noncontain | quality_over_10pct |
| L_14_6_5_4 | L(14,6,5,4) | 29 | 32 | 0.103448 | 120.00217 | general_noncontain | timeout_over_120s;quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_6_5_4 | L(14,6,5,4) | 120.00217 | 29 | 32 | 0.103448 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 117.283974 | 20 | 23 | 0.15 | general_noncontain | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | 116.690659 | 36 | 40 | 0.111111 | general_noncontain | quality_over_10pct |

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

