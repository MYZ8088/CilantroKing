# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 12:49:41
- source_json: `results\n15_iter7_cluster_solver_auto_seed_sweep3.json`

## Batch A: n<16

- total_cases: 14
- compliant_count: 2
- non_compliant_count: 12
- quality_fail_count: 12
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1591.284488
- avg_gap_ratio: 0.159121
- median_gap_ratio: 0.144283
- avg_gap_ratio_non_compliant: 0.172322
- avg_elapsed_sec: 113.663178

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 1 | 5 | 5 | 0 | 0 | 0.146374 | 108.848313 |
| general_noncontain | 2 | 1 | 1 | 1 | 0 | 0 | 0.101724 | 115.721025 |
| j_eq_k_noncontain_medium_n | 6 | 0 | 6 | 6 | 0 | 0 | 0.190999 | 117.792094 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 118.933867 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 180 | 0.267606 | 116.692137 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 224 | 0.244444 | 118.897461 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 73 | 0.196721 | 118.936137 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 71 | 0.163934 | 116.575475 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 945 | 0.156671 | 119.072387 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 574 | 0.145709 | 118.936191 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 118.931827 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.886899 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 78 | 0.130435 | 116.719524 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 153 | 0.108696 | 116.110871 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 64 | 0.103448 | 118.604576 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_6_6 | L(15,7,6,6) | 119.072387 | 817 | 945 | 0.156671 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 118.936191 | 501 | 574 | 0.145709 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 118.936137 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 118.933867 | 189 | 240 | 0.269841 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 118.931827 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 118.897461 | 180 | 224 | 0.244444 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.886899 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 118.604576 | 58 | 64 | 0.103448 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 116.719524 | 69 | 78 | 0.130435 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 116.692137 | 142 | 180 | 0.267606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 116.575475 | 61 | 71 | 0.163934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 116.110871 | 138 | 153 | 0.108696 | containment_s_eq_j | quality_over_10pct |

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

