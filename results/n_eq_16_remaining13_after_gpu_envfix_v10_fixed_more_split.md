# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 06:45:22
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_remaining13_after_gpu_envfix_v10_fixed_more.json`

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
- compliant_count: 3
- non_compliant_count: 10
- quality_fail_count: 10
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1245.466826
- avg_gap_ratio: 0.164293
- median_gap_ratio: 0.179372
- avg_gap_ratio_non_compliant: 0.194975
- avg_elapsed_sec: 95.80514

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 1 | 3 | 3 | 0 | 0 | 0.170319 | 83.841951 |
| general_noncontain | 3 | 0 | 3 | 3 | 0 | 0 | 0.17033 | 91.935859 |
| j_eq_k_noncontain_medium_n | 6 | 2 | 4 | 4 | 0 | 0 | 0.157257 | 105.715241 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 114.688586 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 370 | 0.262799 | 114.729031 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 114.519515 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 115.176577 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 181 | 0.190789 | 115.578914 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 156 | 0.181818 | 115.586696 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 263 | 0.179372 | 116.267999 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 88 | 0.157895 | 85.636213 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 59 | 0.134615 | 43.826068 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 31 | 0.107143 | 117.292924 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_5_4 | L(16,7,5,4) | 117.292924 | 28 | 31 | 0.107143 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 116.267999 | 223 | 263 | 0.179372 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 115.586696 | 132 | 156 | 0.181818 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 115.578914 | 152 | 181 | 0.190789 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 115.176577 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 114.729031 | 293 | 370 | 0.262799 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 114.688586 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 114.519515 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 85.636213 | 76 | 88 | 0.157895 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 43.826068 | 52 | 59 | 0.134615 | general_noncontain | quality_over_10pct |

