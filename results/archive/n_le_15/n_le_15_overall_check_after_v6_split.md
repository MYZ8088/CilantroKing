# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 20:10:22
- source_json: `D:\ai2026.4\CilantroKing\results\n_le_15_overall_check_after_v6.json`

## Batch A: n<16

- total_cases: 256
- compliant_count: 208
- non_compliant_count: 48
- quality_fail_count: 44
- runtime_fail_count: 9
- verify_fail_count: 36
- elapsed_total_sec: 41883.820142
- avg_gap_ratio: 0.008824
- median_gap_ratio: 0.0
- avg_gap_ratio_non_compliant: 0.089548
- avg_elapsed_sec: 163.608672

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 86 | 72 | 14 | 14 | 1 | 11 | 0.011139 | 238.612158 |
| general_noncontain | 84 | 66 | 18 | 14 | 6 | 12 | 0.00419 | 25.116408 |
| j_eq_k_noncontain_medium_n | 86 | 70 | 16 | 16 | 2 | 13 | 0.011017 | 223.876702 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 71 | 0.163934 | 118.661292 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 70 | 0.147541 | 118.621371 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 117.203986 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_5_4 | L(14,6,5,4) | 29 | 33 | 0.137931 | 116.418722 | general_noncontain | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 117.970077 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 560 | 0.117764 | 118.636426 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 154 | 0.115942 | 117.361729 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | 36 | 40 | 0.111111 | 117.159618 | general_noncontain | quality_over_10pct |
| L_12_6_5_4 | L(12,6,5,4) | 14 | 14 | 0.0 | 120.000157 | general_noncontain | timeout_over_120s |
| L_12_7_6_5 | L(12,7,6,5) | 16 | 16 | 0.0 | 120.000196 | general_noncontain | timeout_over_120s |
| L_13_6_5_4 | L(13,6,5,4) | 21 | 21 | 0.0 | 120.000573 | general_noncontain | timeout_over_120s |
| L_13_7_6_5 | L(13,7,6,5) | 24 | 24 | 0.0 | 120.000447 | general_noncontain | timeout_over_120s |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_12_5_5_4 | L(12,5,5,4) | 16993.684063 | 35 | None | None | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct;verification_failed |
| L_12_6_3_3 | L(12,6,3,3) | 16971.375417 | 15 | None | None | containment_s_eq_j | timeout_over_120s;quality_over_10pct;verification_failed |
| L_14_5_5_4 | L(14,5,5,4) | 125.108747 | 69 | None | None | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct;verification_failed |
| L_14_7_5_4 | L(14,7,5,4) | 125.06107 | 14 | None | None | general_noncontain | timeout_over_120s;quality_over_10pct;verification_failed |
| L_14_6_4_3 | L(14,6,4,3) | 125.059954 | 11 | None | None | general_noncontain | timeout_over_120s;quality_over_10pct;verification_failed |
| L_13_6_5_4 | L(13,6,5,4) | 120.000573 | 21 | 21 | 0.0 | general_noncontain | timeout_over_120s |
| L_13_7_6_5 | L(13,7,6,5) | 120.000447 | 24 | 24 | 0.0 | general_noncontain | timeout_over_120s |
| L_12_7_6_5 | L(12,7,6,5) | 120.000196 | 16 | 16 | 0.0 | general_noncontain | timeout_over_120s |
| L_12_6_5_4 | L(12,6,5,4) | 120.000157 | 14 | 14 | 0.0 | general_noncontain | timeout_over_120s |
| L_13_6_6_5 | L(13,6,6,5) | 118.661292 | 61 | 71 | 0.163934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 118.636426 | 501 | 560 | 0.117764 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 118.621371 | 61 | 70 | 0.147541 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 117.970077 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 117.361729 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 117.203986 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |

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

