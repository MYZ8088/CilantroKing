# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 10:33:08
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_after_anchor_v4_no_cpsat.json`

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
- compliant_count: 4
- non_compliant_count: 14
- quality_fail_count: 14
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1021.548386
- avg_gap_ratio: 0.146266
- median_gap_ratio: 0.16886
- avg_gap_ratio_non_compliant: 0.182342
- avg_elapsed_sec: 56.752688

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 0 | 4 | 4 | 0 | 0 | 0.180417 | 33.395816 |
| general_noncontain | 6 | 2 | 4 | 4 | 0 | 0 | 0.120628 | 44.888678 |
| j_eq_k_noncontain_medium_n | 8 | 2 | 6 | 6 | 0 | 0 | 0.148419 | 77.329132 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 35.077349 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 371 | 0.266212 | 88.013207 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 350 | 0.236749 | 35.572003 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 267 | 0.197309 | 47.221916 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_4_3 | L(16,5,4,3) | 31 | 37 | 0.193548 | 7.124621 | general_noncontain | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 37 | 0.193548 | 99.949889 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 181 | 0.190789 | 72.382388 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 155 | 0.174242 | 88.863444 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 89 | 0.171053 | 24.777044 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 96.371705 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 60 | 0.153846 | 24.814131 | general_noncontain | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 65 | 73 | 0.123077 | 0.85183 | containment_s_eq_j | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 71 | 0.109375 | 35.643954 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 31 | 0.107143 | 31.267037 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 99.949889 | 31 | 37 | 0.193548 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 96.371705 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 88.863444 | 132 | 155 | 0.174242 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 88.013207 | 293 | 371 | 0.266212 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 72.382388 | 152 | 181 | 0.190789 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 47.221916 | 223 | 267 | 0.197309 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 35.643954 | 64 | 71 | 0.109375 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 35.572003 | 283 | 350 | 0.236749 | containment_s_eq_j | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 35.077349 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 31.267037 | 28 | 31 | 0.107143 | general_noncontain | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 24.814131 | 52 | 60 | 0.153846 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 24.777044 | 76 | 89 | 0.171053 | containment_s_eq_j | quality_over_10pct |
| L_16_5_4_3 | L(16,5,4,3) | 7.124621 | 31 | 37 | 0.193548 | general_noncontain | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 0.85183 | 65 | 73 | 0.123077 | containment_s_eq_j | quality_over_10pct |

