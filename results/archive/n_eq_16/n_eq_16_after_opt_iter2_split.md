# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 03:16:29
- source_json: `results\n_eq_16_after_opt_iter2.json`

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
- compliant_count: 11
- non_compliant_count: 18
- quality_fail_count: 18
- runtime_fail_count: 3
- verify_fail_count: 0
- elapsed_total_sec: 2695.166634
- avg_gap_ratio: 0.146279
- median_gap_ratio: 0.166667
- avg_gap_ratio_non_compliant: 0.221408
- avg_elapsed_sec: 92.93678

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 9 | 5 | 4 | 4 | 0 | 0 | 0.126921 | 79.740473 |
| general_noncontain | 10 | 4 | 6 | 6 | 0 | 0 | 0.136731 | 90.033665 |
| j_eq_k_noncontain_medium_n | 10 | 2 | 8 | 8 | 3 | 0 | 0.17325 | 107.716573 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 42 | 0.354839 | 122.062448 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 105 | 0.346154 | 119.41194 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 377 | 0.286689 | 119.425867 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 361 | 0.275618 | 119.443121 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 190 | 0.25 | 119.377446 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 94 | 0.236842 | 119.364731 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 64 | 0.230769 | 118.802155 | general_noncontain | quality_over_10pct |
| L_16_7_6_4 | L(16,7,6,4) | 13 | 16 | 0.230769 | 119.211068 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 274 | 0.2287 | 119.460644 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 160 | 0.212121 | 118.413417 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | 25 | 30 | 0.2 | 123.380397 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_5_4_3 | L(16,5,4,3) | 31 | 37 | 0.193548 | 5.521002 | general_noncontain | quality_over_10pct |
| L_16_6_4_3 | L(16,6,4,3) | 16 | 19 | 0.1875 | 119.378851 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 33 | 0.178571 | 119.373682 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 120.461971 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_6_6_4 | L(16,6,6,4) | 123.380397 | 25 | 30 | 0.2 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 122.062448 | 31 | 42 | 0.354839 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 120.461971 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 119.595028 | 64 | 73 | 0.140625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 119.460644 | 223 | 274 | 0.2287 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 119.443121 | 283 | 361 | 0.275618 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 119.425867 | 293 | 377 | 0.286689 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 119.41194 | 78 | 105 | 0.346154 | general_noncontain | quality_over_10pct |
| L_16_6_4_3 | L(16,6,4,3) | 119.378851 | 16 | 19 | 0.1875 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 119.377446 | 152 | 190 | 0.25 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 119.373682 | 28 | 33 | 0.178571 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 119.364731 | 76 | 94 | 0.236842 | containment_s_eq_j | quality_over_10pct |
| L_16_7_6_4 | L(16,7,6,4) | 119.211068 | 13 | 16 | 0.230769 | general_noncontain | quality_over_10pct |
| L_16_5_5_3 | L(16,5,5,3) | 119.052915 | 14 | 16 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 118.802155 | 52 | 64 | 0.230769 | general_noncontain | quality_over_10pct |

