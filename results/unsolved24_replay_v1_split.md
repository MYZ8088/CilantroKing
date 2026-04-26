# Split Analysis: n<16 vs 16<=n<18

- generated_at: 2026-04-26 03:22:43
- source_json: `D:\ai2026.4\CilantroKing\results\unsolved24_replay_v1.json`

## Batch A: n<16

- total_cases: 14
- compliant_count: 0
- non_compliant_count: 14
- quality_fail_count: 14
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1651.246622
- avg_gap_ratio: 0.181005
- median_gap_ratio: 0.173783
- avg_gap_ratio_non_compliant: 0.181005
- avg_elapsed_sec: 117.946187

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 6 | 0 | 6 | 6 | 0 | 0 | 0.174029 | 119.000068 |
| general_noncontain | 2 | 0 | 2 | 2 | 0 | 0 | 0.122845 | 118.313613 |
| j_eq_k_noncontain_medium_n | 6 | 0 | 6 | 6 | 0 | 0 | 0.207369 | 116.769832 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | L(15,7,5,5) | 189 | 240 | 0.269841 | 119.189855 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 142 | 180 | 0.267606 | 116.182614 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 180 | 225 | 0.25 | 116.045662 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 61 | 74 | 0.213115 | 116.600715 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 61 | 73 | 0.196721 | 116.788075 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | 817 | 975 | 0.19339 | 119.334707 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 69 | 81 | 0.173913 | 118.979403 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 501 | 588 | 0.173653 | 118.961584 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 117 | 135 | 0.153846 | 119.225284 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 98 | 112 | 0.142857 | 116.022522 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 80 | 91 | 0.1375 | 118.077152 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 40 | 45 | 0.125 | 117.746199 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 58 | 65 | 0.12069 | 118.881027 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 138 | 154 | 0.115942 | 119.211823 | containment_s_eq_j | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_6_6 | L(15,7,6,6) | 119.334707 | 817 | 975 | 0.19339 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | L(15,6,4,4) | 119.225284 | 117 | 135 | 0.153846 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | 119.211823 | 138 | 154 | 0.115942 | containment_s_eq_j | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | 119.189855 | 189 | 240 | 0.269841 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | 118.979403 | 69 | 81 | 0.173913 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | 118.961584 | 501 | 588 | 0.173653 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | L(15,7,6,5) | 118.881027 | 58 | 65 | 0.12069 | general_noncontain | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | 118.077152 | 80 | 91 | 0.1375 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | L(15,6,5,4) | 117.746199 | 40 | 45 | 0.125 | general_noncontain | quality_over_10pct |
| L_13_7_7_6 | L(13,7,7,6) | 116.788075 | 61 | 73 | 0.196721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | 116.600715 | 61 | 74 | 0.213115 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | 116.182614 | 142 | 180 | 0.267606 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | 116.045662 | 180 | 225 | 0.25 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | 116.022522 | 98 | 112 | 0.142857 | j_eq_k_noncontain_medium_n | quality_over_10pct |

## Batch B: 16<=n<18

- total_cases: 10
- compliant_count: 0
- non_compliant_count: 10
- quality_fail_count: 10
- runtime_fail_count: 0
- verify_fail_count: 0
- elapsed_total_sec: 1094.035265
- avg_gap_ratio: 0.202468
- median_gap_ratio: 0.186304
- avg_gap_ratio_non_compliant: 0.202468
- avg_elapsed_sec: 109.403526

| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| containment_s_eq_j | 3 | 0 | 3 | 3 | 0 | 0 | 0.200708 | 115.611465 |
| general_noncontain | 3 | 0 | 3 | 3 | 0 | 0 | 0.188645 | 94.883985 |
| j_eq_k_noncontain_medium_n | 4 | 0 | 4 | 4 | 0 | 0 | 0.214155 | 115.637229 |

### worst_gap_top15

| id | params | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 293 | 372 | 0.269625 | 117.368445 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 78 | 99 | 0.269231 | 115.175256 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 283 | 351 | 0.240283 | 115.343084 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 31 | 38 | 0.225806 | 115.213331 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 152 | 181 | 0.190789 | 116.864729 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 132 | 156 | 0.181818 | 115.226393 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 223 | 263 | 0.179372 | 114.740747 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 76 | 89 | 0.171053 | 114.626582 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 52 | 60 | 0.153846 | 53.262408 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 28 | 32 | 0.142857 | 116.21429 | general_noncontain | quality_over_10pct |

### slowest_top15

| id | params | elapsed_sec | baseline | solver | gap | family | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | L(16,7,7,6) | 117.368445 | 293 | 372 | 0.269625 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | 116.864729 | 152 | 181 | 0.190789 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | 116.21429 | 28 | 32 | 0.142857 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | 115.343084 | 283 | 351 | 0.240283 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | L(16,5,5,4) | 115.226393 | 132 | 156 | 0.181818 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | 115.213331 | 31 | 38 | 0.225806 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | 115.175256 | 78 | 99 | 0.269231 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | 114.740747 | 223 | 263 | 0.179372 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | 114.626582 | 76 | 89 | 0.171053 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | 53.262408 | 52 | 60 | 0.153846 | general_noncontain | quality_over_10pct |

