# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 13:21:24
- baseline_file: `results\n15_iter1_baseline_from_remaining.json`
- n_range: [13, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
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
- elapsed_total_sec: 1640.881351

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.180328 | 116.606328 |
| 14 | 5 | 0 | 5 | 5 | 0 | 0 | 0.13159 | 117.868265 |
| 15 | 7 | 1 | 6 | 6 | 0 | 0 | 0.174578 | 116.90391 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 180 | 0.267606 | 119.028154 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 225 | 0.25 | 118.904844 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 225 | 0.190476 | 116.627696 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 72 | 0.180328 | 116.595718 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 72 | 0.180328 | 116.616938 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 945 | 0.156671 | 119.165494 | containment_s_eq_j | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 135 | 0.153846 | 115.934524 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 574 | 0.145709 | 118.949627 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 116.759467 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.320758 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 78 | 0.130435 | 118.561392 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 64 | 0.103448 | 116.75819 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 152 | 0.101449 | 116.750082 | containment_s_eq_j | quality_over_10pct |
