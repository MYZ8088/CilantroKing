# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 05:57:55
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
- elapsed_total_sec: 1635.369559

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.204918 | 116.581462 |
| 14 | 5 | 1 | 4 | 4 | 0 | 0 | 0.135938 | 116.696956 |
| 15 | 7 | 1 | 6 | 6 | 0 | 0 | 0.183891 | 116.960265 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 118.930532 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 179 | 0.260563 | 118.986314 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 225 | 0.25 | 116.826949 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 74 | 0.213115 | 116.584529 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 73 | 0.196721 | 116.578394 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 960 | 0.175031 | 118.94436 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 80 | 0.15942 | 118.928573 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 574 | 0.145709 | 118.965875 | containment_s_eq_j | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 116.766461 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 116.746387 | containment_s_eq_j | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 116.015048 | general_noncontain | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 130 | 0.111111 | 116.72821 | containment_s_eq_j | quality_over_10pct |
