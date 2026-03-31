"""Performance and stress tests for larger parameter combinations."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import time
from solver import CoveringDesignSolver


TEST_CASES = [
    # (n, k, j, s, description)
    (7, 6, 5, 5, "E.g.1"),
    (8, 6, 5, 5, "E.g.2"),
    (8, 6, 4, 4, "E.g.3"),
    (9, 6, 4, 4, "E.g.4"),
    (8, 6, 6, 5, "E.g.5"),
    (9, 6, 5, 4, "E.g.7"),
    (10, 6, 6, 4, "E.g.8"),
    (12, 6, 6, 4, "E.g.9"),
    # Medium cases
    (10, 6, 5, 5, "Medium-1"),
    (12, 6, 5, 5, "Medium-2"),
    (10, 6, 4, 3, "Medium-3"),
    (12, 6, 5, 4, "Medium-4"),
    (15, 6, 5, 4, "Medium-5"),
    (15, 6, 6, 4, "Medium-6"),
    # Larger cases
    (18, 6, 5, 4, "Large-1"),
    (20, 6, 6, 4, "Large-2"),
    (15, 6, 4, 4, "Large-3"),
    # Different k values
    (8, 5, 4, 4, "k=5 test"),
    (8, 7, 5, 5, "k=7 test"),
    (8, 4, 4, 3, "k=4 test"),
]


def run_test(n: int, k: int, j: int, s: int, desc: str,
             timeout: float = 120.0) -> None:
    t0 = time.time()
    try:
        solver = CoveringDesignSolver(
            n=n, k=k, j=j, s=s,
            num_attempts=3,
            cancel_fn=lambda: (time.time() - t0) > timeout,
        )
        result = solver.solve()
        elapsed = time.time() - t0
        status = "✓" if result.verified else "✗"
        print(f"  {status} {desc:12s}  L({n},{k},{j},{s}): "
              f"{result.num_groups:4d} groups  {elapsed:7.2f}s  "
              f"(targets={solver.num_targets}, cands={solver.num_cands})")
    except Exception as exc:
        elapsed = time.time() - t0
        print(f"  ✗ {desc:12s}  L({n},{k},{j},{s}): ERROR {exc}  {elapsed:.2f}s")


def main() -> None:
    max_cases = int(sys.argv[1]) if len(sys.argv) > 1 else len(TEST_CASES)
    print(f"Running {max_cases} test cases (timeout=120s each):\n")
    for i, (n, k, j, s, desc) in enumerate(TEST_CASES[:max_cases]):
        run_test(n, k, j, s, desc)
    print("\nDone.")


if __name__ == "__main__":
    main()
