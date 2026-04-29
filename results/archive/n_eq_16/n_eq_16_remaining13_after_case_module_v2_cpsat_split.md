# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 22:15:26
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_remaining13_after_case_module_v2_cpsat.json`

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

- total_cases: 13
- compliant_count: 1
- non_compliant_count: 12
- quality_fail_count: 12
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1255.819738
- avg_gap_ratio: 0.182373
- median_gap_ratio: 0.181818
- avg_gap_ratio_non_compliant: 0.189878
- avg_elapsed_sec: 96.601518

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 1 | 3 | 3 | 0 | 0 | 0.171964 | 90.489912 |
| general_noncontain | 3 | 0 | 3 | 3 | 0 | 0 | 0.17674 | 87.063215 |
| j_eq_k_noncontain_medium_n | 6 | 0 | 6 | 6 | 0 | 0 | 0.192129 | 105.445074 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 372 | 0.269625 | 114.9109 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 111.565814 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 115.1712 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 115.318764 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 180 | 0.184211 | 115.710821 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 264 | 0.183857 | 117.239982 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 156 | 0.181818 | 114.590171 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 89 | 0.171053 | 115.254701 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 104.621563 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 60 | 0.153846 | 33.208491 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 72 | 0.125 | 65.989063 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 31 | 0.107143 | 116.415341 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_6_6_5 | L(16,6,6,5) | 117.239982 | 223 | 264 | 0.183857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 116.415341 | 28 | 31 | 0.107143 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 115.710821 | 152 | 180 | 0.184211 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 115.318764 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 115.254701 | 76 | 89 | 0.171053 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 115.1712 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 114.9109 | 293 | 372 | 0.269625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 114.590171 | 132 | 156 | 0.181818 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 111.565814 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 104.621563 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 65.989063 | 64 | 72 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 33.208491 | 52 | 60 | 0.153846 | general_noncontain | quality_over_10pct |

