# n=18 all legal inputs eval (2min + 10% tolerance)

- generated_at: 2026-04-24 21:54:21
- baseline: `results/coveringrepo_n_lt_26_baselines.json`
- total_cases: 28
- compliant_cases: 4
- non_compliant_cases: 24
- verified_cases: 26
- over_120s_cases: 4
- quality_over_10pct_cases: 22

## non_compliant_cases

| id | params | baseline | solver | ratio | elapsed_sec | reasons |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| L_18_7_7_6 | L(18,7,7,6) | 654 | 946 | 1.446 | 96.65 | quality_over_10pct |
| L_18_6_5_4 | L(18,6,5,4) | 81 | 113 | 1.395 | 59.91 | quality_over_10pct |
| L_18_7_7_4 | L(18,7,7,4) | 11 | 15 | 1.364 | 66.89 | quality_over_10pct |
| L_18_5_5_4 | L(18,5,5,4) | 214 | 290 | 1.355 | 120.80 | timeout_over_120s;quality_over_10pct |
| L_18_7_4_3 | L(18,7,4,3) | 15 | 20 | 1.333 | 61.65 | quality_over_10pct |
| L_18_5_5_3 | L(18,5,5,3) | 22 | 29 | 1.318 | 128.27 | timeout_over_120s;quality_over_10pct |
| L_18_6_4_4 | L(18,6,4,4) | 236 | 305 | 1.292 | 3.18 | quality_over_10pct |
| L_18_7_3_3 | L(18,7,3,3) | 32 | 41 | 1.281 | 37.22 | quality_over_10pct |
| L_18_5_4_3 | L(18,5,4,3) | 43 | 55 | 1.279 | 56.09 | quality_over_10pct |
| L_18_7_5_5 | L(18,7,5,5) | 548 | 696 | 1.270 | 6.29 | quality_over_10pct |
| L_18_7_4_4 | L(18,7,4,4) | 126 | 160 | 1.270 | 4.25 | quality_over_10pct |
| L_18_6_6_4 | L(18,6,6,4) | 42 | 53 | 1.262 | 118.76 | quality_over_10pct |
| L_18_7_5_4 | L(18,7,5,4) | 47 | 59 | 1.255 | 101.62 | quality_over_10pct |
| L_18_4_4_3 | L(18,4,4,3) | 93 | 116 | 1.247 | 119.77 | quality_over_10pct |
| L_18_7_6_5 | L(18,7,6,5) | 174 | 213 | 1.224 | 84.99 | quality_over_10pct |
| L_18_6_6_5 | L(18,6,6,5) | 471 | 571 | 1.212 | 114.42 | quality_over_10pct |
| L_18_6_4_3 | L(18,6,4,3) | 24 | 29 | 1.208 | 96.01 | quality_over_10pct |
| L_18_7_7_5 | L(18,7,7,5) | 72 | 86 | 1.194 | 106.37 | quality_over_10pct |
| L_18_7_6_4 | L(18,7,6,4) | 24 | 28 | 1.167 | 49.37 | quality_over_10pct |
| L_18_5_3_3 | L(18,5,3,3) | 94 | 108 | 1.149 | 5.48 | quality_over_10pct |
| L_18_4_3_3 | L(18,4,3,3) | 207 | 232 | 1.121 | 1.00 | quality_over_10pct |
| L_18_5_4_4 | L(18,5,4,4) | 664 | 732 | 1.102 | 3.60 | quality_over_10pct |
| L_18_7_5_3 | L(18,7,5,3) | 8 | 0 | 0.000 | 468.66 | verification_failed;timeout_over_120s |
| L_18_6_6_3 | L(18,6,6,3) | 7 | 0 | 0.000 | 327.23 | verification_failed;timeout_over_120s |

## reason_breakdown
- quality_over_10pct: 22
- timeout_over_120s: 4
- verification_failed: 2

## family_breakdown_non_compliant
- j_eq_k_noncontain_medium_n: 9
- general_noncontain: 8
- containment_s_eq_j: 7
