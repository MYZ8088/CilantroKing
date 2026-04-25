# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 03:16:29
- baseline_file: `D:\ai2026.4\CilantroKing\results\coveringrepo_n_lt_26_baselines.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 29
- compliant_count: 11
- non_compliant_count: 18
- runtime_fail_count: 3
- quality_fail_count: 18
- verify_fail_count: 0
- status_timeout_count: 3
- status_error_count: 0
- elapsed_total_sec: 2695.166634

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 29 | 11 | 18 | 18 | 3 | 0 | 0.146279 | 92.93678 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 42 | 0.354839 | 122.062448 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 105 | 0.346154 | 119.41194 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 377 | 0.286689 | 119.425867 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 361 | 0.275618 | 119.443121 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 190 | 0.25 | 119.377446 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 94 | 0.236842 | 119.364731 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 64 | 0.230769 | 118.802155 | general_noncontain | quality_over_10pct |
| L_16_7_6_4 | 16 | 7 | 6 | 4 | 13 | 16 | 0.230769 | 119.211068 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 274 | 0.2287 | 119.460644 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 160 | 0.212121 | 118.413417 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_4 | 16 | 6 | 6 | 4 | 25 | 30 | 0.2 | 123.380397 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_5_4_3 | 16 | 5 | 4 | 3 | 31 | 37 | 0.193548 | 5.521002 | general_noncontain | quality_over_10pct |
| L_16_6_4_3 | 16 | 6 | 4 | 3 | 16 | 19 | 0.1875 | 119.378851 | general_noncontain | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 33 | 0.178571 | 119.373682 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | 16 | 7 | 7 | 4 | 6 | 7 | 0.166667 | 120.461971 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_5_5_3 | 16 | 5 | 5 | 3 | 14 | 16 | 0.142857 | 119.052915 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_4_4_3 | 16 | 4 | 4 | 3 | 64 | 73 | 0.140625 | 119.595028 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | 16 | 5 | 3 | 3 | 65 | 73 | 0.123077 | 0.517762 | containment_s_eq_j | quality_over_10pct |
