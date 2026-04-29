# Results Directory Layout

Active result files stay directly under this directory.

## Keep in root

- current baseline files
- the latest compact evaluation output
- current reproducible `n <= 15` snapshots
- method hint files still used during optimization

## Archive layout

- [`archive/n_le_15`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_le_15): historical `n <= 15` runs and reports
- [`archive/n_eq_16`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_eq_16): isolated `n = 16` experiments
- [`archive/n_lt_16`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_lt_16): broader `< 16` analyses and iteration logs
- [`archive/tmp`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/tmp): temporary one-off outputs and special-case scratch artifacts
- [`archive/research`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/research): downloaded HTML/TXT research scraps
- [`archive/misc`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/misc): leftover reports outside the main groups

The archive is intentionally kept inside the repository so older optimization work remains auditable without polluting the active working set.
