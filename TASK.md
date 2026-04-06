# Iterative Solver Improvement Task

## Context

This repository solves covering-design instances `L(n, k, j, s)` by finding as
few `k`-subsets as possible while still covering every `j`-subset with
intersection size at least `s`.

The current branch restores the implementation from GitHub PR #1:
"Optimize solver for Windows and optional CUDA GPU scoring".
That PR improved runtime, especially on larger Windows cases, while keeping the
same solver contract and full verification step. It was later reverted from
`main`, so this branch is the active optimization baseline.

## Objective

Improve the solver in `solver.py` without breaking correctness.

When judging whether a change is better, use this order:

1. Keep every benchmark case verified.
2. Reduce the number of groups returned by the solver.
3. Improve weighted quality against exact values, LJCR values, or lower bounds.
4. Reduce runtime, but not by sacrificing quality without saying so.

## Reference Rules

- `exact`: use PDF / README ground-truth values when they are known.
- `ljcr`: use La Jolla Covering Repository values for containment cases
  (`s == j`).
- `lower_bound`: use `bounds.best_lower_bound(...)` for non-containment cases.

## Workflow

1. Read `AGENTS.md`.
2. Make one focused change.
3. Run `python eval.py --suite smoke` while exploring.
4. Run `python eval.py --suite core` before claiming an improvement.
5. Inspect `results/latest_eval.json`.
6. Compare it against `results/baseline.json`.
7. Only update the baseline after the user agrees that the new behavior should
   become the new target.

## Guardrails

- Preserve the current parameter contract:
  - `7 <= n <= 25`
  - `4 <= k <= 7`
  - `3 <= s <= 7`
  - `s <= j <= k`
- Do not remove or bypass solver verification.
- Do not change the benchmark set, seeds, scoring formula, or reference values
  just to make the score look better.
- Do not special-case benchmark case IDs inside the solver.
- If a change improves quality but materially hurts runtime, say that clearly.

## Current Baseline Files

- Benchmarks: `benchmark_cases.json`
- Latest run: `results/latest_eval.json` (usually the day-to-day `core` suite)
- Stable baseline: `results/baseline.json` (currently a `full` suite snapshot)

The evaluator compares runs by overlapping case IDs, so a `core` run can still
be compared against a `full` baseline.
