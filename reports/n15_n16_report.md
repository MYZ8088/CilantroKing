# n=15 and n=16 Time and Accuracy Report

## Run Summary

- Date: 2026-04-29
- Scope: all baseline cases with `n in {15, 16}` from `coveringrepo_n_lt_26_baselines(1).json`
- Validation mode: full verification, no sampling
- Per-case solver time limit passed to validator: `120s`
- Parallel workers used for this batch: `3`
- Total cases: `59` (`n=15`: `30`, `n=16`: `29`)
- Fully verified cases: `59 / 59`
- Cases at or below ratio `1.21`: `46 / 59`
- Worst ratio: `L_16_7_7_5` with ratio `1.3548` (35.48% over baseline)
- Slowest case: `L_15_7_5_3` in `1503.231s`

Accuracy in this report is shown as:

- `ratio = groups / baseline_blocks`
- `error% = (ratio - 1) * 100`

## Cases Above Ratio 1.21

| id | baseline | groups | ratio | error% | time(s) |
| --- | ---: | ---: | ---: | ---: | ---: |
| L_15_7_6_6 | 817 | 1019 | 1.2472 | 24.72% | 128.488 |
| L_15_5_5_4 | 95 | 122 | 1.2842 | 28.42% | 120.037 |
| L_15_7_7_6 | 180 | 238 | 1.3222 | 32.22% | 122.969 |
| L_15_6_6_5 | 142 | 190 | 1.3380 | 33.80% | 121.650 |
| L_16_7_6_4 | 13 | 16 | 1.2308 | 23.08% | 121.032 |
| L_16_6_4_3 | 16 | 20 | 1.2500 | 25.00% | 77.672 |
| L_16_7_4_4 | 76 | 95 | 1.2500 | 25.00% | 120.623 |
| L_16_6_6_5 | 223 | 280 | 1.2556 | 25.56% | 128.933 |
| L_16_6_4_4 | 152 | 192 | 1.2632 | 26.32% | 121.508 |
| L_16_5_5_4 | 132 | 168 | 1.2727 | 27.27% | 120.795 |
| L_16_7_7_6 | 293 | 384 | 1.3106 | 31.06% | 145.976 |
| L_16_7_6_5 | 78 | 104 | 1.3333 | 33.33% | 123.711 |
| L_16_7_7_5 | 31 | 42 | 1.3548 | 35.48% | 124.479 |

## n=15 Detailed Results

| id | (k,j,s) | baseline | groups | ratio | error% | time(s) | verified | strategy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_4_3_3 | (4,3,3) | 124 | 131 | 1.0565 | 5.65% | 109.655 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_4_4_3 | (4,4,3) | 52 | 61 | 1.1731 | 17.31% | 105.228 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_5_3_3 | (5,3,3) | 55 | 60 | 1.0909 | 9.09% | 109.567 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_5_4_3 | (5,4,3) | 24 | 27 | 1.1250 | 12.50% | 103.548 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_5_4_4 | (5,4,4) | 294 | 303 | 1.0306 | 3.06% | 120.671 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_5_5_3 | (5,5,3) | 13 | 13 | 1.0000 | 0.00% | 144.657 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_5_5_4 | (5,5,4) | 95 | 122 | 1.2842 | 28.42% | 120.037 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_3_3 | (6,3,3) | 31 | 32 | 1.0323 | 3.23% | 110.681 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_4_3 | (6,4,3) | 14 | 15 | 1.0714 | 7.14% | 130.930 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_4_4 | (6,4,4) | 117 | 140 | 1.1966 | 19.66% | 120.146 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_5_3 | (6,5,3) | 7 | 7 | 1.0000 | 0.00% | 474.777 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_5_4 | (6,5,4) | 40 | 48 | 1.2000 | 20.00% | 120.027 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_5_5 | (6,5,5) | 578 | 667 | 1.1540 | 15.40% | 123.535 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_6_3 | (6,6,3) | 4 | 4 | 1.0000 | 0.00% | 49.309 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_6_4 | (6,6,4) | 19 | 21 | 1.1053 | 10.53% | 120.096 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_6_6_5 | (6,6,5) | 142 | 190 | 1.3380 | 33.80% | 121.650 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_3_3 | (7,3,3) | 15 | 15 | 1.0000 | 0.00% | 26.200 | true | n=15:bitmask-greedy-bound |
| L_15_7_4_3 | (7,4,3) | 9 | 9 | 1.0000 | 0.00% | 285.391 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_4_4 | (7,4,4) | 57 | 63 | 1.1053 | 10.53% | 120.208 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_5_3 | (7,5,3) | 5 | 5 | 1.0000 | 0.00% | 1503.231 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_5_4 | (7,5,4) | 20 | 24 | 1.2000 | 20.00% | 250.209 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_5_5 | (7,5,5) | 189 | 228 | 1.2063 | 20.63% | 121.546 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_6_3 | (7,6,3) | 2 | 2 | 1.0000 | 0.00% | 0.199 | true | n=15:bitmask-greedy-bound |
| L_15_7_6_4 | (7,6,4) | 9 | 9 | 1.0000 | 0.00% | 111.799 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_6_5 | (7,6,5) | 58 | 70 | 1.2069 | 20.69% | 120.568 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_6_6 | (7,6,6) | 817 | 1019 | 1.2472 | 24.72% | 128.488 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_7_3 | (7,7,3) | 2 | 2 | 1.0000 | 0.00% | 0.215 | true | n=15:bitmask-greedy-bound |
| L_15_7_7_4 | (7,7,4) | 5 | 5 | 1.0000 | 0.00% | 80.373 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_7_5 | (7,7,5) | 24 | 28 | 1.1667 | 16.67% | 120.573 | true | n=15:bitmask-random-greedy-lns-ilp |
| L_15_7_7_6 | (7,7,6) | 180 | 238 | 1.3222 | 32.22% | 122.969 | true | n=15:bitmask-random-greedy-lns-ilp |

## n=16 Detailed Results

| id | (k,j,s) | baseline | groups | ratio | error% | time(s) | verified | strategy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_16_4_3_3 | (4,3,3) | 140 | 140 | 1.0000 | 0.00% | 28.913 | true | n=16:bitmask-greedy-bound |
| L_16_4_4_3 | (4,4,3) | 64 | 74 | 1.1562 | 15.62% | 73.995 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_5_3_3 | (5,3,3) | 65 | 73 | 1.1231 | 12.31% | 104.853 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_5_4_3 | (5,4,3) | 31 | 35 | 1.1290 | 12.90% | 72.050 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_5_4_4 | (5,4,4) | 404 | 434 | 1.0743 | 7.43% | 121.122 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_5_5_3 | (5,5,3) | 14 | 14 | 1.0000 | 0.00% | 91.248 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_5_5_4 | (5,5,4) | 132 | 168 | 1.2727 | 27.27% | 120.795 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_3_3 | (6,3,3) | 38 | 41 | 1.0789 | 7.89% | 119.198 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_4_3 | (6,4,3) | 16 | 20 | 1.2500 | 25.00% | 77.672 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_4_4 | (6,4,4) | 152 | 192 | 1.2632 | 26.32% | 121.508 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_5_3 | (6,5,3) | 8 | 8 | 1.0000 | 0.00% | 92.706 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_5_4 | (6,5,4) | 52 | 60 | 1.1538 | 15.38% | 120.137 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_5_5 | (6,5,5) | 808 | 840 | 1.0396 | 3.96% | 126.884 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_6_3 | (6,6,3) | 5 | 5 | 1.0000 | 0.00% | 84.135 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_6_4 | (6,6,4) | 25 | 30 | 1.2000 | 20.00% | 121.421 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_6_6_5 | (6,6,5) | 223 | 280 | 1.2556 | 25.56% | 128.933 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_3_3 | (7,3,3) | 24 | 25 | 1.0417 | 4.17% | 109.415 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_4_3 | (7,4,3) | 11 | 11 | 1.0000 | 0.00% | 75.622 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_4_4 | (7,4,4) | 76 | 95 | 1.2500 | 25.00% | 120.623 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_5_3 | (7,5,3) | 5 | 5 | 1.0000 | 0.00% | 80.694 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_5_4 | (7,5,4) | 28 | 32 | 1.1429 | 14.29% | 120.016 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_5_5 | (7,5,5) | 283 | 328 | 1.1590 | 15.90% | 21.809 | true | n=16:partial-orbit-ilp |
| L_16_7_6_3 | (7,6,3) | 4 | 4 | 1.0000 | 0.00% | 88.706 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_6_4 | (7,6,4) | 13 | 16 | 1.2308 | 23.08% | 121.032 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_6_5 | (7,6,5) | 78 | 104 | 1.3333 | 33.33% | 123.711 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_7_3 | (7,7,3) | 2 | 2 | 1.0000 | 0.00% | 0.524 | true | n=16:bitmask-greedy-bound |
| L_16_7_7_4 | (7,7,4) | 6 | 7 | 1.1667 | 16.67% | 120.191 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_7_5 | (7,7,5) | 31 | 42 | 1.3548 | 35.48% | 124.479 | true | n=16:bitmask-random-greedy-lns-ilp |
| L_16_7_7_6 | (7,7,6) | 293 | 384 | 1.3106 | 31.06% | 145.976 | true | n=16:bitmask-random-greedy-lns-ilp |