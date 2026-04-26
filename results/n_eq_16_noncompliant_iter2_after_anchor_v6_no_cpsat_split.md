# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 13:43:43
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_after_anchor_v6_no_cpsat.json`

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
- compliant_count: 6
- non_compliant_count: 12
- quality_fail_count: 12
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1480.084835
- avg_gap_ratio: 0.134875
- median_gap_ratio: 0.148352
- avg_gap_ratio_non_compliant: 0.187193
- avg_elapsed_sec: 82.226935

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 0 | 4 | 4 | 0 | 0 | 0.17581 | 73.276832 |
| general_noncontain | 6 | 3 | 3 | 3 | 0 | 0 | 0.117896 | 64.125326 |
| j_eq_k_noncontain_medium_n | 8 | 3 | 5 | 5 | 0 | 0 | 0.127142 | 100.278193 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 372 | 0.269625 | 111.444948 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 39.56435 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 108.771944 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 116.121796 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 180 | 0.184211 | 94.483113 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 156 | 0.181818 | 111.578235 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 262 | 0.174888 | 95.104852 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 89 | 0.171053 | 81.70999 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 60 | 0.153846 | 22.513734 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 32 | 0.142857 | 83.111355 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 72 | 0.125 | 43.455586 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 65 | 72 | 0.107692 | 8.142282 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 116.121796 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 111.578235 | 132 | 156 | 0.181818 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 111.444948 | 293 | 372 | 0.269625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 108.771944 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 95.104852 | 223 | 262 | 0.174888 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 94.483113 | 152 | 180 | 0.184211 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 83.111355 | 28 | 32 | 0.142857 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 81.70999 | 76 | 89 | 0.171053 | containment_s_eq_j | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 43.455586 | 64 | 72 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 39.56435 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 22.513734 | 52 | 60 | 0.153846 | general_noncontain | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 8.142282 | 65 | 72 | 0.107692 | containment_s_eq_j | quality_over_10pct |

