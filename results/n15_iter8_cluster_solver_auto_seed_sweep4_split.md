# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 13:21:24
- source_json: `results\n15_iter8_cluster_solver_auto_seed_sweep4.json`

## Batch A: n<16

- total_cases: 14
- compliant_count: 1
- non_compliant_count: 13
- quality_fail_count: 13
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1640.881351
- avg_gap_ratio: 0.160047
- median_gap_ratio: 0.149778
- avg_gap_ratio_non_compliant: 0.164666
- avg_elapsed_sec: 117.205811

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 0 | 6 | 6 | 0 | 0 | 0.147609 | 117.624697 |
| general_noncontain | 2 | 1 | 1 | 1 | 0 | 0 | 0.101724 | 114.333328 |
| j_eq_k_noncontain_medium_n | 6 | 0 | 6 | 6 | 0 | 0 | 0.191926 | 117.744419 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 180 | 0.267606 | 119.028154 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 225 | 0.25 | 118.904844 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 225 | 0.190476 | 116.627696 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 72 | 0.180328 | 116.595718 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 72 | 0.180328 | 116.616938 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 945 | 0.156671 | 119.165494 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 115.934524 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 574 | 0.145709 | 118.949627 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 116.759467 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.320758 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 78 | 0.130435 | 118.561392 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 64 | 0.103448 | 116.75819 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 152 | 0.101449 | 116.750082 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_6_6 | L(15,7,6,6) | 119.165494 | 817 | 945 | 0.156671 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 119.028154 | 142 | 180 | 0.267606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 118.949627 | 501 | 574 | 0.145709 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 118.904844 | 180 | 225 | 0.25 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 118.561392 | 69 | 78 | 0.130435 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.320758 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 116.759467 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 116.75819 | 58 | 64 | 0.103448 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 116.750082 | 138 | 152 | 0.101449 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 116.627696 | 189 | 225 | 0.190476 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 116.616938 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 116.595718 | 61 | 72 | 0.180328 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 115.934524 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |

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

