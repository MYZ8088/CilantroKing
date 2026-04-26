# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 13:52:06
- source_json: `results\n15_iter9_cluster_solver_auto_seedbank.json`

## Batch A: n<16

- total_cases: 14
- compliant_count: 3
- non_compliant_count: 11
- quality_fail_count: 11
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1302.337971
- avg_gap_ratio: 0.164471
- median_gap_ratio: 0.161677
- avg_gap_ratio_non_compliant: 0.185456
- avg_elapsed_sec: 93.024141

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 2 | 4 | 4 | 0 | 0 | 0.153101 | 79.419072 |
| general_noncontain | 2 | 1 | 1 | 1 | 0 | 0 | 0.101724 | 59.505431 |
| j_eq_k_noncontain_medium_n | 6 | 0 | 6 | 6 | 0 | 0 | 0.196756 | 117.802114 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 119.00892 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 180 | 0.267606 | 118.97302 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 225 | 0.25 | 116.774913 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 73 | 0.196721 | 116.518545 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 960 | 0.175031 | 118.951923 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 588 | 0.173653 | 119.54844 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 71 | 0.163934 | 118.942836 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 80 | 0.15942 | 118.936481 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 116.666886 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.934477 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 64 | 0.103448 | 118.610512 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_6_6 | L(14,7,6,6) | 119.54844 | 501 | 588 | 0.173653 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 119.00892 | 189 | 240 | 0.269841 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 118.97302 | 142 | 180 | 0.267606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 118.951923 | 817 | 960 | 0.175031 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 118.942836 | 61 | 71 | 0.163934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 118.936481 | 69 | 80 | 0.15942 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.934477 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 118.610512 | 58 | 64 | 0.103448 | general_noncontain | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 116.774913 | 180 | 225 | 0.25 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 116.666886 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 116.518545 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |

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

