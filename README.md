# An Optimal Samples Selection System

A GUI-based solver for the **Covering Design** combinatorial optimization problem: given parameters $(m, n, k, j, s)$, find the minimum number of $k$-subsets (groups) of an $n$-element sample pool such that every $j$-subset is covered by at least one group with $\geq s$ common elements.

This is equivalent to the classical covering design $C(n, k, t)$ when $s = j = t$.

---

## Problem Definition

Given:
- **m** — population size (45–54), the universe from which samples are drawn
- **n** — sample pool size (7–25), a random or manually chosen subset of the population
- **k** — group size (4–7), each constructed group has exactly $k$ elements
- **j** — test subset size ($s \leq j \leq k$)
- **s** — minimum intersection threshold (3–7)

Find the **smallest** collection of $k$-subsets of the sample pool such that every $j$-subset of the pool intersects at least one group in $\geq s$ elements.

---

## Features

- **Graphical interface** — Tkinter GUI with parameter input, progress bar, result display
- **Three solver strategies** — incremental greedy, heuristic greedy, local search + simulated annealing post-processing
- **Multi-attempt randomization** — runs multiple attempts and keeps the best result
- **Result persistence** — SQLite database storage and retrieval via DB Browser
- **Theoretical validation** — Schönheim lower bound, volume lower bound, LJCR known-best values
- **Print support** — export results to file

---

## Project Structure

```
ai_homework/
├── main.py                         # Entry point
├── app.py                          # Tkinter GUI
├── solver.py                       # Core solver (greedy + SA)
├── bounds.py                       # Theoretical bounds + LJCR dataset
├── database.py                     # SQLite result storage
├── requirements.txt                # Python dependencies
├── SOLUTION.md                     # Detailed algorithm documentation (Chinese)
├── MANUAL_TEST_REFERENCE.txt       # 186 LJCR test cases with expected results
└── tests/
    ├── ljcr_dataset.py             # LJCR dataset (186 entries, proven/best-known)
    ├── test_ljcr_dataset.py        # LJCR-based test runner
    ├── test_solver.py              # 8 PDF ground-truth examples
    ├── test_perf.py                # 20 medium/large performance cases
    └── test_validation.py         # 34 cases vs theoretical bounds
```

---

## Requirements

- Python 3.10+
- numpy >= 1.24

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Launch the GUI

```bash
python main.py
```

### GUI Input Fields

| Field | Description | Range |
|-------|-------------|-------|
| **m** | Population size | 45–54 |
| **n** | Sample pool size | 7–25 |
| **k** | Group size | 4–7 |
| **j** | Test subset size (= t for C(n,k,t)) | s ≤ j ≤ k |
| **s** | Minimum intersection (= t for C(n,k,t)) | 3–7 |

For classical covering design $C(n, k, t)$: set **j = s = t**.

### Example — Verify C(8, 6, 4) = 7

Input: `m=45, n=8, k=6, j=4, s=4` → Expected output: **7 groups**

### Sample Modes

- **Random n** — automatically picks $n$ random elements from $\{1, \ldots, m\}$
- **Input n** — manually enter exactly $n$ comma-separated values (e.g. `3,7,12,18,22,31,45,50`)

### Buttons

| Button | Action |
|--------|--------|
| **Execute** | Run the solver |
| **Store** | Save result to SQLite database |
| **Print** | Open result in system viewer |
| **Clear** | Reset the output panel |
| **DB Browser** | Browse all stored results |

---

## Running Tests

```bash
# Quick smoke test against 25 proven-optimal LJCR values (n≤12)
python tests/test_ljcr_dataset.py --mode smoke

# Full LJCR test (all entries up to n=15)
python tests/test_ljcr_dataset.py --mode full --max-n 15

# Dataset summary
python tests/test_ljcr_dataset.py --mode summary

# 8 PDF ground-truth examples
python -m pytest tests/test_solver.py -v

# Theoretical bounds validation (34 cases)
python tests/test_validation.py
```

---

## LJCR Test Dataset

The file `tests/ljcr_dataset.py` contains **186** known covering design values from the [La Jolla Covering Repository](https://ljcr.dmgordon.org/cover/table.html) (2026-03-19), covering $n=7$–$25$, $k=4$–$7$, $t=3$–$6$.

Each entry is classified as:
- **绝对正确 (Proven optimal)** — Schönheim lower bound equals LJCR value → mathematically proven minimum (49 entries)
- **可能最优 (Best known)** — LJCR value exceeds Schönheim bound → best known but not proven optimal (137 entries)

See `MANUAL_TEST_REFERENCE.txt` for a complete table of all 186 test cases with the exact GUI input values and expected results.

---

## Algorithm Overview

The solver uses a three-phase approach:

1. **Greedy Construction** — incrementally add the $k$-subset covering the most uncovered $j$-subsets; falls back to heuristic greedy for large instances
2. **Local Search** — remove redundant groups that do not contribute unique coverage
3. **Simulated Annealing** — probabilistic swap moves to escape local optima

Multiple independent attempts are run with different random seeds; the best result is returned.

For full algorithmic details, see [SOLUTION.md](SOLUTION.md).
