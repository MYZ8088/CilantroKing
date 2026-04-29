# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-27 15:51:35
- source_json: `results/n_eq_16_recheck_after_restore.json`

## Batch A: n<16

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

## Batch B: 16<=n<18

- total_cases: 29
- compliant_count: 11
- non_compliant_count: 18
- quality_fail_count: 18
- runtime_fail_count: 0
- verify_fail_count: 14
- elapsed_total_sec: 1412.767053
- avg_gap_ratio: 0.05902
- median_gap_ratio: 0.032258
- avg_gap_ratio_non_compliant: 0.153267
- avg_elapsed_sec: 48.716105

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 9 | 5 | 4 | 4 | 0 | 3 | 0.055074 | 61.5529 |
| general_noncontain | 10 | 3 | 7 | 7 | 0 | 6 | 0.041718 | 41.595165 |
| j_eq_k_noncontain_medium_n | 10 | 3 | 7 | 7 | 0 | 5 | 0.077598 | 44.28393 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 180 | 0.184211 | 116.067577 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 155 | 0.174242 | 117.207161 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 59 | 0.134615 | 67.67242 | general_noncontain | quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | 25 | 28 | 0.12 | 115.99534 | j_eq_k_noncontain_medium_n | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_5_5_4 | L(16,5,5,4) | 117.207161 | 132 | 155 | 0.174242 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 116.067577 | 152 | 180 | 0.184211 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | 115.99534 | 25 | 28 | 0.12 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 67.67242 | 52 | 59 | 0.134615 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 0.277173 | 223 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_7_5 | L(16,7,7,5) | 0.237738 | 31 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_6_3 | L(16,7,6,3) | 0.228216 | 4 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_7_6_5 | L(16,7,6,5) | 0.22135 | 78 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_7_7_3 | L(16,7,7,3) | 0.215571 | 2 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_5_4 | L(16,7,5,4) | 0.215107 | 28 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_7_4_4 | L(16,7,4,4) | 0.212927 | 76 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |
| L_16_7_5_5 | L(16,7,5,5) | 0.207425 | 283 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |
| L_16_7_7_6 | L(16,7,7,6) | 0.204978 | 293 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_4_3 | L(16,7,4,3) | 0.204805 | 11 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_7_7_4 | L(16,7,7,4) | 0.204143 | 6 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |

