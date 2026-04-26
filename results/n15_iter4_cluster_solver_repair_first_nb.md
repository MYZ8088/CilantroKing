# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-26 00:19:17
- baseline_file: `results\n15_iter1_baseline_from_remaining.json`
- n_range: [13, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
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
- elapsed_total_sec: 1567.956329

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 2 | 0 | 2 | 2 | 0 | 0 | 0.180328 | 109.533713 |
| 14 | 5 | 0 | 5 | 5 | 0 | 0 | 0.139279 | 115.679083 |
| 15 | 7 | 0 | 7 | 7 | 0 | 0 | 0.173241 | 110.070498 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 240 | 0.269841 | 100.450958 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 180 | 0.267606 | 101.857254 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 73 | 0.196721 | 100.081059 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 586 | 0.169661 | 102.376629 | containment_s_eq_j | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 210 | 0.166667 | 102.388039 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 71 | 0.163934 | 118.986367 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 941 | 0.151775 | 108.421012 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 79 | 0.144928 | 118.990617 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 112 | 0.142857 | 119.032778 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 91 | 0.1375 | 118.99238 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 45 | 0.125 | 119.134132 | general_noncontain | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 65 | 0.12069 | 119.227527 | general_noncontain | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 130 | 0.111111 | 119.014566 | containment_s_eq_j | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 152 | 0.101449 | 119.003011 | containment_s_eq_j | quality_over_10pct |
