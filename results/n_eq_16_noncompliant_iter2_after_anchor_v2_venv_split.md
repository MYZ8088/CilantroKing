# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-25 09:57:47
- source_json: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_after_anchor_v2_venv.json`

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
- runtime_fail_count: 1
- verify_fail_count: 0
- elapsed_total_sec: 1879.110625
- avg_gap_ratio: 0.218293
- median_gap_ratio: 0.230516
- avg_gap_ratio_non_compliant: 0.231134
- avg_elapsed_sec: 104.395035

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 4 | 0 | 4 | 4 | 0 | 0 | 0.21974 | 87.819099 |
| general_noncontain | 6 | 0 | 6 | 6 | 0 | 0 | 0.244254 | 98.26331 |
| j_eq_k_noncontain_medium_n | 8 | 1 | 7 | 7 | 1 | 0 | 0.198099 | 117.281796 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 105 | 0.346154 | 116.87561 | general_noncontain | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 41 | 0.322581 | 120.533059 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 381 | 0.300341 | 117.007448 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 361 | 0.275618 | 116.913008 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_3 | L(16,6,4,3) | 16 | 20 | 0.25 | 116.311944 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 95 | 0.25 | 116.950283 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 163 | 0.234848 | 116.878552 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 64 | 0.230769 | 116.95996 | general_noncontain | quality_over_10pct |
| L_16_7_6_4 | L(16,7,6,4) | 13 | 16 | 0.230769 | 117.969872 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 187 | 0.230263 | 116.882335 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 272 | 0.219731 | 117.128635 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 34 | 0.214286 | 116.894452 | general_noncontain | quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | 25 | 30 | 0.2 | 118.903517 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_4_3 | L(16,5,4,3) | 31 | 37 | 0.193548 | 4.568022 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 6 | 7 | 0.166667 | 116.791054 | j_eq_k_noncontain_medium_n | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | L(16,7,7,5) | 120.533059 | 31 | 41 | 0.322581 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | 118.903517 | 25 | 30 | 0.2 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_4 | L(16,7,6,4) | 117.969872 | 13 | 16 | 0.230769 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 117.128635 | 223 | 272 | 0.219731 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | 117.007448 | 293 | 381 | 0.300341 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 116.95996 | 52 | 64 | 0.230769 | general_noncontain | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 116.950283 | 76 | 95 | 0.25 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 116.913008 | 283 | 361 | 0.275618 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 116.894452 | 28 | 34 | 0.214286 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 116.882335 | 152 | 187 | 0.230263 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 116.878552 | 132 | 163 | 0.234848 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 116.87561 | 78 | 105 | 0.346154 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | 116.791054 | 6 | 7 | 0.166667 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_3 | L(16,6,4,3) | 116.311944 | 16 | 20 | 0.25 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | L(16,4,4,3) | 114.083336 | 64 | 73 | 0.140625 | j_eq_k_noncontain_medium_n | quality_over_10pct |

