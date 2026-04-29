# Optimal Samples Selection System

This is the Python-only covering-design optimizer for the PDF project. The saved project keeps the algorithmic solver, validation tools, development notes, and the `n=15`/`n=16` report.

For selected samples `N`, the solver outputs the smallest groups it can find so that every `j`-sample group has at least `s` common samples with at least one generated `k`-sample group.

## Algorithm

- `n=15`: dispatched directly to [n15_solver.py](n15_solver.py). This file now contains the copied local algorithm for the `n=15` path, including its internal recursive helpers, full bitmask coverage, cyclic-orbit construction, partial-orbit ILP repair for `n=15,k=7,j=s=5`, recursive covering construction, greedy restarts, local search, optional ILP compression, and full validation.
- `n=16`: dispatched directly to [n16_solver.py](n16_solver.py). This file contains a separate copied algorithm for `n=16`, tuned independently from the `n=15` path. The hard `n=16,k=7,j=s=5` path is still algorithmic partial cyclic orbit plus ILP repair; it does not use the baseline validation file as an answer source.
- Other `n <= 16` values are intentionally not kept in this trimmed project. The retained code is focused on the requested `n=15` and `n=16` cases.

No result table is embedded in the code. All groups are generated from the input parameters.

See [ALGORITHM.md](ALGORITHM.md) for the development/algorithm notes, including set cover, ILP, fallback methods, and full baseline validation. The saved `n=15`/`n=16` timing and accuracy report is [reports/n15_n16_report.md](reports/n15_n16_report.md).

## Generate Results

Randomly choose `n` samples from `1..m`:

```bash
python3 optimal_samples.py generate --m 45 --n 16 --k 7 --j 5 --s 5 --time-limit 120 --show
```

Use manually selected `n` samples:

```bash
python3 optimal_samples.py generate --m 45 --n 15 --k 7 --j 6 --s 3 --samples 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 --show
```

The result is saved under `db/` using the PDF shape:

```text
m-n-k-j-s-x-y.txt
```

where `x` is the run number and `y` is the number of generated groups.

## DB Operations

```bash
python3 optimal_samples.py list
python3 optimal_samples.py show 45-8-6-5-5-1-12.txt
python3 optimal_samples.py delete 45-8-6-5-5-1-12.txt --yes
```

Running without a subcommand opens the interactive menu:

```bash
python3 optimal_samples.py
```

## Verify

```bash
python3 -m unittest -v
```

The tests cover the main numeric examples in the PDF and verify the DB filename/content format.

Compare against the provided baseline counts with full coverage verification:

```bash
python3 validate_against_baseline.py --max-n 16 --time-limit 120 --ratio-threshold 1.21 --output baseline_validation_results.csv
```

Run quick smoke validation for the extracted `n=15` and `n=16` solver entry points:

```bash
python3 validate_against_baseline.py --only L_15_7_6_3,L_16_7_7_3 --time-limit 10 --ratio-threshold 1.21
```

The hardest measured cases are documented in [ALGORITHM.md](ALGORITHM.md). `L_15_7_5_5` currently measures 228/189 and `L_16_7_5_5` measures 328/283. The standalone `n16_solver.py` path verifies `L_16_7_5_5` in 21.809 seconds with ratio 1.1590, inside the requested 10%-20% comparison window.