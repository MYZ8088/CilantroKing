# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 20:28:47
- source_json: `results/n_le_15_extra13_recheck_workers2_gpu1.json`

## Batch A: n<16

- total_cases: 13
- compliant_count: 8
- non_compliant_count: 5
- quality_fail_count: 4
- runtime_fail_count: 2
- verify_fail_count: 0
- elapsed_total_sec: 1522.968816
- avg_gap_ratio: 0.050649
- median_gap_ratio: 0.042105
- avg_gap_ratio_non_compliant: 0.097912
- avg_elapsed_sec: 117.151447

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 3 | 3 | 0 | 0 | 0 | 0 | 0.042257 | 117.344531 |
| general_noncontain | 7 | 3 | 4 | 3 | 2 | 0 | 0.05208 | 117.347289 |
| j_eq_k_noncontain_medium_n | 3 | 2 | 1 | 1 | 0 | 0 | 0.055702 | 116.501401 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_4 | L(15,7,5,4) | 20 | 23 | 0.15 | 116.960636 | general_noncontain | quality_over_10pct |
| L_13_5_5_4 | L(13,5,5,4) | 48 | 54 | 0.125 | 116.189023 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | 36 | 40 | 0.111111 | 113.629628 | general_noncontain | quality_over_10pct |
| L_14_6_5_4 | L(14,6,5,4) | 29 | 32 | 0.103448 | 120.000771 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_15_6_4_3 | L(15,6,4,3) | 14 | 14 | 0.0 | 120.001955 | general_noncontain | timeout_over_120s |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_4_3 | L(15,6,4,3) | 120.001955 | 14 | 14 | 0.0 | general_noncontain | timeout_over_120s |
| L_14_6_5_4 | L(14,6,5,4) | 120.000771 | 29 | 32 | 0.103448 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 116.960636 | 20 | 23 | 0.15 | general_noncontain | quality_over_10pct |
| L_13_5_5_4 | L(13,5,5,4) | 116.189023 | 48 | 54 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | 113.629628 | 36 | 40 | 0.111111 | general_noncontain | quality_over_10pct |

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

