# n<18 compliance rerun (120s + 10% + GPU)

- generated_at: 2026-04-25 10:27:39
- baseline_file: `results/n_lt_16_remaining20_from_v10_baselines.json`
- n_range: [7, 16)
- timeout_sec: 120.0
- hard_timeout_sec: 130.0
- num_attempts: 3
- workers: 2
- CK_USE_GPU: 1

## summary

- total_cases: 20
- compliant_count: 0
- non_compliant_count: 20
- runtime_fail_count: 0
- quality_fail_count: 20
- verify_fail_count: 0
- status_timeout_count: 0
- status_error_count: 0
- elapsed_total_sec: 2377.946525

## by_n

| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 4 | 0 | 4 | 4 | 0 | 0 | 0.211891 | 117.916808 |
| 14 | 7 | 0 | 7 | 7 | 0 | 0 | 0.232368 | 118.779899 |
| 15 | 9 | 0 | 9 | 9 | 0 | 0 | 0.238942 | 119.424444 |

## non_compliant_top40_by_gap

| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_7_6 | 14 | 7 | 7 | 6 | 100 | 138 | 0.38 | 119.354302 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_5_5 | 15 | 7 | 5 | 5 | 189 | 251 | 0.328042 | 119.430572 | containment_s_eq_j | quality_over_10pct |
| L_15_6_6_5 | 15 | 6 | 6 | 5 | 142 | 187 | 0.316901 | 119.439246 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_7_6 | 15 | 7 | 7 | 6 | 180 | 235 | 0.305556 | 119.428843 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_13_7_5_5 | 13 | 7 | 5 | 5 | 78 | 101 | 0.294872 | 113.481165 | containment_s_eq_j | quality_over_10pct |
| L_14_6_4_4 | 14 | 6 | 4 | 4 | 80 | 103 | 0.2875 | 119.363566 | containment_s_eq_j | quality_over_10pct |
| L_15_5_5_4 | 15 | 5 | 5 | 4 | 95 | 119 | 0.252632 | 119.396831 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_6_6_5 | 14 | 6 | 6 | 5 | 98 | 121 | 0.234694 | 119.345199 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_6 | 15 | 7 | 6 | 6 | 817 | 996 | 0.219094 | 119.38997 | containment_s_eq_j | quality_over_10pct |
| L_13_6_6_5 | 13 | 6 | 6 | 5 | 61 | 74 | 0.213115 | 119.392075 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_7_6_5 | 15 | 7 | 6 | 5 | 58 | 70 | 0.206897 | 119.413224 | general_noncontain | quality_over_10pct |
| L_14_7_5_5 | 14 | 7 | 5 | 5 | 138 | 166 | 0.202899 | 119.372961 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_4 | 15 | 6 | 5 | 4 | 40 | 48 | 0.2 | 119.38951 | general_noncontain | quality_over_10pct |
| L_13_7_7_6 | 13 | 7 | 7 | 6 | 61 | 73 | 0.196721 | 119.419669 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_14_7_6_6 | 14 | 7 | 6 | 6 | 501 | 599 | 0.195609 | 117.635396 | containment_s_eq_j | quality_over_10pct |
| L_14_5_5_4 | 14 | 5 | 5 | 4 | 69 | 82 | 0.188406 | 119.357004 | j_eq_k_noncontain_medium_n | quality_over_10pct |
| L_15_6_4_4 | 15 | 6 | 4 | 4 | 117 | 138 | 0.179487 | 119.515774 | containment_s_eq_j | quality_over_10pct |
| L_13_6_5_5 | 13 | 6 | 5 | 5 | 245 | 280 | 0.142857 | 119.374322 | containment_s_eq_j | quality_over_10pct |
| L_15_6_5_5 | 15 | 6 | 5 | 5 | 578 | 660 | 0.141869 | 119.416029 | containment_s_eq_j | quality_over_10pct |
| L_14_6_5_5 | 14 | 6 | 5 | 5 | 371 | 422 | 0.137466 | 117.030867 | containment_s_eq_j | quality_over_10pct |
