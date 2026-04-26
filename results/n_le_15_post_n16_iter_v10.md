# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 06:59:50
- baseline_file: `D:\ai2026.4\CilantroKing\results\n15_iter1_baseline_from_remaining.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 125.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 14
- compliant_count: 1
- non_compliant_count: 13
- runtime_fail_count: 0
- quality_fail_count: 13
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1446.150801

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.163934 | 83.278308 |
| 14 | 5 | 0 | 5 | 5 | 0 | 0 | 0.172691 | 113.80382 |
| 15 | 7 | 1 | 6 | 6 | 0 | 0 | 0.19168 | 101.510726 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 239 | 0.26455 | 119.666377 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 177 | 0.246479 | 117.618856 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 224 | 0.244444 | 117.883092 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 99 | 0.2375 | 116.287667 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 990 | 0.21175 | 117.080718 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 597 | 0.191617 | 117.778405 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 77.404721 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 115 | 0.173469 | 117.93174 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 118.097709 | containment_s_eq_j | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 70 | 0.147541 | 89.151896 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 158 | 0.144928 | 118.747756 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 68.980882 | general_noncontain | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 77 | 0.115942 | 98.273534 | j_eq_k_noncontain_medium_n | quality_over_10pct |
