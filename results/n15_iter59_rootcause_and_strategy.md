# n<=15 ???14??????iter5~iter9?

- ????: 2026-04-26 14:02:53
- ????: 14
- ?????: 3
- ??????: 11

## ???????????

| cluster | count | compliant | avg_gap | avg_excess_to_110 |
| --- | ---: | ---: | ---: | ---: |
| containment_s_eq_j__medium | 2 | 0 | 0.127632 | 6.0 |
| containment_s_eq_j__ok | 2 | 2 | 0.077016 | -2.0 |
| containment_s_eq_j__severe | 2 | 0 | 0.173573 | 32.5 |
| general_noncontain__edge | 1 | 0 | 0.103448 | 1.0 |
| general_noncontain__ok | 1 | 1 | 0.1 | 0.0 |
| j_eq_k_noncontain_medium_n__medium | 4 | 0 | 0.151838 | 4.0 |
| j_eq_k_noncontain_medium_n__severe | 2 | 0 | 0.212481 | 18.5 |

## case??

| id | baseline | 110%?? | source | iter5 | iter6 | iter7 | iter8 | iter9 | best | best_excess | best_from | compliant |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_15_6_4_4 | 117 | 128 | 130 | 130 | 135 | 124 | 135 | 125 | 124 | -4 | n15_iter7_cluster_solver_auto_seed_sweep3.json | True |
| L_14_7_5_5 | 138 | 151 | 152 | 151 | 151 | 153 | 152 | 151 | 151 | 0 | n15_iter5_cluster_solver_auto_portfolio.json | True |
| L_15_6_5_4 | 40 | 44 | 45 | 44 | 44 | 44 | 44 | 44 | 44 | 0 | n15_iter5_cluster_solver_auto_portfolio.json | True |
| L_15_7_6_5 | 58 | 63 | 65 | 65 | 64 | 64 | 64 | 64 | 64 | 1 | n15_iter6_cluster_solver_auto_portfolio_seed2.json | False |
| L_14_5_5_4 | 69 | 75 | 80 | 80 | 80 | 78 | 78 | 80 | 78 | 3 | n15_iter7_cluster_solver_auto_seed_sweep3.json | False |
| L_14_6_4_4 | 80 | 88 | 91 | 91 | 91 | 91 | 91 | 91 | 91 | 3 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_13_7_7_6 | 61 | 67 | 71 | 74 | 72 | 71 | 72 | 71 | 71 | 4 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_14_6_6_5 | 98 | 107 | 111 | 112 | 112 | 112 | 112 | 112 | 111 | 4 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_13_6_6_5 | 61 | 67 | 72 | 73 | 72 | 73 | 72 | 73 | 72 | 5 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_14_7_6_6 | 501 | 551 | 560 | 574 | 574 | 574 | 574 | 588 | 560 | 9 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_15_6_6_5 | 142 | 156 | 170 | 179 | 180 | 180 | 180 | 180 | 170 | 14 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_15_7_5_5 | 189 | 207 | 240 | 240 | 240 | 240 | 225 | 240 | 225 | 18 | n15_iter8_cluster_solver_auto_seed_sweep4.json | False |
| L_15_7_7_6 | 180 | 198 | 221 | 225 | 225 | 224 | 225 | 225 | 221 | 23 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_15_7_6_6 | 817 | 898 | 945 | 960 | 960 | 945 | 945 | 960 | 945 | 47 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
