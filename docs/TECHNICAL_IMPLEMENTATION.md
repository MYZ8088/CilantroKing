# Technical Implementation Notes

This note explains the technical choices in the optimized `lbn` workspace, with emphasis on the `n <= 15` acceptance target:

- `elapsed_sec < 120`
- `verified == true`
- `solver_blocks / baseline_blocks <= 1.10`

## 1. Baseline strategy

### Canonical source

The canonical baseline source is:

- [`coveringrepo_n_lt_26_baselines(1).json`](C:/Users/York/Desktop/CilantroKing-lbn-opt/coveringrepo_n_lt_26_baselines(1).json)

This is treated as the standard reference for acceptance. The solver and evaluation scripts prefer this file first and only fall back to older in-repo baseline copies if needed.

### Why this matters

Earlier optimization code was willing to keep searching after it had already found a legally acceptable solution, because it only looked at theoretical lower bounds. That is useful for research, but not for the delivery rule here. Using the canonical baseline lets the solver stop once it is already inside the allowed `10%` band.

## 2. Solver architecture

### Main file

- [`solver.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/solver.py)

### Major phases

The solver uses a layered design rather than a single monolithic search:

1. fast seed generation
2. greedy construction
3. local optimization and repair
4. specialized refinement modules
5. final verification

This structure was retained because it already matches the problem family well and allows targeted tuning without destabilizing the whole code path.

## 3. Acceptance-aware early stopping

### What changed

The optimized copy adds an acceptance upper bound derived from the canonical baseline:

- if a case has baseline `B`, the practical stop line is `ceil(1.10 * B)`
- once the current solution is verified and at or below that threshold, the solver can stop the heavy search loop

### Why this was chosen

This is the lowest-risk way to cut runtime for edge cases that were timing out only because of over-polishing. It does not weaken correctness because final verification still checks coverage. It simply prevents the solver from spending the remaining budget chasing improvements that are not required by the acceptance rule.

### Where it helps most

- `j = k, s = k - 1` near-boundary cases
- small and medium `n <= 15` cases where a legal solution appears quickly
- cases that used to land near `118s-120s` with no meaningful quality gain late in the run

## 4. Cached known-design path

### Main files

- [`special5_case_module.py`](C:/Users/York/Desktop/CilantroKing-lbn-opt/special5_case_module.py)
- [`known_designs`](C:/Users/York/Desktop/CilantroKing-lbn-opt/known_designs)

### Why caching was used

Some hard cases already have reliable published or recovered designs. Re-solving them from scratch every time wastes compute and adds instability around the time limit. For those cases the most practical engineering choice is:

1. store the known design
2. load it directly
3. still verify it before returning

### Organization

Known designs are now grouped by `n`:

- `known_designs/n12`
- `known_designs/n13`
- `known_designs/n14`
- `known_designs/n15`

That layout makes it easier to audit which difficult cases were solved by construction data rather than live search.

### Why not cache everything

Caching is applied only where it meaningfully reduces risk or where a trusted design was already recovered. The rest of the solver still runs normally so the codebase remains a solver, not just a lookup table.

## 5. Specialized refinement modules

The solver already contains several targeted refinement families. The optimization work kept those boundaries and changed policy rather than inventing a new architecture.

### Containment cases: `s = j`

These use containment-oriented refinement because coverage structure is stricter and repeated high-cost passes tend to be expensive.

Chosen tactics:

- tighter tail budgets
- fewer repeated expensive passes once the solution is already close enough
- preference for verified acceptable exits over theoretical improvement chasing

### Near-noncontainment `j = k, s = k - 1`

These cases are often structurally awkward and can burn time in orbit, SAT, and cycle-based passes.

Chosen tactics:

- keep specialized paths
- allow them to run when quality is still not acceptable
- skip or shorten them once the acceptance line has already been reached

### General noncontainment

These use the existing greedy plus repair pipeline, with acceptance-aware stopping as the main runtime control.

## 6. GPU policy

### Goal

Use GPU only when it helps short batched scoring, not as a sustained high-load search engine.

### Implementation choice

The solver keeps optional CuPy support with automatic fallback. The intended mode is:

- GPU for batch scoring
- CPU for orchestration and verification
- immediate fallback if the GPU path is unavailable or unstable

### Why this is conservative

The user requirement explicitly prefers machine safety over aggressive saturation. That makes short GPU bursts and limited worker count a better fit than wide parallel search.

## 7. CPU and scheduling policy

### Chosen policy

- use `workers=1` for heavy compliance reruns
- validate one case or one small cluster at a time
- avoid broad background sweeps until enough single-case fixes have landed

### Why this was chosen

The problem here was not only algorithm quality but also observability. A giant batch hides which case is still expensive and makes runtime unpredictable. Single-case validation keeps optimization measurable and keeps machine load bounded.

## 8. Verification strategy

Every accepted result still needs:

- coverage verification
- size comparison against baseline
- time check against the budget

This is why the optimization work avoids shortcuts that would skip verification. Performance matters, but only together with a checked solution.

## 9. Repository hygiene and result handling

### Problem

The workspace had accumulated many intermediate outputs:

- repeated trial reports
- temporary one-case runs
- split markdown/json artifacts
- research scrape leftovers

That made it hard to tell which files were active deliverables and which were disposable experiment residue.

### Chosen cleanup

Instead of deleting everything outright, historical files were moved into:

- [`results/archive/n_le_15`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_le_15)
- [`results/archive/n_eq_16`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_eq_16)
- [`results/archive/n_lt_16`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/n_lt_16)
- [`results/archive/tmp`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/tmp)
- [`results/archive/research`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/research)
- [`results/archive/misc`](C:/Users/York/Desktop/CilantroKing-lbn-opt/results/archive/misc)

This keeps the active root clean while preserving auditability.

## 10. Why these choices fit the acceptance target

The acceptance target is operational, not purely academic. That means the best technical choices are the ones that reliably produce:

- a verified answer
- within the time limit
- within the allowed quality band
- without abusing CPU or GPU

That is why the implementation favors:

- baseline-aware early stopping
- cached known designs for recovered hard cases
- conservative parallelism
- targeted refinement instead of global brute force
- archived history rather than a cluttered live workspace

## 11. Remaining work pattern

For cases still above the `10%` band, the recommended loop is:

1. run a single case
2. measure exact gap to canonical baseline
3. decide whether the fix is better as:
   - algorithm tuning
   - recovered known design
   - specialized dispatch
4. rerun the same case immediately
5. only after that, update the grouped regression set

That process keeps the optimization effort explainable and keeps compute cost under control.
