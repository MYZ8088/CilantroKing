# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 02:51:49
- source_json: `results\n_eq_16_after_opt_iter1.json`

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
- compliant_count: 12
- non_compliant_count: 17
- quality_fail_count: 16
- runtime_fail_count: 5
- verify_fail_count: 1
- elapsed_total_sec: 3081.624325
- avg_gap_ratio: 0.128831
- median_gap_ratio: 0.130756
- avg_gap_ratio_non_compliant: 0.205651
- avg_elapsed_sec: 106.262908

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 9 | 5 | 4 | 4 | 0 | 0 | 0.118673 | 107.426004 |
| general_noncontain | 10 | 5 | 5 | 5 | 1 | 0 | 0.127054 | 103.428014 |
| j_eq_k_noncontain_medium_n | 10 | 2 | 8 | 7 | 4 | 1 | 0.140963 | 108.051015 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 105 | 0.346154 | 119.374508 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 377 | 0.286689 | 119.661746 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 361 | 0.275618 | 119.406871 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 94 | 0.236842 | 119.38573 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 163 | 0.234848 | 119.370893 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 64 | 0.230769 | 119.388197 | general_noncontain | quality_over_10pct |
| L_16_7_6_4 | L(16,7,6,4) | 13 | 16 | 0.230769 | 119.359297 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 187 | 0.230263 | 119.368222 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 273 | 0.224215 | 119.510123 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | 25 | 30 | 0.2 | 121.630937 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_6_4_3 | L(16,6,4,3) | 16 | 19 | 0.1875 | 120.018826 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 33 | 0.178571 | 119.379455 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 120.755242 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 64 | 74 | 0.15625 | 119.38047 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_3_3 | L(16,6,3,3) | 38 | 42 | 0.105263 | 119.418622 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 125.028171 | 31 | None | None | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct;verification_failed |
| L_16_6_6_4 | L(16,6,6,4) | 121.630937 | 25 | 30 | 0.2 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 120.755242 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_6_4_3 | L(16,6,4,3) | 120.018826 | 16 | 19 | 0.1875 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_16_5_5_3 | L(16,5,5,3) | 120.000565 | 14 | 14 | 0.0 | j_eq_k_noncontain_medium_n | timeout_over_120s |
| L_16_7_7_6 | L(16,7,7,6) | 119.661746 | 293 | 377 | 0.286689 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 119.510123 | 223 | 273 | 0.224215 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_3_3 | L(16,6,3,3) | 119.418622 | 38 | 42 | 0.105263 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 119.406871 | 283 | 361 | 0.275618 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 119.388197 | 52 | 64 | 0.230769 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 119.38573 | 76 | 94 | 0.236842 | containment_s_eq_j | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 119.38047 | 64 | 74 | 0.15625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 119.379455 | 28 | 33 | 0.178571 | general_noncontain | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 119.374508 | 78 | 105 | 0.346154 | general_noncontain | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 119.370893 | 132 | 163 | 0.234848 | j_eq_k_noncontain_medium_n | quality_over_10pct |

