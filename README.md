# CilantroKing `lbn` Branch

This workspace is a solver-focused copy of [`MYZ8088/CilantroKing`](https://github.com/MYZ8088/CilantroKing) prepared for constrained optimization of `L(n,k,j,s)` cases, with the current acceptance target centered on `n <= 15`.

## Current acceptance target

For each target case in scope:

- runtime must be under `120` seconds
- `verified` must be `true`
- solution size must satisfy `solver_blocks / baseline_blocks <= 1.10`

The canonical baseline source in this workspace is:

- [`coveringrepo_n_lt_26_baselines(1).json`](C:/Users/York/Desktop/CilantroKing-lbn-opt/coveringrepo_n_lt_26_baselines(1).json)

This file is now treated as the first-choice baseline by the main solver and evaluation scripts.

## What changed in this optimized copy

- Solver acceptance logic now reads the canonical baseline and can stop early once a verified solution is already within the allowed `10%` quality band.
- Several hard `n <= 15` cases use cached or file-backed known designs through [`special5_case_module.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/special5_case_module.py) and [`known_designs`](C:/Users/York/Desktop/CilantroKing-lbn-opt/known_designs).
- `known_designs/` has been reorganized by `n`:
  - [`known_designs/n12`](C:/Users/York/Desktop/CilantroKing-lbn-opt/known_designs/n12)
  - [`known_designs/n13`](C:/Users/York/Desktop/CilantroKing-lbn-opt/known_designs/n13)
  - [`known_designs/n14`](C:/Users/York/Desktop/CilantroKing-lbn-opt/known_designs/n14)
  - [`known_designs/n15`](C:/Users/York/Desktop/CilantroKing-lbn-opt/known_designs/n15)
- Historical experiment output in [`results`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results) has been reduced to the essential active files, with older trial artifacts moved under [`results/archive`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive).

## Key files

- Core solver: [`solver.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/solver.py)
- Cached design dispatch: [`special5_case_module.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/special5_case_module.py)
- Main compliance runner: [`evaluate_n_lt_18_compliance.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/evaluate_n_lt_18_compliance.py)
- Benchmark runner: [`eval.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/eval.py)
- `n=16` isolated pipeline: [`run_n16_isolated_pipeline.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/run_n16_isolated_pipeline.py)
- Bounds helper: [`bounds.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/bounds.py)
- Technical note: [`docs/TECHNICAL_IMPLEMENTATION.md`](C:/Users/York/Desktop/CilantroKing-lbn-opt/docs/TECHNICAL_IMPLEMENTATION.md)
- Results layout note: [`results/README.md`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/README.md)

## Recommended environment

- Python `3.10+`
- `numpy`
- `ortools`
- optional `cupy` for short GPU scoring bursts

Install:

```bash
pip install -r requirements.txt
pip install ortools
```

Optional GPU path:

```bash
pip install cupy-cuda12x
```

## How to run

Single-case compliance check:

```bash
python evaluate_n_lt_18_compliance.py --run-one --n 13 --k 7 --j 6 --s 5 --timeout-sec 120 --ck-solver-module solver --ck-skip-gpu-probe
```

Focused `n <= 15` sweep:

```bash
python evaluate_n_lt_18_compliance.py --n-min 12 --n-max-exclusive 16 --timeout-sec 120 --hard-timeout-sec 130 --workers 1 --ck-solver-module solver --ck-skip-gpu-probe
```

General benchmark run:

```bash
python eval.py
```

## Conservative compute policy

This copy is tuned to avoid sustained overload:

- use `workers=1` for heavy compliance reruns unless there is a clear reason to fan out
- GPU is optional and intended for batch scoring, not long-running brute force
- CP-SAT and tail refinement are curtailed once a verified solution is already good enough for the baseline rule

## Results layout

Active files remain directly under [`results`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results), while older outputs are archived under:

- [`results/archive/n_le_15`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_le_15)
- [`results/archive/n_eq_16`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_eq_16)
- [`results/archive/n_lt_16`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_lt_16)
- [`results/archive/tmp`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/tmp)
- [`results/archive/research`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/research)
- [`results/archive/misc`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/misc)

## Notes

- `n <= 15` is the active acceptance scope.
- `n = 16` remains isolated and is not mixed into the `n <= 15` acceptance logic.
- Historical reports were archived rather than discarded so optimization work remains auditable.
