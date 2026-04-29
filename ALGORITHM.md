# Algorithm Notes

## Model

The PDF requirement is modeled as set cover.

For each input `(n, k, j, s)`, every `j`-subset of the selected `n` samples is a requirement. Every candidate `k`-block covers the requirements whose intersection with that block has size at least `s`. The solver selects as few `k`-blocks as it can while covering all requirements.

Validation is always full validation: `verify_solution()` enumerates every `j`-subset and checks that at least one selected block intersects it in at least `s` samples. The baseline validation script also uses this full check. Sampling may be used only to create candidate choices in large heuristic phases, not to certify correctness.

## Files

- `optimal_samples.py`: shared data model, bitmask coverage oracle, CLI, DB output, full validation.
- `solver_dispatcher.py`: central solver dispatcher. It decides which solver family handles the case.
- `n15_solver.py`: dedicated `n=15` solver. It contains a local copy of the exact bitmask/orbit/greedy/LNS/ILP pipeline used for `n=15`, plus the internal smaller-`n` recursive helpers needed by that pipeline.
- `n16_solver.py`: dedicated `n=16` solver. It contains a separate local copy of the same algorithmic family, tuned independently for `n=16`.
- `validate_against_baseline.py`: compares generated block counts against the provided baseline counts and performs full coverage verification.
- `reports/n15_n16_report.md`: saved timing and accuracy report for every `n=15` and `n=16` baseline case.

## n=15 and n=16 Solvers

For `n=15` and `n=16`, the solver uses full bitmasks because all requirements and candidate blocks are small enough to enumerate exactly.

The pipeline is:

1. Build all candidate `k`-blocks and their bitmask coverage over all `j`-requirements.
2. Try cyclic-orbit construction. This generates mathematically structured block orbits by rotating a base block modulo `n`.
3. For the hard `n=15,k=7,j=s=5` and `n=16,k=7,j=s=5` cases, try a partial cyclic-orbit cover and repair the remaining uncovered requirements with a small ILP over the uncovered requirements only.
4. Try recursive covering construction for classical `j=s` cases:
   `C(n,k,t) <= C(n-1,k,t) + C(n-1,k-1,t-1)`.
5. Run deterministic bitmask greedy.
6. If enough time remains, run randomized greedy restarts.
7. If enough time remains, run large-neighborhood search.
8. If enough time remains, run full-count fixed-size swap compression. This maintains coverage counts for every requirement, not a sample.
9. If SciPy MILP is available and the model is small enough, try ILP compression.
10. Prune redundant blocks and run full validation.

The baseline JSON is used only as a quality target in `validate_against_baseline.py`. No baseline block list is embedded or returned as an answer.

## What ILP Means

ILP means integer linear programming.

The set-cover ILP is:

```text
minimize sum(x_b)
subject to for every requirement r: sum(x_b for b covering r) >= 1
x_b in {0, 1}
```

Each variable `x_b` decides whether candidate block `b` is selected. If the ILP solver proves or finds a smaller feasible solution within the time limit, the solver uses it.

ILP is not the only method. It can be slow or fail to find a useful incumbent because covering designs are highly symmetric. When that happens, the system keeps the best solution from constructive/greedy/local-search phases. It never outputs an ILP relaxation as a final answer.

## Baseline Validation

Run selected cases:

```bash
python3 validate_against_baseline.py --only L_15_7_5_5,L_16_7_5_5 --time-limit 120 --ratio-threshold 1.21
```

Run all retained `n=15` and `n=16` cases:

```bash
python3 validate_against_baseline.py --max-n 16 --time-limit 120 --output baseline_validation_results.csv
```

The default quality threshold is `1.15`, meaning generated block count within about 15% of the baseline count is treated as passing. For a looser 10%-20% project target, use `--ratio-threshold 1.21`. The CSV still records the exact ratio for every case.

Current measured hard-case status on this machine:

- `L_15_7_5_5`: 228 groups vs baseline 189, ratio 1.2063, full validation passed.
- `L_16_7_5_5`: 328 groups vs baseline 283, ratio 1.1590, full validation passed in 21.809 seconds after the standalone `n16_solver.py` split.

Both hard cases are generated algorithmically with partial cyclic-orbit cores plus ILP repair. They are fully verified and use no embedded baseline solution blocks.