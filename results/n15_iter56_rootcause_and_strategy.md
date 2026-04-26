# n<=15 ???14??????iter5/iter6?

- ????: 2026-04-26 06:26:53
- ????: 14
- ?????: 2
- ??????: 12

## ???????????

| cluster | count | compliant | avg_gap | avg_excess_to_110 |
| --- | ---: | ---: | ---: | ---: |
| containment_s_eq_j__edge | 1 | 0 | 0.111111 | 2.0 |
| containment_s_eq_j__medium | 2 | 0 | 0.127632 | 6.0 |
| containment_s_eq_j__ok | 1 | 1 | 0.094203 | 0.0 |
| containment_s_eq_j__severe | 2 | 0 | 0.213256 | 40.0 |
| general_noncontain__edge | 1 | 0 | 0.103448 | 1.0 |
| general_noncontain__ok | 1 | 1 | 0.1 | 0.0 |
| j_eq_k_noncontain_medium_n__medium | 4 | 0 | 0.159084 | 4.5 |
| j_eq_k_noncontain_medium_n__severe | 2 | 0 | 0.21248 | 18.5 |

## case??

| id | family | baseline | 110%?? | source | iter5 | iter6 | best | best_excess | best_from | compliant |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_14_7_5_5 | containment_s_eq_j | 138 | 151 | 152 | 151 | 151 | 151 | 0 | n15_iter5_cluster_solver_auto_portfolio.json | True |
| L_15_6_5_4 | general_noncontain | 40 | 44 | 45 | 44 | 44 | 44 | 0 | n15_iter5_cluster_solver_auto_portfolio.json | True |
| L_15_7_6_5 | general_noncontain | 58 | 63 | 65 | 65 | 64 | 64 | 1 | n15_iter6_cluster_solver_auto_portfolio_seed2.json | False |
| L_15_6_4_4 | containment_s_eq_j | 117 | 128 | 130 | 130 | 135 | 130 | 2 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_14_6_4_4 | containment_s_eq_j | 80 | 88 | 91 | 91 | 91 | 91 | 3 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_13_7_7_6 | j_eq_k_noncontain_medium_n | 61 | 67 | 71 | 74 | 72 | 71 | 4 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_14_6_6_5 | j_eq_k_noncontain_medium_n | 98 | 107 | 111 | 112 | 112 | 111 | 4 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_13_6_6_5 | j_eq_k_noncontain_medium_n | 61 | 67 | 72 | 73 | 72 | 72 | 5 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_14_5_5_4 | j_eq_k_noncontain_medium_n | 69 | 75 | 80 | 80 | 80 | 80 | 5 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_14_7_6_6 | containment_s_eq_j | 501 | 551 | 560 | 574 | 574 | 560 | 9 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_15_6_6_5 | j_eq_k_noncontain_medium_n | 142 | 156 | 170 | 179 | 180 | 170 | 14 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_15_7_7_6 | j_eq_k_noncontain_medium_n | 180 | 198 | 221 | 225 | 225 | 221 | 23 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_15_7_5_5 | containment_s_eq_j | 189 | 207 | 240 | 240 | 240 | 240 | 33 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
| L_15_7_6_6 | containment_s_eq_j | 817 | 898 | 945 | 960 | 960 | 945 | 47 | n_le_15_noncompliant15_after_special_v5_w1.json | False |
