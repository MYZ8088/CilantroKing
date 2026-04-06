# Agent Workflow Notes

This repo uses a benchmark-driven optimization loop.

## Read First

Before editing solver logic, read:

1. `TASK.md`
2. `benchmark_cases.json`
3. `results/baseline.json`
4. `results/latest_eval.json` if it exists

## Required Loop

1. Make one narrow change at a time.
2. Prefer improving solution quality first, then runtime.
3. Run `python eval.py --suite smoke` during exploration.
4. Run `python eval.py --suite core` before reporting a win.
5. Treat `results/latest_eval.json` as the source of truth for the current run.

## Regression Rules

Treat the change as a regression if any of the following happens:

- a previously verified benchmark case becomes unverified
- weighted quality ratio gets worse
- group count gets worse on an important benchmark without a clearly stronger
  improvement elsewhere

Use runtime as a tiebreaker after correctness and quality.

## Anti-Gaming Rules

Unless the user explicitly asks for it, do not:

- edit `benchmark_cases.json`
- edit `results/baseline.json`
- change the scoring formula in `eval.py`
- increase `num_attempts` or timeouts only to inflate results
- disable GPU or CPU paths only for selected benchmark cases
- skip failed benchmark cases in the final summary

## Promotion Rule

Only promote a new baseline when the user asks or clearly approves it.

The normal command for that is:

```bash
python eval.py --suite full --write-baseline
```

`results/baseline.json` is allowed to be broader than `results/latest_eval.json`.
When suites differ, compare only the overlapping case IDs.

## Useful Commands

```bash
python eval.py --suite smoke
python eval.py --suite core
python eval.py --suite full
python tests/test_solver.py
```
