# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-27 15:32:40
- source_json: `results/n_le_16_compliance_120s_10pct_yb.json`

## Batch A: n<16

- total_cases: 256
- compliant_count: 235
- non_compliant_count: 21
- quality_fail_count: 17
- runtime_fail_count: 4
- verify_fail_count: 0
- elapsed_total_sec: 11415.852916
- avg_gap_ratio: 0.017457
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: 0.13517
- avg_elapsed_sec: 44.593175

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 86 | 81 | 5 | 5 | 0 | 0 | 0.019484 | 56.481591 |
| general_noncontain | 84 | 75 | 9 | 5 | 4 | 0 | 0.009238 | 37.042625 |
| j_eq_k_noncontain_medium_n | 86 | 79 | 7 | 7 | 0 | 0 | 0.023458 | 40.079716 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 128 | 0.28 | 117.304982 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 180 | 0.267606 | 116.02261 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 236 | 0.248677 | 118.305809 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 219 | 0.216667 | 117.44168 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 116.440776 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 72 | 0.180328 | 118.639278 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 960 | 0.175031 | 118.725616 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 20 | 23 | 0.15 | 117.709908 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 574 | 0.145709 | 117.551506 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 79 | 0.144928 | 118.625238 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 117.190519 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.650883 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | 117.988646 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 117.377367 | general_noncontain | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | 36 | 40 | 0.111111 | 119.035171 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_6_4 | L(15,7,6,4) | 120.002277 | 9 | 9 | 0.0 | general_noncontain | timeout_over_120s |
| L_15_6_4_3 | L(15,6,4,3) | 120.001298 | 14 | 14 | 0.0 | general_noncontain | timeout_over_120s |
| L_12_5_4_3 | L(12,5,4,3) | 120.000996 | 12 | 12 | 0.0 | general_noncontain | timeout_over_120s |
| L_13_5_4_3 | L(13,5,4,3) | 120.000973 | 16 | 16 | 0.0 | general_noncontain | timeout_over_120s |
| L_14_7_6_5 | L(14,7,6,5) | 119.035171 | 36 | 40 | 0.111111 | general_noncontain | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 118.725616 | 817 | 960 | 0.175031 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.650883 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 118.639278 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 118.625238 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 118.335156 | 138 | 153 | 0.108696 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 118.305809 | 189 | 236 | 0.248677 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 117.988646 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 117.709908 | 20 | 23 | 0.15 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 117.551506 | 501 | 574 | 0.145709 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 117.44168 | 180 | 219 | 0.216667 | j_eq_k_noncontain_medium_n | quality_over_10pct |

## Batch B: 16<=n<18

- total_cases: 29
- compliant_count: 0
- non_compliant_count: 29
- quality_fail_count: 29
- runtime_fail_count: 0
- verify_fail_count: 29
- elapsed_total_sec: 12.328061
- avg_gap_ratio: None
- median_gap_ratio: None
- avg_gap_ratio_non_compliant: None
- avg_elapsed_sec: 0.425106

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 9 | 0 | 9 | 9 | 0 | 9 | None | 0.460404 |
| general_noncontain | 10 | 0 | 10 | 10 | 0 | 10 | None | 0.419643 |
| j_eq_k_noncontain_medium_n | 10 | 0 | 10 | 10 | 0 | 10 | None | 0.398799 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_4_3_3 | L(16,4,3,3) | 0.63326 | 140 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |
| L_16_4_4_3 | L(16,4,4,3) | 0.6023 | 64 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_4_3 | L(16,7,4,3) | 0.598876 | 11 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_7_4_4 | L(16,7,4,4) | 0.572625 | 76 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |
| L_16_6_4_3 | L(16,6,4,3) | 0.477259 | 16 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_7_3_3 | L(16,7,3,3) | 0.476314 | 24 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |
| L_16_7_5_4 | L(16,7,5,4) | 0.471945 | 28 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_7_6_3 | L(16,7,6,3) | 0.45628 | 4 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_6_5_5 | L(16,6,5,5) | 0.437547 | 808 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |
| L_16_6_3_3 | L(16,6,3,3) | 0.435835 | 38 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |
| L_16_7_6_5 | L(16,7,6,5) | 0.431544 | 78 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_6_6_3 | L(16,6,6,3) | 0.42737 | 5 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_5_3 | L(16,7,5,3) | 0.421715 | 5 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_6_4_4 | L(16,6,4,4) | 0.417325 | 152 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |
| L_16_7_5_5 | L(16,7,5,5) | 0.415089 | 283 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |

