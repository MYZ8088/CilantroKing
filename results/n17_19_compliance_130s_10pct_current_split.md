# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-28 15:28:54
- source_json: `D:\ai2026.4\CilantroKing\results\n17_19_compliance_130s_10pct_current.json`

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

- total_cases: 28
- compliant_count: 3
- non_compliant_count: 25
- quality_fail_count: 25
- runtime_fail_count: 2
- verify_fail_count: 2
- elapsed_total_sec: 1056.753034
- avg_gap_ratio: 0.236686
- median_gap_ratio: 0.25463
- avg_gap_ratio_non_compliant: 0.267558
- avg_elapsed_sec: 37.74118

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 8 | 1 | 7 | 7 | 0 | 0 | 0.229633 | 3.103814 |
| general_noncontain | 10 | 1 | 9 | 9 | 1 | 1 | 0.246343 | 30.921598 |
| j_eq_k_noncontain_medium_n | 10 | 1 | 9 | 9 | 1 | 1 | 0.233298 | 72.270654 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_17_7_7_6 | L(17,7,7,6) | 444 | 608 | 0.369369 | 43.518127 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_6_5_3 | L(17,6,5,3) | 11 | 15 | 0.363636 | 20.39472 | general_noncontain | quality_over_10pct |
| L_17_6_5_4 | L(17,6,5,4) | 66 | 89 | 0.348485 | 17.683415 | general_noncontain | quality_over_10pct |
| L_17_5_5_3 | L(17,5,5,3) | 18 | 24 | 0.333333 | 69.101304 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_5_3_3 | L(17,5,3,3) | 68 | 90 | 0.323529 | 1.43634 | containment_s_eq_j | quality_over_10pct |
| L_17_6_4_4 | L(17,6,4,4) | 188 | 243 | 0.292553 | 1.685735 | containment_s_eq_j | quality_over_10pct |
| L_17_7_6_5 | L(17,7,6,5) | 115 | 148 | 0.286957 | 7.778206 | general_noncontain | quality_over_10pct |
| L_17_7_4_4 | L(17,7,4,4) | 98 | 126 | 0.285714 | 1.270058 | containment_s_eq_j | quality_over_10pct |
| L_17_7_5_5 | L(17,7,5,5) | 398 | 510 | 0.281407 | 1.779258 | containment_s_eq_j | quality_over_10pct |
| L_17_7_6_4 | L(17,7,6,4) | 18 | 23 | 0.277778 | 45.797336 | general_noncontain | quality_over_10pct |
| L_17_6_6_4 | L(17,6,6,4) | 33 | 42 | 0.272727 | 56.504236 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_5_5_4 | L(17,5,5,4) | 175 | 221 | 0.262857 | 51.726716 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_7_3_3 | L(17,7,3,3) | 27 | 34 | 0.259259 | 6.238424 | containment_s_eq_j | quality_over_10pct |
| L_17_6_3_3 | L(17,6,3,3) | 44 | 55 | 0.25 | 7.362414 | containment_s_eq_j | quality_over_10pct |
| L_17_6_4_3 | L(17,6,4,3) | 20 | 25 | 0.25 | 14.308897 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_17_7_7_3 | L(17,7,7,3) | 135.124291 | 3 | None | None | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct;verification_failed |
| L_17_7_6_3 | L(17,7,6,3) | 135.08847 | 4 | None | None | general_noncontain | timeout_over_120s;quality_over_10pct;verification_failed |
| L_17_7_7_4 | L(17,7,7,4) | 116.708028 | 9 | 11 | 0.222222 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_4_4_3 | L(17,4,4,3) | 89.465051 | 77 | 92 | 0.194805 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_7_7_5 | L(17,7,7,5) | 85.995214 | 49 | 60 | 0.22449 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_5_5_3 | L(17,5,5,3) | 69.101304 | 18 | 24 | 0.333333 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_6_6_4 | L(17,6,6,4) | 56.504236 | 33 | 42 | 0.272727 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_5_5_4 | L(17,5,5,4) | 51.726716 | 175 | 221 | 0.262857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_7_6_4 | L(17,7,6,4) | 45.797336 | 18 | 23 | 0.277778 | general_noncontain | quality_over_10pct |
| L_17_7_7_6 | L(17,7,7,6) | 43.518127 | 444 | 608 | 0.369369 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_6_6_5 | L(17,6,6,5) | 24.63214 | 332 | 405 | 0.21988 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_17_7_5_4 | L(17,7,5,4) | 21.174238 | 37 | 45 | 0.216216 | general_noncontain | quality_over_10pct |
| L_17_6_5_3 | L(17,6,5,3) | 20.39472 | 11 | 15 | 0.363636 | general_noncontain | quality_over_10pct |
| L_17_6_5_4 | L(17,6,5,4) | 17.683415 | 66 | 89 | 0.348485 | general_noncontain | quality_over_10pct |
| L_17_6_4_3 | L(17,6,4,3) | 14.308897 | 20 | 25 | 0.25 | general_noncontain | quality_over_10pct |

