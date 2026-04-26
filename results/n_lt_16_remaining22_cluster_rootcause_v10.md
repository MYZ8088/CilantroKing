# ??22???????????????v10?

- ?????`results/n_lt_16_remaining22_from_v5_baselines.json`??? v5 ?????
- ?????`v7 -> v8 -> v9 -> v10`

## 1. ?????22??

- ? `containment_s_eq_j` + `j-s=0`?10 ????gap `19.71% -> 19.42%`
- ? `j_eq_k_noncontain_medium_n` + `j-s=1`?8 ????gap `21.51% -> 21.15%`
- ? `general_noncontain` + `j-s=1`?4 ????gap `13.30% -> 8.85%`

## 2. ????

- `j_eq_k_noncontain_medium_n`???????????????Phase-G ???????
- `containment_s_eq_j`?????????????????????????
- `general_noncontain`??????????1~3???????????????

## 3. ????????????

- ??A?j=k,s=j-1??`_phase_i_jk_cycle_module`???????????
- ??B?s=j??`_phase_i_containment_cycle_module`?containment ?? fixed-size ???
- ??C?general ?????`_phase_i_general_small_module`????????
- ?????`_phase_i_full_cp_sat_module`??????? CP-SAT?

## 4. ? Covering Repository ???????

- ???22????????????
  - hill_climb: 2
  - tabu: 1
  - simulated_annealing: 0
  - random_greedy: 0
  - known_design: 18
- ?????????????hill-climb / tabu / random-greedy / SA???????????

## 5. ???????22??

- v5: ?? `0/22`???gap `19.20%`????? `29.53s`
- v7: ?? `0/22`???gap `19.07%`????? `25.83s`
- v8: ?? `0/22`???gap `18.90%`????? `43.58s`
- v9: ?? `1/22`???gap `18.81%`????? `48.47s`
- v10: ?? `2/22`???gap `18.13%`????? `52.13s`

## 6. ?????v5 -> v10?

- `L_14_5_5_4`: `80 -> 79` (?-1), gap `15.94% -> 14.49%`
- `L_14_6_4_4`: `101 -> 100` (?-1), gap `26.25% -> 25.00%`
- `L_14_7_5_5`: `160 -> 158` (?-2), gap `15.94% -> 14.49%`
- `L_14_7_6_5`: `40 -> 39` (?-1), gap `11.11% -> 8.33%`
- `L_15_6_6_5`: `179 -> 177` (?-2), gap `26.06% -> 24.65%`
- `L_15_7_5_4`: `23 -> 20` (?-3), gap `15.00% -> 0.00%`
- `L_15_7_6_6`: `988 -> 986` (?-2), gap `20.93% -> 20.69%`

## 7. ????????20??

- `L_14_7_7_6` `j_eq_k_noncontain_medium_n`: baseline `100`, solver `130`, gap `30.00%`, elapsed `79.44s`
- `L_13_7_5_5` `containment_s_eq_j`: baseline `78`, solver `101`, gap `29.49%`, elapsed `24.84s`
- `L_15_7_5_5` `containment_s_eq_j`: baseline `189`, solver `241`, gap `27.51%`, elapsed `47.77s`
- `L_14_6_4_4` `containment_s_eq_j`: baseline `80`, solver `100`, gap `25.00%`, elapsed `28.77s`
- `L_15_7_7_6` `j_eq_k_noncontain_medium_n`: baseline `180`, solver `225`, gap `25.00%`, elapsed `54.94s`
- `L_15_6_6_5` `j_eq_k_noncontain_medium_n`: baseline `142`, solver `177`, gap `24.65%`, elapsed `74.04s`
- `L_15_5_5_4` `j_eq_k_noncontain_medium_n`: baseline `95`, solver `115`, gap `21.05%`, elapsed `65.26s`
- `L_15_7_6_6` `containment_s_eq_j`: baseline `817`, solver `986`, gap `20.69%`, elapsed `55.58s`
- `L_13_7_7_6` `j_eq_k_noncontain_medium_n`: baseline `61`, solver `73`, gap `19.67%`, elapsed `39.21s`
- `L_14_7_6_6` `containment_s_eq_j`: baseline `501`, solver `594`, gap `18.56%`, elapsed `48.50s`
- `L_13_6_6_5` `j_eq_k_noncontain_medium_n`: baseline `61`, solver `72`, gap `18.03%`, elapsed `37.58s`
- `L_14_6_6_5` `j_eq_k_noncontain_medium_n`: baseline `98`, solver `114`, gap `16.33%`, elapsed `71.07s`
- `L_13_6_5_5` `containment_s_eq_j`: baseline `245`, solver `283`, gap `15.51%`, elapsed `40.78s`
- `L_15_6_4_4` `containment_s_eq_j`: baseline `117`, solver `135`, gap `15.38%`, elapsed `32.33s`
- `L_14_6_5_5` `containment_s_eq_j`: baseline `371`, solver `427`, gap `15.09%`, elapsed `58.57s`
- `L_15_6_5_4` `general_noncontain`: baseline `40`, solver `46`, gap `15.00%`, elapsed `29.29s`
- `L_14_5_5_4` `j_eq_k_noncontain_medium_n`: baseline `69`, solver `79`, gap `14.49%`, elapsed `43.43s`
- `L_14_7_5_5` `containment_s_eq_j`: baseline `138`, solver `158`, gap `14.49%`, elapsed `41.93s`
- `L_15_6_5_5` `containment_s_eq_j`: baseline `578`, solver `650`, gap `12.46%`, elapsed `64.73s`
- `L_15_7_6_5` `general_noncontain`: baseline `58`, solver `65`, gap `12.07%`, elapsed `41.20s`
