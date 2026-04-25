# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 10:39:00
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_after_anchor_v5_no_cpsat.json`

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
- compliant_count: 2
- non_compliant_count: 16
- quality_fail_count: 16
- runtime_fail_count: 0
- verify_fail_count: 11
- elapsed_total_sec: 301.421988
- avg_gap_ratio: 0.113004
- median_gap_ratio: 0.123077
- avg_gap_ratio_non_compliant: 0.158206
- avg_elapsed_sec: 16.745666

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 0 | 4 | 4 | 0 | 2 | 0.156933 | 11.317919 |
| general_noncontain | 6 | 1 | 5 | 5 | 0 | 4 | 0.096774 | 12.697062 |
| j_eq_k_noncontain_medium_n | 8 | 1 | 7 | 7 | 0 | 5 | 0.094539 | 22.495992 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_5_4_3 | L(16,5,4,3) | 31 | 37 | 0.193548 | 4.244164 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 181 | 0.190789 | 44.175246 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 155 | 0.174242 | 57.848038 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | 65 | 73 | 0.123077 | 0.494972 | containment_s_eq_j | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 71 | 0.109375 | 21.266755 | j_eq_k_noncontain_medium_n | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_5_5_4 | L(16,5,5,4) | 57.848038 | 132 | 155 | 0.174242 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 44.175246 | 152 | 181 | 0.190789 | containment_s_eq_j | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 21.266755 | 64 | 71 | 0.109375 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 19.550738 | 6 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_7_5 | L(16,7,7,5) | 9.466887 | 31 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_6_4 | L(16,7,6,4) | 8.329854 | 13 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_7_6_5 | L(16,7,6,5) | 6.474017 | 78 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_6_6_4 | L(16,6,6,4) | 6.144674 | 25 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_7_5_4 | L(16,7,5,4) | 4.983517 | 28 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_5_4_3 | L(16,5,4,3) | 4.244164 | 31 | 37 | 0.193548 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 3.384171 | 293 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_6_5_4 | L(16,6,5,4) | 2.693881 | 52 | None | None | general_noncontain | quality_over_10pct;verification_failed;status_error |
| L_16_6_6_5 | L(16,6,6,5) | 1.59875 | 223 | None | None | j_eq_k_noncontain_medium_n | quality_over_10pct;verification_failed;status_error |
| L_16_5_3_3 | L(16,5,3,3) | 0.494972 | 65 | 73 | 0.123077 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 0.401044 | 76 | None | None | containment_s_eq_j | quality_over_10pct;verification_failed;status_error |

