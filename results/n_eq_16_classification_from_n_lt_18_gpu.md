# n=16 ??????? n<18 ???

- source: `D:\ai2026.4\CilantroKing\results\n_lt_18_compliance_120s_10pct_gpu.json`
- generated_at: 2026-04-25 02:15:50

## ??

- total: 29
- compliant: 8
- non_compliant: 21
- quality_fail: 21
- runtime_fail: 0
- verify_fail: 0

## family ??

- all: {'containment_s_eq_j': 9, 'j_eq_k_noncontain_medium_n': 10, 'general_noncontain': 10}
- non_compliant: {'j_eq_k_noncontain_medium_n': 7, 'containment_s_eq_j': 6, 'general_noncontain': 8}

## ???????

- {'quality_over_10pct': 21}

## compliant (8)

| id | params | family | baseline | solver | gap | elapsed_sec | reasons |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| L_16_4_3_3 | L(16,4,3,3) | containment_s_eq_j | 140 | 140 | 0.0 | 0.284708 |  |
| L_16_5_4_4 | L(16,5,4,4) | containment_s_eq_j | 404 | 443 | 0.096535 | 0.373743 |  |
| L_16_5_5_3 | L(16,5,5,3) | j_eq_k_noncontain_medium_n | 14 | 14 | 0.0 | 117.996934 |  |
| L_16_6_5_5 | L(16,6,5,5) | containment_s_eq_j | 808 | 840 | 0.039604 | 0.795666 |  |
| L_16_6_6_3 | L(16,6,6,3) | j_eq_k_noncontain_medium_n | 5 | 5 | 0.0 | 27.439749 |  |
| L_16_7_5_3 | L(16,7,5,3) | general_noncontain | 5 | 5 | 0.0 | 13.493864 |  |
| L_16_7_6_3 | L(16,7,6,3) | general_noncontain | 4 | 4 | 0.0 | 33.202052 |  |
| L_16_7_7_3 | L(16,7,7,3) | j_eq_k_noncontain_medium_n | 2 | 2 | 0.0 | 105.65975 |  |

## gap_10_20pct (8)

| id | params | family | baseline | solver | gap | elapsed_sec | reasons |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| L_16_4_4_3 | L(16,4,4,3) | j_eq_k_noncontain_medium_n | 64 | 74 | 0.15625 | 84.692636 | quality_over_10pct |
| L_16_5_3_3 | L(16,5,3,3) | containment_s_eq_j | 65 | 73 | 0.123077 | 0.49977 | quality_over_10pct |
| L_16_5_4_3 | L(16,5,4,3) | general_noncontain | 31 | 37 | 0.193548 | 5.098483 | quality_over_10pct |
| L_16_6_3_3 | L(16,6,3,3) | containment_s_eq_j | 38 | 43 | 0.131579 | 4.81991 | quality_over_10pct |
| L_16_6_6_4 | L(16,6,6,4) | j_eq_k_noncontain_medium_n | 25 | 30 | 0.2 | 74.288874 | quality_over_10pct |
| L_16_7_3_3 | L(16,7,3,3) | containment_s_eq_j | 24 | 27 | 0.125 | 2.555417 | quality_over_10pct |
| L_16_7_4_3 | L(16,7,4,3) | general_noncontain | 11 | 13 | 0.181818 | 10.059994 | quality_over_10pct |
| L_16_7_7_4 | L(16,7,7,4) | j_eq_k_noncontain_medium_n | 6 | 7 | 0.166667 | 52.073992 | quality_over_10pct |

## gap_20_30pct (8)

| id | params | family | baseline | solver | gap | elapsed_sec | reasons |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| L_16_5_5_4 | L(16,5,5,4) | j_eq_k_noncontain_medium_n | 132 | 163 | 0.234848 | 111.990211 | quality_over_10pct |
| L_16_6_4_4 | L(16,6,4,4) | containment_s_eq_j | 152 | 192 | 0.263158 | 0.37766 | quality_over_10pct |
| L_16_6_5_3 | L(16,6,5,3) | general_noncontain | 8 | 10 | 0.25 | 8.376649 | quality_over_10pct |
| L_16_6_5_4 | L(16,6,5,4) | general_noncontain | 52 | 64 | 0.230769 | 9.522162 | quality_over_10pct |
| L_16_6_6_5 | L(16,6,6,5) | j_eq_k_noncontain_medium_n | 223 | 276 | 0.237668 | 60.092025 | quality_over_10pct |
| L_16_7_4_4 | L(16,7,4,4) | containment_s_eq_j | 76 | 96 | 0.263158 | 1.099424 | quality_over_10pct |
| L_16_7_5_4 | L(16,7,5,4) | general_noncontain | 28 | 34 | 0.214286 | 14.341052 | quality_over_10pct |
| L_16_7_5_5 | L(16,7,5,5) | containment_s_eq_j | 283 | 361 | 0.275618 | 0.537422 | quality_over_10pct |

## gap_gt_30pct (5)

| id | params | family | baseline | solver | gap | elapsed_sec | reasons |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| L_16_6_4_3 | L(16,6,4,3) | general_noncontain | 16 | 21 | 0.3125 | 10.562487 | quality_over_10pct |
| L_16_7_6_4 | L(16,7,6,4) | general_noncontain | 13 | 17 | 0.307692 | 20.490111 | quality_over_10pct |
| L_16_7_6_5 | L(16,7,6,5) | general_noncontain | 78 | 106 | 0.358974 | 21.507951 | quality_over_10pct |
| L_16_7_7_5 | L(16,7,7,5) | j_eq_k_noncontain_medium_n | 31 | 42 | 0.354839 | 59.493029 | quality_over_10pct |
| L_16_7_7_6 | L(16,7,7,6) | j_eq_k_noncontain_medium_n | 293 | 382 | 0.303754 | 32.799461 | quality_over_10pct |

## invalid_or_timeout (0)

- (none)

## other_noncompliant (0)

- (none)

