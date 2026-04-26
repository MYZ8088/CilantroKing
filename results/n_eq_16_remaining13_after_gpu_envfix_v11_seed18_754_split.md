# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 12:49:51
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_remaining13_after_gpu_envfix_v11_seed18_754.json`

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
- compliant_count: 4
- non_compliant_count: 9
- quality_fail_count: 9
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1243.588849
- avg_gap_ratio: 0.162071
- median_gap_ratio: 0.179372
- avg_gap_ratio_non_compliant: 0.205493
- avg_elapsed_sec: 95.660681

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 1 | 3 | 3 | 0 | 0 | 0.170319 | 88.57943 |
| general_noncontain | 3 | 1 | 2 | 2 | 0 | 0 | 0.158425 | 82.60078 |
| j_eq_k_noncontain_medium_n | 6 | 2 | 4 | 4 | 0 | 0 | 0.158395 | 106.911465 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 372 | 0.269625 | 115.271443 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 114.631531 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 115.079265 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 116.408358 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 181 | 0.190789 | 115.615131 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 156 | 0.181818 | 116.43459 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 263 | 0.179372 | 114.948794 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 88 | 0.157895 | 101.074583 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 59 | 0.134615 | 50.41745 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_5_5_4 | L(16,5,5,4) | 116.43459 | 132 | 156 | 0.181818 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 116.408358 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 115.615131 | 152 | 181 | 0.190789 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 115.271443 | 293 | 372 | 0.269625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 115.079265 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 114.948794 | 223 | 263 | 0.179372 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 114.631531 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 101.074583 | 76 | 88 | 0.157895 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 50.41745 | 52 | 59 | 0.134615 | general_noncontain | quality_over_10pct |

