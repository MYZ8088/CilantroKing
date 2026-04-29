# n=16 ??????????iter2?

- source: `D:\ai2026.4\CilantroKing\results\n_eq_16_after_opt_iter2.json`
- total_cases: 29
- noncompliant_cases: 18
- ??: solver_blocks > baseline*1.10 ? runtime>120s ?????

## ???

| cluster | count | avg_gap | max_gap | avg_elapsed | runtime_fail |
| --- | ---: | ---: | ---: | ---: | ---: |
| C1_light_k5_containment_early | 1 | 0.1231 | 0.1231 | 0.52 | 0 |
| C1_light_k5_general_early | 1 | 0.1935 | 0.1935 | 5.52 | 0 |
| C1_light_k5_other | 3 | 0.1652 | 0.2121 | 119.02 | 0 |
| C2_hard_j_eq_k_dense | 5 | 0.2474 | 0.3548 | 120.96 | 3 |
| C3_hard_containment_dense | 3 | 0.2542 | 0.2756 | 119.40 | 0 |
| C4_hard_general_dense | 5 | 0.2348 | 0.3462 | 119.24 | 0 |

## ????

### C1_light_k5_containment_early
- ????: ?????????????????????????10%????)
- ???: 1
- ????:
  - L_16_5_3_3  L(16,5,3,3), gap=0.1231, elapsed=0.52s, reasons=quality_over_10pct

### C1_light_k5_general_early
- ????: ????????????????????????CP-SAT???)
- ???: 1
- ????:
  - L_16_5_4_3  L(16,5,4,3), gap=0.1935, elapsed=5.52s, reasons=quality_over_10pct

### C1_light_k5_other
- ????: ????????????????????)
- ???: 3
- ????:
  - L_16_5_5_4  L(16,5,5,4), gap=0.2121, elapsed=118.41s, reasons=quality_over_10pct
  - L_16_5_5_3  L(16,5,5,3), gap=0.1429, elapsed=119.05s, reasons=quality_over_10pct
  - L_16_4_4_3  L(16,4,4,3), gap=0.1406, elapsed=119.60s, reasons=quality_over_10pct

### C2_hard_j_eq_k_dense
- ????: ??? j=k ????????????????1-step??????????+???)
- ???: 5
- ????:
  - L_16_7_7_5  L(16,7,7,5), gap=0.3548, elapsed=122.06s, reasons=timeout_over_120s;quality_over_10pct
  - L_16_7_7_6  L(16,7,7,6), gap=0.2867, elapsed=119.43s, reasons=quality_over_10pct
  - L_16_6_6_5  L(16,6,6,5), gap=0.2287, elapsed=119.46s, reasons=quality_over_10pct
  - L_16_6_6_4  L(16,6,6,4), gap=0.2000, elapsed=123.38s, reasons=timeout_over_120s;quality_over_10pct
  - L_16_7_7_4  L(16,7,7,4), gap=0.1667, elapsed=120.46s, reasons=timeout_over_120s;quality_over_10pct

### C3_hard_containment_dense
- ????: containment ???????????120s?????????)
- ???: 3
- ????:
  - L_16_7_5_5  L(16,7,5,5), gap=0.2756, elapsed=119.44s, reasons=quality_over_10pct
  - L_16_6_4_4  L(16,6,4,4), gap=0.2500, elapsed=119.38s, reasons=quality_over_10pct
  - L_16_7_4_4  L(16,7,4,4), gap=0.2368, elapsed=119.36s, reasons=quality_over_10pct

### C4_hard_general_dense
- ????: general ?????k??????????????????????????)
- ???: 5
- ????:
  - L_16_7_6_5  L(16,7,6,5), gap=0.3462, elapsed=119.41s, reasons=quality_over_10pct
  - L_16_6_5_4  L(16,6,5,4), gap=0.2308, elapsed=118.80s, reasons=quality_over_10pct
  - L_16_7_6_4  L(16,7,6,4), gap=0.2308, elapsed=119.21s, reasons=quality_over_10pct
  - L_16_6_4_3  L(16,6,4,3), gap=0.1875, elapsed=119.38s, reasons=quality_over_10pct
  - L_16_7_5_4  L(16,7,5,4), gap=0.1786, elapsed=119.37s, reasons=quality_over_10pct

## ??????????

- C1: `n16_light` ???partial-reseed + multi-drop + small CP-SAT bridge?
- C2: `n16_hard_jk` ???2-step/1-step ???? + anchored reseed?
- C3: `n16_hard_containment` ???containment??????? + anchored reseed?
- C4: `n16_hard_general` ???general??????? + anchored reseed?
