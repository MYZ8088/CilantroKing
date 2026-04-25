# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 21:38:15
- source_json: `results/n_le_15_noncompliant15_after_special_v4_w1.json`

## Batch A: n<16

- total_cases: 15
- compliant_count: 2
- non_compliant_count: 13
- quality_fail_count: 13
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1760.814942
- avg_gap_ratio: 0.145423
- median_gap_ratio: 0.144928
- avg_gap_ratio_non_compliant: 0.162537
- avg_elapsed_sec: 117.387663

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 1 | 5 | 5 | 0 | 0 | 0.146591 | 118.335908 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.122845 | 113.610962 |
| j_eq_k_noncontain_medium_n | 7 | 1 | 6 | 6 | 0 | 0 | 0.150874 | 117.653939 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 118.706458 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 180 | 0.267606 | 115.965669 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 73 | 0.196721 | 118.04973 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 210 | 0.166667 | 117.72698 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 945 | 0.156671 | 118.384325 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 70 | 0.147541 | 118.626862 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 574 | 0.145709 | 118.063161 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 79 | 0.144928 | 118.669245 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.619651 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 111 | 0.132653 | 117.264174 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | 113.616282 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 113.605642 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 152 | 0.101449 | 118.17203 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 118.706458 | 189 | 240 | 0.269841 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 118.669245 | 69 | 79 | 0.144928 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 118.626862 | 61 | 70 | 0.147541 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.619651 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 118.384325 | 817 | 945 | 0.156671 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 118.17203 | 138 | 152 | 0.101449 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 118.063161 | 501 | 574 | 0.145709 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 118.04973 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 117.72698 | 180 | 210 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 117.264174 | 98 | 111 | 0.132653 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 115.965669 | 142 | 180 | 0.267606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 113.616282 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 113.605642 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |

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

