# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 10:57:19
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_after_anchor_v5b_no_cpsat.json`

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

- total_cases: 18
- compliant_count: 5
- non_compliant_count: 13
- quality_fail_count: 13
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1637.531348
- avg_gap_ratio: 0.144621
- median_gap_ratio: 0.160257
- avg_gap_ratio_non_compliant: 0.183211
- avg_elapsed_sec: 90.973964

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 0 | 4 | 4 | 0 | 0 | 0.17581 | 87.026255 |
| general_noncontain | 6 | 3 | 3 | 3 | 0 | 0 | 0.111943 | 76.952824 |
| j_eq_k_noncontain_medium_n | 8 | 2 | 6 | 6 | 0 | 0 | 0.153536 | 103.463673 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 372 | 0.269625 | 115.241558 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 77.225146 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 117.177821 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 118.234399 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 180 | 0.184211 | 110.086237 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 156 | 0.181818 | 115.822665 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 263 | 0.179372 | 118.443077 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 89 | 0.171053 | 115.040293 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 112.260174 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 60 | 0.153846 | 30.389979 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 72 | 0.125 | 29.655814 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 65 | 72 | 0.107692 | 5.800668 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 31 | 0.107143 | 115.899993 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_6_6_5 | L(16,6,6,5) | 118.443077 | 223 | 263 | 0.179372 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 118.234399 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 117.177821 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 115.899993 | 28 | 31 | 0.107143 | general_noncontain | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 115.822665 | 132 | 156 | 0.181818 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 115.241558 | 293 | 372 | 0.269625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 115.040293 | 76 | 89 | 0.171053 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 112.260174 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 110.086237 | 152 | 180 | 0.184211 | containment_s_eq_j | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 77.225146 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 30.389979 | 52 | 60 | 0.153846 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 29.655814 | 64 | 72 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 5.800668 | 65 | 72 | 0.107692 | containment_s_eq_j | quality_over_10pct |

