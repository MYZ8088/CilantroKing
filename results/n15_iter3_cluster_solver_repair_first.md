# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 02:58:09
- baseline_file: `D:\ai2026.4\CilantroKing\results\n15_iter3_baseline_from_remaining.json`
- n_range: [13, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 4
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 14
- compliant_count: 0
- non_compliant_count: 14
- runtime_fail_count: 0
- quality_fail_count: 14
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1650.253239

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.196721 | 117.748379 |
| 14 | 5 | 0 | 5 | 5 | 0 | 0 | 0.1289 | 118.569405 |
| 15 | 7 | 0 | 7 | 7 | 0 | 0 | 0.197036 | 117.415637 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 118.844843 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 180 | 0.267606 | 116.29575 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 225 | 0.25 | 116.750936 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 73 | 0.196721 | 118.931247 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 116.565511 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 960 | 0.175031 | 116.252271 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 119.230844 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 119.280506 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 116.756287 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 66 | 0.137931 | 115.956216 | general_noncontain | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.622935 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 118.578598 | general_noncontain | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 560 | 0.117764 | 118.96336 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 152 | 0.101449 | 119.223935 | containment_s_eq_j | quality_over_10pct |
