# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 10:57:19
- baseline_file: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_baselines.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 18
- compliant_count: 5
- non_compliant_count: 13
- runtime_fail_count: 0
- quality_fail_count: 13
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1637.531348

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 18 | 5 | 13 | 13 | 0 | 0 | 0.144621 | 90.973964 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 372 | 0.269625 | 115.241558 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 99 | 0.269231 | 77.225146 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 351 | 0.240283 | 117.177821 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 38 | 0.225806 | 118.234399 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 180 | 0.184211 | 110.086237 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 156 | 0.181818 | 115.822665 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 263 | 0.179372 | 118.443077 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 89 | 0.171053 | 115.040293 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_4 | 16 | 7 | 7 | 4 | 6 | 7 | 0.166667 | 112.260174 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 60 | 0.153846 | 30.389979 | general_noncontain | quality_over_10pct |
| L_16_4_4_3 | 16 | 4 | 4 | 3 | 64 | 72 | 0.125 | 29.655814 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | 16 | 5 | 3 | 3 | 65 | 72 | 0.107692 | 5.800668 | containment_s_eq_j | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 31 | 0.107143 | 115.899993 | general_noncontain | quality_over_10pct |
