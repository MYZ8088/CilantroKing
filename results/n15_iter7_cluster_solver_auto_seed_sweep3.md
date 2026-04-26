# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 12:49:41
- baseline_file: `results\n15_iter1_baseline_from_remaining.json`
- n_range: [13, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 1
- CK_USE_GPU: 1

## summary

- total_cases: 14
- compliant_count: 2
- non_compliant_count: 12
- runtime_fail_count: 0
- quality_fail_count: 12
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 1591.284488

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.180328 | 117.755806 |
| 14 | 5 | 0 | 5 | 5 | 0 | 0 | 0.133039 | 117.917062 |
| 15 | 7 | 2 | 5 | 5 | 0 | 0 | 0.171691 | 109.455366 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 118.933867 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 180 | 0.267606 | 116.692137 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 224 | 0.244444 | 118.897461 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 73 | 0.196721 | 118.936137 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 71 | 0.163934 | 116.575475 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 945 | 0.156671 | 119.072387 | containment_s_eq_j | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 574 | 0.145709 | 118.936191 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 118.931827 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.886899 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 78 | 0.130435 | 116.719524 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 153 | 0.108696 | 116.110871 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 64 | 0.103448 | 118.604576 | general_noncontain | quality_over_10pct |
