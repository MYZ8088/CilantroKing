# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 12:49:51
- baseline_file: `D:\ai2026.4\CilantroKing\results\n_eq_16_remaining13_baseline_from_v6.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 13
- compliant_count: 4
- non_compliant_count: 9
- runtime_fail_count: 0
- quality_fail_count: 9
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1243.588849

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 13 | 4 | 9 | 9 | 0 | 0 | 0.162071 | 95.660681 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 372 | 0.269625 | 115.271443 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 99 | 0.269231 | 114.631531 | general_noncontain | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 351 | 0.240283 | 115.079265 | containment_s_eq_j | quality_over_10pct |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 38 | 0.225806 | 116.408358 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 181 | 0.190789 | 115.615131 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 156 | 0.181818 | 116.43459 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 263 | 0.179372 | 114.948794 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 88 | 0.157895 | 101.074583 | containment_s_eq_j | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 59 | 0.134615 | 50.41745 | general_noncontain | quality_over_10pct |
