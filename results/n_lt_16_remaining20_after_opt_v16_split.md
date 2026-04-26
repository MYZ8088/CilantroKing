# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 11:11:31
- source_json: `results/n_lt_16_remaining20_after_opt_v16.json`

## Batch A: n<16

- total_cases: 20
- compliant_count: 2
- non_compliant_count: 18
- quality_fail_count: 18
- runtime_fail_count: 1
- verify_fail_count: 0
- elapsed_total_sec: 2373.689405
- avg_gap_ratio: 0.172682
- median_gap_ratio: 0.168793
- avg_gap_ratio_non_compliant: 0.189772
- avg_elapsed_sec: 118.68447

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 10 | 2 | 8 | 8 | 1 | 0 | 0.14241 | 118.531978 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.122845 | 117.394591 |
| j_eq_k_noncontain_medium_n | 8 | 0 | 8 | 8 | 0 | 0 | 0.222981 | 119.197555 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | L(14,7,7,6) | 100 | 134 | 0.34 | 118.648239 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 181 | 0.274648 | 119.386173 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 120.001761 | containment_s_eq_j | timeout_over_120s;quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 227 | 0.261111 | 119.225486 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 1005 | 0.23011 | 117.37994 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 95 | 115 | 0.210526 | 118.944852 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 117 | 0.193878 | 119.325418 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 72 | 0.180328 | 119.365271 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 162 | 0.173913 | 118.180442 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 588 | 0.173653 | 118.262904 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 71 | 0.163934 | 119.337861 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 80 | 0.15942 | 119.34714 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 118.514473 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.992841 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 578 | 655 | 0.133218 | 118.457949 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 120.001761 | 189 | 240 | 0.269841 | containment_s_eq_j | timeout_over_120s;quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 119.386173 | 142 | 181 | 0.274648 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 119.365271 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 119.34714 | 69 | 80 | 0.15942 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 119.337861 | 61 | 71 | 0.163934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 119.325418 | 98 | 117 | 0.193878 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 119.225486 | 180 | 227 | 0.261111 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.992841 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | 118.944852 | 95 | 115 | 0.210526 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_7_6 | L(14,7,7,6) | 118.648239 | 100 | 134 | 0.34 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 118.514473 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | 118.457949 | 578 | 655 | 0.133218 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 118.262904 | 501 | 588 | 0.173653 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 118.180442 | 138 | 162 | 0.173913 | containment_s_eq_j | quality_over_10pct |
| L_13_6_5_5 | L(13,6,5,5) | 118.112749 | 245 | 273 | 0.114286 | containment_s_eq_j | quality_over_10pct |

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

