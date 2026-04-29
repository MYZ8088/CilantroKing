# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 10:15:34
- baseline_file: `D:\ai2026.4\CilantroKing\results\n_eq_16_noncompliant_iter2_baselines.json`
- n_range: [16, 17)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 18
- compliant_count: 1
- non_compliant_count: 17
- runtime_fail_count: 2
- quality_fail_count: 17
- verify_fail_count: 0
- status_timeout_count: 2
- status_error_count: 0
- elapsed_total_sec: 1884.289856

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 18 | 1 | 17 | 17 | 2 | 0 | 0.215731 | 104.68277 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_7_7_5 | 16 | 7 | 7 | 5 | 31 | 42 | 0.354839 | 121.313086 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_7_6_5 | 16 | 7 | 6 | 5 | 78 | 105 | 0.346154 | 116.900841 | general_noncontain | quality_over_10pct |
| L_16_7_7_6 | 16 | 7 | 7 | 6 | 293 | 379 | 0.293515 | 116.968934 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_5 | 16 | 7 | 5 | 5 | 283 | 361 | 0.275618 | 116.895477 | containment_s_eq_j | quality_over_10pct |
| L_16_7_4_4 | 16 | 7 | 4 | 4 | 76 | 95 | 0.25 | 116.890882 | containment_s_eq_j | quality_over_10pct |
| L_16_6_4_4 | 16 | 6 | 4 | 4 | 152 | 188 | 0.236842 | 116.836996 | containment_s_eq_j | quality_over_10pct |
| L_16_5_5_4 | 16 | 5 | 5 | 4 | 132 | 163 | 0.234848 | 116.869202 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_6_5_4 | 16 | 6 | 5 | 4 | 52 | 64 | 0.230769 | 116.905779 | general_noncontain | quality_over_10pct |
| L_16_7_6_4 | 16 | 7 | 6 | 4 | 13 | 16 | 0.230769 | 116.759555 | general_noncontain | quality_over_10pct |
| L_16_6_6_5 | 16 | 6 | 6 | 5 | 223 | 272 | 0.219731 | 116.895254 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_7_5_4 | 16 | 7 | 5 | 4 | 28 | 34 | 0.214286 | 116.900232 | general_noncontain | quality_over_10pct |
| L_16_6_6_4 | 16 | 6 | 6 | 4 | 25 | 30 | 0.2 | 118.749094 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_4_3 | 16 | 5 | 4 | 3 | 31 | 37 | 0.193548 | 4.199156 | general_noncontain | quality_over_10pct |
| L_16_6_4_3 | 16 | 6 | 4 | 3 | 16 | 19 | 0.1875 | 116.855821 | general_noncontain | quality_over_10pct |
| L_16_7_7_4 | 16 | 7 | 7 | 4 | 6 | 7 | 0.166667 | 120.042008 | j_eq_k_noncontain_medium_n | timeout_over_120s;quality_over_10pct |
| L_16_4_4_3 | 16 | 4 | 4 | 3 | 64 | 72 | 0.125 | 116.861422 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_16_5_3_3 | 16 | 5 | 3 | 3 | 65 | 73 | 0.123077 | 0.493288 | containment_s_eq_j | quality_over_10pct |
