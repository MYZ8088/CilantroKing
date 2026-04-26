# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 03:11:44
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_remaining13_after_gpu_envfix_v9_fixed774.json`

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
- elapsed_total_sec: 1350.337777
- avg_gap_ratio: 0.167892
- median_gap_ratio: 0.179372
- avg_gap_ratio_non_compliant: 0.199654
- avg_elapsed_sec: 103.872137

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 1 | 3 | 3 | 0 | 0 | 0.173608 | 95.816343 |
| general_noncontain | 3 | 0 | 3 | 3 | 0 | 0 | 0.17674 | 101.411282 |
| j_eq_k_noncontain_medium_n | 6 | 2 | 4 | 4 | 0 | 0 | 0.159658 | 110.473093 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 372 | 0.269625 | 116.30131 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 115.556886 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 116.414916 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 117.263231 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 181 | 0.190789 | 115.557301 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 157 | 0.189394 | 115.924497 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 263 | 0.179372 | 115.794511 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 89 | 0.171053 | 114.7387 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 60 | 0.153846 | 71.251566 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 31 | 0.107143 | 117.425393 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_5_4 | L(16,7,5,4) | 117.425393 | 28 | 31 | 0.107143 | general_noncontain | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 117.263231 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 116.414916 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 116.30131 | 293 | 372 | 0.269625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 115.924497 | 132 | 157 | 0.189394 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 115.794511 | 223 | 263 | 0.179372 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 115.557301 | 152 | 181 | 0.190789 | containment_s_eq_j | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 115.556886 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 114.7387 | 76 | 89 | 0.171053 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 71.251566 | 52 | 60 | 0.153846 | general_noncontain | quality_over_10pct |

