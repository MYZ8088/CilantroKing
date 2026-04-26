# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 03:22:43
- baseline_file: `D:\ai2026.4\CilantroKing\results\baseline_24_unsolved_cases.json`
- n_range: [13, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 4
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 24
- compliant_count: 0
- non_compliant_count: 24
- runtime_fail_count: 0
- quality_fail_count: 24
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 2745.281887

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.204918 | 116.694395 |
| 14 | 5 | 0 | 5 | 5 | 0 | 0 | 0.148773 | 118.250497 |
| 15 | 7 | 0 | 7 | 7 | 0 | 0 | 0.197196 | 118.086478 |
| 16 | 10 | 0 | 10 | 10 | 0 | 0 | 0.202468 | 109.403526 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 119.189855 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 372 | 0.269625 | 117.368445 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 99 | 0.269231 | 115.175256 | general_noncontain | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 180 | 0.267606 | 116.182614 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 225 | 0.25 | 116.045662 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 351 | 0.240283 | 115.343084 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 38 | 0.225806 | 115.213331 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 74 | 0.213115 | 116.600715 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 116.788075 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 975 | 0.19339 | 119.334707 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 181 | 0.190789 | 116.864729 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 156 | 0.181818 | 115.226393 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 263 | 0.179372 | 114.740747 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 81 | 0.173913 | 118.979403 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 588 | 0.173653 | 118.961584 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 89 | 0.171053 | 114.626582 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 119.225284 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 60 | 0.153846 | 53.262408 | general_noncontain | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 116.022522 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 32 | 0.142857 | 116.21429 | general_noncontain | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.077152 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 117.746199 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 118.881027 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 154 | 0.115942 | 119.211823 | containment_s_eq_j | quality_over_10pct |
