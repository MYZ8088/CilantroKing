# n<=15 ????????????v1?

- ???: 306
- ??: 279
- ???: 27
- ?????: 7
- ????: 24

| id | L(n,k,j,s) | family | status | baseline | solver | ratio | elapsed | reasons |
|---|---|---|---|---:|---:|---:|---:|---|
| L_12_7_6_5 | L(12,7,6,5) | general_noncontain | timeout | 16 | None | None | 130.042708 | timeout_over_120s;quality_over_10pct;verification_failed |
| L_12_7_6_6 | L(12,7,6,6) | containment_s_eq_j | timeout | 176 | None | None | 130.025324 | timeout_over_120s;quality_over_10pct;verification_failed |
| L_13_5_5_4 | L(13,5,5,4) | j_eq_k_noncontain_medium_n | ok | 48 | 54 | 1.125000 | 114.916148 | quality_over_10pct |
| L_13_6_6_5 | L(13,6,6,5) | j_eq_k_noncontain_medium_n | ok | 61 | 72 | 1.180328 | 117.140910 | quality_over_10pct |
| L_13_7_5_5 | L(13,7,5,5) | containment_s_eq_j | timeout | 78 | None | None | 130.032436 | timeout_over_120s;quality_over_10pct;verification_failed |
| L_13_7_6_5 | L(13,7,6,5) | general_noncontain | timeout | 24 | 24 | 1.000000 | 120.001438 | timeout_over_120s |
| L_13_7_7_6 | L(13,7,7,6) | j_eq_k_noncontain_medium_n | ok | 61 | 73 | 1.196721 | 118.659859 | quality_over_10pct |
| L_14_5_5_4 | L(14,5,5,4) | j_eq_k_noncontain_medium_n | ok | 69 | 79 | 1.144928 | 118.631917 | quality_over_10pct |
| L_14_6_4_4 | L(14,6,4,4) | containment_s_eq_j | ok | 80 | 91 | 1.137500 | 118.640047 | quality_over_10pct |
| L_14_6_5_4 | L(14,6,5,4) | general_noncontain | timeout | 29 | 32 | 1.103448 | 120.000635 | timeout_over_120s;quality_over_10pct |
| L_14_6_6_5 | L(14,6,6,5) | j_eq_k_noncontain_medium_n | ok | 98 | 112 | 1.142857 | 118.640103 | quality_over_10pct |
| L_14_7_5_5 | L(14,7,5,5) | containment_s_eq_j | ok | 138 | 154 | 1.115942 | 118.814498 | quality_over_10pct |
| L_14_7_6_5 | L(14,7,6,5) | general_noncontain | ok | 36 | 40 | 1.111111 | 115.941588 | quality_over_10pct |
| L_14_7_6_6 | L(14,7,6,6) | containment_s_eq_j | ok | 501 | 588 | 1.173653 | 116.087579 | quality_over_10pct |
| L_14_7_7_5 | L(14,7,7,5) | j_eq_k_noncontain_medium_n | ok | 14 | 16 | 1.142857 | 116.415770 | quality_over_10pct |
| L_14_7_7_6 | L(14,7,7,6) | j_eq_k_noncontain_medium_n | ok | 100 | 140 | 1.400000 | 118.802370 | quality_over_10pct |
| L_15_5_5_4 | L(15,5,5,4) | j_eq_k_noncontain_medium_n | ok | 95 | 119 | 1.252632 | 116.493235 | quality_over_10pct |
| L_15_6_4_3 | L(15,6,4,3) | general_noncontain | timeout | 14 | 15 | 1.071429 | 120.000761 | timeout_over_120s |
| L_15_6_5_4 | L(15,6,5,4) | general_noncontain | ok | 40 | 46 | 1.150000 | 117.238599 | quality_over_10pct |
| L_15_6_5_5 | L(15,6,5,5) | containment_s_eq_j | ok | 578 | 645 | 1.115917 | 116.670766 | quality_over_10pct |
| L_15_6_6_5 | L(15,6,6,5) | j_eq_k_noncontain_medium_n | ok | 142 | 175 | 1.232394 | 117.771556 | quality_over_10pct |
| L_15_7_5_4 | L(15,7,5,4) | general_noncontain | ok | 20 | 23 | 1.150000 | 117.882831 | quality_over_10pct |
| L_15_7_5_5 | L(15,7,5,5) | containment_s_eq_j | ok | 189 | 234 | 1.238095 | 117.956648 | quality_over_10pct |
| L_15_7_6_4 | L(15,7,6,4) | general_noncontain | timeout | 9 | 9 | 1.000000 | 120.000536 | timeout_over_120s |
| L_15_7_6_5 | L(15,7,6,5) | general_noncontain | ok | 58 | 65 | 1.120690 | 117.464256 | quality_over_10pct |
| L_15_7_6_6 | L(15,7,6,6) | containment_s_eq_j | ok | 817 | 953 | 1.166463 | 115.731159 | quality_over_10pct |
| L_15_7_7_6 | L(15,7,7,6) | j_eq_k_noncontain_medium_n | ok | 180 | 210 | 1.166667 | 118.314272 | quality_over_10pct |

## ????
- ? n: {12: 2, 13: 5, 14: 9, 15: 11}
- ? family: {'general_noncontain': 9, 'containment_s_eq_j': 8, 'j_eq_k_noncontain_medium_n': 10}
- ? status: {'timeout': 7, 'ok': 20}
