# n<=15 ???14?????????????

- ????: 2026-04-26 00:22:57
- ?????: 14
- ????????: 12
- ???????: 2

## ?????????????

| cluster | count | compliant | avg_gap | avg_excess_to_110 |
| --- | ---: | ---: | ---: | ---: |
| containment_s_eq_j__edge | 2 | 0 | 0.104617 | 2.5 |
| containment_s_eq_j__medium | 2 | 0 | 0.144638 | 23.0 |
| containment_s_eq_j__ok | 1 | 1 | 0.08547 | -1.0 |
| containment_s_eq_j__severe | 1 | 0 | 0.269841 | 33.0 |
| general_noncontain__medium | 2 | 0 | 0.122845 | 1.5 |
| j_eq_k_noncontain_medium_n__medium | 4 | 0 | 0.144324 | 5.5 |
| j_eq_k_noncontain_medium_n__ok | 1 | 1 | 0.0 | -6.0 |
| j_eq_k_noncontain_medium_n__severe | 1 | 0 | 0.197183 | 14.0 |

## ??????? vs ?????

| id | family | baseline | 110%?? | source | best | delta | best_gap | excess_to_limit | best_from | compliant |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| L_13_6_6_5 | j_eq_k_noncontain_medium_n | 61 | 67 | 72 | 61 | -11 | 0.000000 | -6 | n15_iter2_cluster_solver_exact_first.json | True |
| L_13_7_7_6 | j_eq_k_noncontain_medium_n | 61 | 67 | 71 | 70 | -1 | 0.147541 | 3 | n15_iter3_cluster_solver_repair_first.json | False |
| L_14_5_5_4 | j_eq_k_noncontain_medium_n | 69 | 75 | 80 | 78 | -2 | 0.130435 | 3 | n15_iter1_cluster_solver_balanced.json | False |
| L_14_6_4_4 | containment_s_eq_j | 80 | 88 | 91 | 91 | 0 | 0.137500 | 3 | source | False |
| L_14_6_6_5 | j_eq_k_noncontain_medium_n | 98 | 107 | 111 | 111 | 0 | 0.132653 | 4 | source | False |
| L_14_7_5_5 | containment_s_eq_j | 138 | 151 | 152 | 152 | 0 | 0.101449 | 1 | source | False |
| L_14_7_6_6 | containment_s_eq_j | 501 | 551 | 560 | 555 | -5 | 0.107784 | 4 | n15_iter1_cluster_solver_balanced.json | False |
| L_15_6_4_4 | containment_s_eq_j | 117 | 128 | 130 | 127 | -3 | 0.085470 | -1 | n15_iter3_cluster_solver_repair_first.json | True |
| L_15_6_5_4 | general_noncontain | 40 | 44 | 45 | 45 | 0 | 0.125000 | 1 | source | False |
| L_15_6_6_5 | j_eq_k_noncontain_medium_n | 142 | 156 | 170 | 170 | 0 | 0.197183 | 14 | source | False |
| L_15_7_5_5 | containment_s_eq_j | 189 | 207 | 240 | 240 | 0 | 0.269841 | 33 | source | False |
| L_15_7_6_5 | general_noncontain | 58 | 63 | 65 | 65 | 0 | 0.120690 | 2 | source | False |
| L_15_7_6_6 | containment_s_eq_j | 817 | 898 | 945 | 941 | -4 | 0.151775 | 43 | n15_iter4_cluster_solver_repair_first_nb.json | False |
| L_15_7_7_6 | j_eq_k_noncontain_medium_n | 180 | 198 | 221 | 210 | -11 | 0.166667 | 12 | n15_iter1_cluster_solver_balanced.json | False |

## ?????????

- `j_eq_k_noncontain_medium_n`: ???+????drop-repair ?????????????? orbit/domset ???????????
- `containment_s_eq_j`: ????????1~5???????????? shrinking ???????????? neighborhood decision SAT ?????
- `general_noncontain`: ???????????????????????????????+??????

## ?? coveringrepository ?????

- Deep search options -> ?????????SAT/??SAT????????????
- Shrinking options -> ????? drop-repair ????????
- Best covering blocks / blocks weight -> ????? fragile-target ???????
- Union/inverse construction ?? -> ?????????????????????

## ?????????????

1. containment ???????????L_14_7_5_5, L_14_7_6_6, L_15_6_5_4, L_15_7_6_5
2. jk ????5??????L_14_5_5_4, L_14_6_6_5
3. jk ????>10?????L_15_6_6_5, L_15_7_5_5, L_15_7_7_6
