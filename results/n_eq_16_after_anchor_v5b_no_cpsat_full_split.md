# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 12:54:52
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_after_anchor_v5b_no_cpsat_full.json`

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

- total_cases: 29
- compliant_count: 16
- non_compliant_count: 13
- quality_fail_count: 13
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 2168.157147
- avg_gap_ratio: 0.089115
- median_gap_ratio: 0.064356
- avg_gap_ratio_non_compliant: 0.185614
- avg_elapsed_sec: 74.76404

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 9 | 5 | 4 | 4 | 0 | 0 | 0.085563 | 66.702257 |
| general_noncontain | 10 | 7 | 3 | 3 | 0 | 0 | 0.063045 | 64.857438 |
| j_eq_k_noncontain_medium_n | 10 | 4 | 6 | 6 | 0 | 0 | 0.11838 | 91.926245 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 372 | 0.269625 | 112.39676 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 49.19874 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 111.65898 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 114.011436 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 180 | 0.184211 | 94.065755 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 156 | 0.181818 | 112.084971 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 262 | 0.174888 | 101.996682 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 89 | 0.171053 | 82.002268 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 105.921386 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 60 | 0.153846 | 20.358073 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 32 | 0.142857 | 86.351687 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 72 | 0.125 | 42.940697 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 65 | 72 | 0.107692 | 7.090883 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 114.011436 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 112.39676 | 293 | 372 | 0.269625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 112.084971 | 132 | 156 | 0.181818 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 111.65898 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 105.921386 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 101.996682 | 223 | 262 | 0.174888 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 94.065755 | 152 | 180 | 0.184211 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 86.351687 | 28 | 32 | 0.142857 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 82.002268 | 76 | 89 | 0.171053 | containment_s_eq_j | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 49.19874 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 42.940697 | 64 | 72 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 20.358073 | 52 | 60 | 0.153846 | general_noncontain | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 7.090883 | 65 | 72 | 0.107692 | containment_s_eq_j | quality_over_10pct |

