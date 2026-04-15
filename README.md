# An Optimal Samples Selection System

A modern GUI-based solver for the **Covering Design** combinatorial optimization problem: given parameters $(m, n, k, j, s)$, find the minimum number of $k$-subsets (groups) of an $n$-element sample pool such that every $j$-subset is covered by at least one group with $\geq s$ common elements.

This is equivalent to the classical covering design $C(n, k, t)$ when $s = j = t$.

## 🎨 Modern UI

The application features a clean, modern interface with:
- **Card-based design** with smooth layouts and large, readable fonts
- **Custom styled dialogs** with color-coded feedback (success/error/warning)
- **Interactive buttons** with hover effects
- **Real-time progress tracking** with visual progress bars
- **Database browser** for viewing and managing saved results
- **Run tracking** - automatically tracks multiple runs with the same parameters

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

- **Modern Graphical Interface** — Clean, card-based UI with pure Tkinter
  - Large, readable fonts (Segoe UI) with proper spacing
  - Custom styled dialogs with emoji icons and color coding
  - Smooth hover effects on interactive elements
  - Real-time progress tracking with visual feedback
- **Optimized Workflow** — Fast response with on-demand verification
  - Quick solution generation (preprocessing + algorithm time displayed)
  - Separate verification button for manual validation
  - Auto-refresh display after verification
- **Three Solver Strategies** — Incremental greedy, heuristic greedy, local search + simulated annealing
- **GPU Acceleration** — Optional CUDA support for large instances (automatic CPU fallback)
- **Multi-attempt Randomization** — Runs multiple attempts and keeps the best result
- **Result Persistence** — SQLite database with run tracking
  - Automatic run numbering for repeated parameter sets
  - Filename format: `m-n-k-j-s-runNumber-groupCount`
  - Database browser with detailed result viewing
- **Theoretical Validation** — Schönheim lower bound, volume lower bound, LJCR known-best values

---

## Project Structure

```
ai_homework/
├── main_clean.py                   # Modern UI entry point (recommended)
├── app_clean.py                    # Modern Tkinter GUI (pure tkinter)
├── main.py                         # Legacy entry point
├── app.py                          # Legacy GUI
├── solver.py                       # Core solver (greedy + SA + GPU support)
├── bounds.py                       # Theoretical bounds + LJCR dataset
├── database.py                     # SQLite result storage with run tracking
├── requirements.txt                # Python dependencies
├── SOLUTION.md                     # Detailed algorithm documentation (Chinese)
├── MANUAL_TEST_REFERENCE.txt       # 186 LJCR test cases with expected results
├── UI_IMPROVEMENTS.md              # UI development history
├── MODERN_UI_GUIDE.md              # Modern UI design guide
└── tests/
    ├── ljcr_dataset.py             # LJCR dataset (186 entries, proven/best-known)
    ├── test_ljcr_dataset.py        # LJCR-based test runner
    ├── test_solver.py              # 8 PDF ground-truth examples
    ├── test_perf.py                # 20 medium/large performance cases
    └── test_validation.py          # 34 cases vs theoretical bounds
```

---

## Requirements

- Python 3.10+
- numpy >= 1.24
- (Optional) CuPy for GPU acceleration

Install dependencies:

```bash
pip install -r requirements.txt
```

For GPU support (optional):
```bash
pip install cupy-cuda12x  # or appropriate CUDA version
```

---

## Usage

### Launch the Modern GUI (Recommended)

```bash
python main_clean.py
```

Or use the legacy interface:
```bash
python main.py
```

### GUI Workflow

1. **Set Parameters** — Enter values for m, n, k, j, s in the parameter card
2. **Select Samples** — Choose random selection or manual input
3. **Execute** — Click the Execute button to generate solution
4. **Review Summary** — View groups found and time elapsed
5. **Verify (Optional)** — Click Verify button to validate the solution
6. **Print Details** — Click Print Details to see all groups
7. **Store** — Save the result to database with automatic run numbering

### Modern UI Features

- **⚙️ Parameters Card** — Clean input fields with hints and validation
- **📊 Sample Selection** — Radio buttons for random/manual mode
- **Action Buttons**:
  - ▶ Execute — Generate solution
  - ⏹ Cancel — Stop current execution
  - 💾 Store — Save to database
  - ✓ Verify — Validate solution (on-demand)
  - 🖨 Print Details — Show all groups
  - 🗑 Clear — Reset display
  - 📁 Database Browser — View saved results
- **⏱ Progress** — Real-time progress bar and status messages
- **📋 Results** — Beautiful formatted output with emoji indicators
- **Run Tracking** — Automatic numbering: `m-n-k-j-s-runNumber-groupCount`

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
| **▶ Execute** | Run the solver with current parameters |
| **⏹ Cancel** | Stop the current execution |
| **💾 Store** | Save result to SQLite database with run tracking |
| **✓ Verify** | Validate solution (checks all targets are covered) |
| **🖨 Print Details** | Display detailed group information |
| **🗑 Clear** | Reset the output panel |
| **📁 Database Browser** | Browse, view, and delete stored results |

### Database Browser

The database browser allows you to:
- View all saved results in a list (format: `m-n-k-j-s-runNumber-groupCount`)
- Click **👁 Display** to see detailed group information
- Click **🗑 Delete** to remove a result (with confirmation dialog)
- Results are automatically tracked by run number for the same parameters

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

The solver uses a three-phase approach with GPU acceleration support:

1. **Greedy Construction** — Incrementally add the $k$-subset covering the most uncovered $j$-subsets
   - Incremental greedy with precomputed coverage tables for medium instances
   - Heuristic greedy with element-frequency scoring for large instances
   - Optional GPU batch scoring for very large problems (automatic CPU fallback)
   
2. **Local Search** — Remove redundant groups that do not contribute unique coverage
   - Brute-force removal for small solutions (≤60 groups)
   - Fast coverage-count tracking for larger solutions

3. **Simulated Annealing** — Probabilistic swap moves to escape local optima
   - Applied to medium-sized solutions (4-200 groups)
   - Time-budgeted based on instance size

Multiple independent attempts are run with different random seeds; the best result is returned.

### Performance Optimizations

- **Preprocessing Time Included** — Timer starts from initialization to accurately reflect total algorithm time
- **Skip Final Verification** — GUI mode skips automatic verification for faster response (manual verification available)
- **Adaptive Strategies** — Automatically selects best algorithm based on instance size
- **GPU Acceleration** — CuPy-based batch scoring for instances with >500M interactions
- **Memory Management** — Chunked processing to handle large instances efficiently

For full algorithmic details, see [SOLUTION.md](SOLUTION.md).

---

## Development Notes

- **UI Evolution**: See [UI_IMPROVEMENTS.md](UI_IMPROVEMENTS.md) for the complete UI development history
- **Modern Design**: See [MODERN_UI_GUIDE.md](MODERN_UI_GUIDE.md) for design principles and implementation details
- **Benchmark Testing**: Follow [AGENTS.md](AGENTS.md) workflow for solver improvements
