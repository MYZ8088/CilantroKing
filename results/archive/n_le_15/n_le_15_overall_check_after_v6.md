# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 20:10:22
- baseline_file: `D:\ai2026.4\CilantroKing\results\coveringrepo_n_lt_26_baselines.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 256
- compliant_count: 208
- non_compliant_count: 48
- runtime_fail_count: 9
- quality_fail_count: 44
- verify_fail_count: 36
- status_timeout_count: 9
- status_error_count: 31
- elapsed_total_sec: 41883.820142

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 7 | 16 | 16 | 0 | 0 | 0 | 0 | 0.0 | 0.021756 |
| 8 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 0.196155 |
| 9 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 1.569879 |
| 10 | 30 | 30 | 0 | 0 | 0 | 0 | 0.0 | 5.081774 |
| 11 | 30 | 30 | 0 | 0 | 0 | 0 | 0.00578 | 7.944077 |
| 12 | 30 | 26 | 4 | 2 | 4 | 2 | 0.002966 | 1202.987641 |
| 13 | 30 | 26 | 4 | 2 | 2 | 0 | 0.020603 | 87.254563 |
| 14 | 30 | 20 | 10 | 10 | 3 | 4 | 0.041031 | 90.894244 |
| 15 | 30 | 0 | 30 | 30 | 0 | 30 | None | 0.187401 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 71 | 0.163934 | 118.661292 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 70 | 0.147541 | 118.621371 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 117.203986 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_5_4 | 14 | 6 | 5 | 4 | 29 | 33 | 0.137931 | 116.418722 | general_noncontain | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 117.970077 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 560 | 0.117764 | 118.636426 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 154 | 0.115942 | 117.361729 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_5 | 14 | 7 | 6 | 5 | 36 | 40 | 0.111111 | 117.159618 | general_noncontain | quality_over_10pct |
| L_12_6_5_4 | 12 | 6 | 5 | 4 | 14 | 14 | 0.0 | 120.000157 | general_noncontain | timeout_over_120s |
| L_12_7_6_5 | 12 | 7 | 6 | 5 | 16 | 16 | 0.0 | 120.000196 | general_noncontain | timeout_over_120s |
| L_13_6_5_4 | 13 | 6 | 5 | 4 | 21 | 21 | 0.0 | 120.000573 | general_noncontain | timeout_over_120s |
| L_13_7_6_5 | 13 | 7 | 6 | 5 | 24 | 24 | 0.0 | 120.000447 | general_noncontain | timeout_over_120s |
