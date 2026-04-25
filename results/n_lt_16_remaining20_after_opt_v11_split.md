# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 09:30:10
- source_json: `results/n_lt_16_remaining20_after_opt_v11.json`

## Batch A: n<16

- total_cases: 20
- compliant_count: 0
- non_compliant_count: 20
- quality_fail_count: 20
- runtime_fail_count: 0
- verify_fail_count: 4
- elapsed_total_sec: 506.084045
- avg_gap_ratio: 0.190758
- median_gap_ratio: 0.171796
- avg_gap_ratio_non_compliant: 0.190758
- avg_elapsed_sec: 25.304202

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 0 | 10 | 10 | 0 | 2 | 0.182486 | 21.395786 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 1 | 0.15 | 17.890332 |
| j_eq_k_noncontain_medium_n | 8 | 0 | 8 | 8 | 0 | 1 | 0.206035 | 32.043191 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 130 | 0.3 | 55.868824 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | L(13,7,5,5) | 78 | 101 | 0.294872 | 13.494504 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 100 | 0.25 | 15.256999 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 177 | 0.246479 | 45.908062 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 115 | 0.210526 | 42.800049 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 20.903105 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 594 | 0.185629 | 38.877163 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 20.929227 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 114 | 0.163265 | 38.757606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_5_5 | L(13,6,5,5) | 245 | 283 | 0.155102 | 22.513489 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 20.99309 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | L(14,6,5,5) | 371 | 427 | 0.150943 | 31.963396 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 46 | 0.15 | 18.989491 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 79 | 0.144928 | 23.126727 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 158 | 0.144928 | 28.940454 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 55.868824 | 100 | 130 | 0.3 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 45.908062 | 142 | 177 | 0.246479 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 42.800049 | 95 | 115 | 0.210526 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 39.943336 | 578 | 650 | 0.124567 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 38.877163 | 501 | 594 | 0.185629 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 38.757606 | 98 | 114 | 0.163265 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_5_5 | L(14,6,5,5) | 31.963396 | 371 | 427 | 0.150943 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 28.940454 | 138 | 158 | 0.144928 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 23.126727 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_5_5 | L(13,6,5,5) | 22.513489 | 245 | 283 | 0.155102 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 20.99309 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 20.929227 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 20.903105 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 18.989491 | 40 | 46 | 0.15 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 16.791174 | 58 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |

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

