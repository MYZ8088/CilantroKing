# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 10:15:34
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_after_anchor_v3.json`

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
- compliant_count: 1
- non_compliant_count: 17
- quality_fail_count: 17
- runtime_fail_count: 2
- verify_fail_count: 0
- elapsed_total_sec: 1884.289856
- avg_gap_ratio: 0.215731
- median_gap_ratio: 0.22525
- avg_gap_ratio_non_compliant: 0.228421
- avg_elapsed_sec: 104.68277

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 0 | 4 | 4 | 0 | 0 | 0.221384 | 87.779161 |
| general_noncontain | 6 | 0 | 6 | 6 | 0 | 0 | 0.233838 | 98.086897 |
| j_eq_k_noncontain_medium_n | 8 | 1 | 7 | 7 | 2 | 0 | 0.199325 | 118.081479 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 42 | 0.354839 | 121.313086 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 105 | 0.346154 | 116.900841 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 379 | 0.293515 | 116.968934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 361 | 0.275618 | 116.895477 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 95 | 0.25 | 116.890882 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 188 | 0.236842 | 116.836996 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 163 | 0.234848 | 116.869202 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 64 | 0.230769 | 116.905779 | general_noncontain | quality_over_10pct |
| L_16_7_6_4 | L(16,7,6,4) | 13 | 16 | 0.230769 | 116.759555 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 272 | 0.219731 | 116.895254 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 34 | 0.214286 | 116.900232 | general_noncontain | quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | 25 | 30 | 0.2 | 118.749094 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_4_3 | L(16,5,4,3) | 31 | 37 | 0.193548 | 4.199156 | general_noncontain | quality_over_10pct |
| L_16_6_4_3 | L(16,6,4,3) | 16 | 19 | 0.1875 | 116.855821 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 120.042008 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 121.313086 | 31 | 42 | 0.354839 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 120.042008 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | 118.749094 | 25 | 30 | 0.2 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 116.968934 | 293 | 379 | 0.293515 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 116.905779 | 52 | 64 | 0.230769 | general_noncontain | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 116.900841 | 78 | 105 | 0.346154 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 116.900232 | 28 | 34 | 0.214286 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 116.895477 | 283 | 361 | 0.275618 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 116.895254 | 223 | 272 | 0.219731 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 116.890882 | 76 | 95 | 0.25 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 116.869202 | 132 | 163 | 0.234848 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 116.861422 | 64 | 72 | 0.125 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_3 | L(16,6,4,3) | 116.855821 | 16 | 19 | 0.1875 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 116.836996 | 152 | 188 | 0.236842 | containment_s_eq_j | quality_over_10pct |
| L_16_7_6_4 | L(16,7,6,4) | 116.759555 | 13 | 16 | 0.230769 | general_noncontain | quality_over_10pct |

