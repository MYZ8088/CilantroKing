# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 02:51:49
- baseline_file: `D:\ai2026.4\CilantroKing\results\coveringrepo_n_lt_26_baselines.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 29
- compliant_count: 12
- non_compliant_count: 17
- runtime_fail_count: 5
- quality_fail_count: 16
- verify_fail_count: 1
- status_timeout_count: 5
- status_error_count: 0
- elapsed_total_sec: 3081.624325

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 29 | 12 | 17 | 16 | 5 | 1 | 0.128831 | 106.262908 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 105 | 0.346154 | 119.374508 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 377 | 0.286689 | 119.661746 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 361 | 0.275618 | 119.406871 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 94 | 0.236842 | 119.38573 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 163 | 0.234848 | 119.370893 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 64 | 0.230769 | 119.388197 | general_noncontain | quality_over_10pct |
| L_16_7_6_4 | 16 | 7 | 6 | 4 | 13 | 16 | 0.230769 | 119.359297 | general_noncontain | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 187 | 0.230263 | 119.368222 | containment_s_eq_j | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 273 | 0.224215 | 119.510123 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_4 | 16 | 6 | 6 | 4 | 25 | 30 | 0.2 | 121.630937 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_6_4_3 | 16 | 6 | 4 | 3 | 16 | 19 | 0.1875 | 120.018826 | general_noncontain | timeout_over_120s;quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 33 | 0.178571 | 119.379455 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | 16 | 7 | 7 | 4 | 6 | 7 | 0.166667 | 120.755242 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_4_4_3 | 16 | 4 | 4 | 3 | 64 | 74 | 0.15625 | 119.38047 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_3_3 | 16 | 6 | 3 | 3 | 38 | 42 | 0.105263 | 119.418622 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_3 | 16 | 5 | 5 | 3 | 14 | 14 | 0.0 | 120.000565 | j_eq_k_noncontain_medium_n | timeout_over_120s |
