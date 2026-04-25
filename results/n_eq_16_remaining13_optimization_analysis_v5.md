# n=16 ??13????????v5?

- ?????`D:\ai2026.4\CilantroKing\results\n_eq_16_after_anchor_v6_no_cpsat_full.json`
- ?????13 ??????????

## ??????

| run | compliant | non_compliant | avg_gap | avg_elapsed_sec |
| --- | ---: | ---: | ---: | ---: |
| n_eq_16_remaining13_after_case_module_v1_no_cpsat.json | 1 | 12 | 0.182101 | 98.747 |
| n_eq_16_remaining13_after_case_module_v2_cpsat.json | 1 | 12 | 0.182373 | 96.602 |
| n_eq_16_remaining13_after_case_module_v3_no_cpsat.json | 1 | 12 | 0.179962 | 94.729 |
| n_eq_16_remaining13_after_case_module_v4_cpsat.json | 1 | 12 | 0.180768 | 94.636 |
| n_eq_16_remaining13_after_case_module_v5_no_cpsat.json | 2 | 11 | 0.182877 | 100.133 |

## v6 -> v5 ????

| id | baseline | threshold | v6_solver | v5_solver | delta(v5-v6) | need_drop_v6 | need_drop_v5 | v5_compliant |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| L_16_4_4_3 | 64 | 70 | 72 | 70 | -2 | 2 | 0 | True |
| L_16_5_3_3 | 65 | 71 | 72 | 71 | -1 | 1 | 0 | True |
| L_16_5_5_4 | 132 | 145 | 156 | 156 | 0 | 11 | 11 | False |
| L_16_6_4_4 | 152 | 167 | 180 | 181 | 1 | 13 | 14 | False |
| L_16_6_5_4 | 52 | 57 | 60 | 60 | 0 | 3 | 3 | False |
| L_16_6_6_5 | 223 | 245 | 262 | 263 | 1 | 17 | 18 | False |
| L_16_7_4_4 | 76 | 83 | 89 | 89 | 0 | 6 | 6 | False |
| L_16_7_5_4 | 28 | 30 | 32 | 32 | 0 | 2 | 2 | False |
| L_16_7_5_5 | 283 | 311 | 351 | 351 | 0 | 40 | 40 | False |
| L_16_7_6_5 | 78 | 85 | 99 | 99 | 0 | 14 | 14 | False |
| L_16_7_7_4 | 6 | 6 | 7 | 7 | 0 | 1 | 1 | False |
| L_16_7_7_5 | 31 | 34 | 37 | 38 | 1 | 3 | 4 | False |
| L_16_7_7_6 | 293 | 322 | 372 | 372 | 0 | 50 | 50 | False |

## best-of-runs?v1~v5?

| id | best_solver | best_run | threshold | need_drop_best | compliant_best |
| --- | ---: | --- | ---: | ---: | --- |
| L_16_4_4_3 | 70 | n_eq_16_remaining13_after_case_module_v5_no_cpsat.json | 70 | 0 | True |
| L_16_5_3_3 | 70 | n_eq_16_remaining13_after_case_module_v3_no_cpsat.json | 71 | 0 | True |
| L_16_5_5_4 | 155 | n_eq_16_remaining13_after_case_module_v3_no_cpsat.json | 145 | 10 | False |
| L_16_6_4_4 | 180 | n_eq_16_remaining13_after_case_module_v1_no_cpsat.json | 167 | 13 | False |
| L_16_6_5_4 | 60 | n_eq_16_remaining13_after_case_module_v1_no_cpsat.json | 57 | 3 | False |
| L_16_6_6_5 | 263 | n_eq_16_remaining13_after_case_module_v3_no_cpsat.json | 245 | 18 | False |
| L_16_7_4_4 | 89 | n_eq_16_remaining13_after_case_module_v1_no_cpsat.json | 83 | 6 | False |
| L_16_7_5_4 | 31 | n_eq_16_remaining13_after_case_module_v1_no_cpsat.json | 30 | 1 | False |
| L_16_7_5_5 | 349 | n_eq_16_remaining13_after_case_module_v3_no_cpsat.json | 311 | 38 | False |
| L_16_7_6_5 | 99 | n_eq_16_remaining13_after_case_module_v1_no_cpsat.json | 85 | 14 | False |
| L_16_7_7_4 | 7 | n_eq_16_remaining13_after_case_module_v1_no_cpsat.json | 6 | 1 | False |
| L_16_7_7_5 | 38 | n_eq_16_remaining13_after_case_module_v1_no_cpsat.json | 34 | 4 | False |
| L_16_7_7_6 | 371 | n_eq_16_remaining13_after_case_module_v3_no_cpsat.json | 322 | 49 | False |

## ??

- ??????2/13?`L_16_5_3_3`, `L_16_4_4_3`??
- ???????`L_16_7_7_6`, `L_16_7_5_5`, `L_16_7_6_5`, `L_16_6_6_5`, `L_16_6_4_4`?
- ????? near-cluster ????? hard-cluster????>=14??????