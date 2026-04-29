# n<16 ??24??????????v5?

- ????: ????
- ????: `results/n_lt_16_remaining24_from_v3.json`
- ????: `results/n_lt_16_remaining24_after_opt_v5.json`

## 1. ????

- ? `containment_s_eq_j` + `j-s=0`: 10 ?, ??gap `19.85% -> 19.71%`
- ? `j_eq_k_noncontain_medium_n` + `j-s=1`: 9 ?, ??gap `22.10% -> 20.05%`
- ? `general_noncontain` + `j-s=1`: 5 ?, ??gap `12.89% -> 12.02%`

## 2. ????????????????

- ??????????24??????:
  - hill_climb: 2
  - tabu: 1
  - simulated_annealing: 0
  - random_greedy: 0
  - known_design: 20
- ?????: `hill-climb / tabu / simulated annealing / random greedy` ??????
- ????????????????????????????

## 3. ?????????

- ??A?j=k, s=j-1?: ??????????????????
  - ??: n<16 ?????? + ???????
- ??B??????: Phase-H ??????????????????????
  - ??: ?????????? `_phase_h_ranked_candidates`?
- ??C???????: ????????CP-SAT??????????
  - ??: ???? `... -> Phase-H -> Phase-G -> Phase-H`?

## 4. ?????v3 -> v5?

- ???: `0/24 -> 2/24`
- ??gap: `19.25% -> 18.23%`
- ????: `106.24s -> 28.83s`
- ??????new-old???: `-23`

### 4.1 ?????10?

- `L_14_7_7_6`: `144 -> 130` (?-14), gap `44.00% -> 30.00%`
- `L_15_7_6_6`: `992 -> 988` (?-4), gap `21.42% -> 20.93%`
- `L_14_7_6_6`: `597 -> 594` (?-3), gap `19.16% -> 18.56%`
- `L_13_5_5_4`: `54 -> 52` (?-2), gap `12.50% -> 8.33%`
- `L_14_6_5_4`: `33 -> 31` (?-2), gap `13.79% -> 6.90%`
- `L_14_6_5_5`: `429 -> 427` (?-2), gap `15.63% -> 15.09%`
- `L_14_6_6_5`: `116 -> 114` (?-2), gap `18.37% -> 16.33%`
- `L_15_6_4_4`: `137 -> 135` (?-2), gap `17.09% -> 15.38%`
- `L_15_6_6_5`: `181 -> 179` (?-2), gap `27.46% -> 26.06%`
- `L_14_6_4_4`: `102 -> 101` (?-1), gap `27.50% -> 26.25%`

### 4.2 ??????gap???

- `L_14_7_7_6` `j_eq_k_noncontain_medium_n`: baseline `100`, solver `130`, gap `30.00%`, elapsed `62.37s`
- `L_13_7_5_5` `containment_s_eq_j`: baseline `78`, solver `101`, gap `29.49%`, elapsed `8.11s`
- `L_15_7_5_5` `containment_s_eq_j`: baseline `189`, solver `241`, gap `27.51%`, elapsed `14.79s`
- `L_14_6_4_4` `containment_s_eq_j`: baseline `80`, solver `101`, gap `26.25%`, elapsed `10.24s`
- `L_15_6_6_5` `j_eq_k_noncontain_medium_n`: baseline `142`, solver `179`, gap `26.06%`, elapsed `41.75s`
- `L_15_7_7_6` `j_eq_k_noncontain_medium_n`: baseline `180`, solver `225`, gap `25.00%`, elapsed `29.86s`
- `L_15_5_5_4` `j_eq_k_noncontain_medium_n`: baseline `95`, solver `115`, gap `21.05%`, elapsed `45.11s`
- `L_15_7_6_6` `containment_s_eq_j`: baseline `817`, solver `988`, gap `20.93%`, elapsed `28.60s`
- `L_13_7_7_6` `j_eq_k_noncontain_medium_n`: baseline `61`, solver `73`, gap `19.67%`, elapsed `22.95s`
- `L_14_7_6_6` `containment_s_eq_j`: baseline `501`, solver `594`, gap `18.56%`, elapsed `24.55s`
- `L_13_6_6_5` `j_eq_k_noncontain_medium_n`: baseline `61`, solver `72`, gap `18.03%`, elapsed `24.19s`
- `L_14_6_6_5` `j_eq_k_noncontain_medium_n`: baseline `98`, solver `114`, gap `16.33%`, elapsed `49.94s`
- `L_14_5_5_4` `j_eq_k_noncontain_medium_n`: baseline `69`, solver `80`, gap `15.94%`, elapsed `27.63s`
- `L_14_7_5_5` `containment_s_eq_j`: baseline `138`, solver `160`, gap `15.94%`, elapsed `19.67s`
- `L_13_6_5_5` `containment_s_eq_j`: baseline `245`, solver `283`, gap `15.51%`, elapsed `12.45s`
- `L_15_6_4_4` `containment_s_eq_j`: baseline `117`, solver `135`, gap `15.38%`, elapsed `16.33s`
- `L_14_6_5_5` `containment_s_eq_j`: baseline `371`, solver `427`, gap `15.09%`, elapsed `33.57s`
- `L_15_6_5_4` `general_noncontain`: baseline `40`, solver `46`, gap `15.00%`, elapsed `27.65s`
- `L_15_7_5_4` `general_noncontain`: baseline `20`, solver `23`, gap `15.00%`, elapsed `39.49s`
- `L_15_6_5_5` `containment_s_eq_j`: baseline `578`, solver `650`, gap `12.46%`, elapsed `46.22s`
- `L_15_7_6_5` `general_noncontain`: baseline `58`, solver `65`, gap `12.07%`, elapsed `30.29s`
- `L_14_7_6_5` `general_noncontain`: baseline `36`, solver `40`, gap `11.11%`, elapsed `34.00s`
