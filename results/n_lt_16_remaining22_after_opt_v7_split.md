# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 02:21:47
- source_json: `results/n_lt_16_remaining22_after_opt_v7.json`

## Batch A: n<16

- total_cases: 22
- compliant_count: 0
- non_compliant_count: 22
- quality_fail_count: 22
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 568.217118
- avg_gap_ratio: 0.190698
- median_gap_ratio: 0.171796
- avg_gap_ratio_non_compliant: 0.190698
- avg_elapsed_sec: 25.828051

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 0 | 10 | 10 | 0 | 0 | 0.197131 | 15.707865 |
| general_noncontain | 4 | 0 | 4 | 4 | 0 | 0 | 0.13295 | 24.340291 |
| j_eq_k_noncontain_medium_n | 8 | 0 | 8 | 8 | 0 | 0 | 0.211531 | 39.222163 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 130 | 0.3 | 57.929727 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | L(13,7,5,5) | 78 | 101 | 0.294872 | 6.35458 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 241 | 0.275132 | 12.883108 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 101 | 0.2625 | 7.163041 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 225 | 0.25 | 37.60367 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 177 | 0.246479 | 51.188792 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 115 | 0.210526 | 49.336109 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 988 | 0.209302 | 25.672983 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 26.35403 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 594 | 0.185629 | 18.484759 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 23.06969 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 114 | 0.163265 | 41.480263 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 160 | 0.15942 | 12.295453 | containment_s_eq_j | quality_over_10pct |
| L_13_6_5_5 | L(13,6,5,5) | 245 | 283 | 0.155102 | 8.682401 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 12.962509 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 57.929727 | 100 | 130 | 0.3 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 51.188792 | 142 | 177 | 0.246479 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 49.336109 | 95 | 115 | 0.210526 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 41.480263 | 98 | 114 | 0.163265 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 37.60367 | 180 | 225 | 0.25 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 32.169108 | 578 | 650 | 0.124567 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 26.81502 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 26.444185 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 26.35403 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | 25.793802 | 20 | 23 | 0.15 | general_noncontain | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 25.672983 | 817 | 988 | 0.209302 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | 25.054727 | 36 | 40 | 0.111111 | general_noncontain | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 23.06969 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_5_5 | L(14,6,5,5) | 20.410712 | 371 | 427 | 0.150943 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 20.068449 | 40 | 46 | 0.15 | general_noncontain | quality_over_10pct |

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

