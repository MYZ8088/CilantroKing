"""Comprehensive validation: compare solver results against theoretical bounds and LJCR."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import time
from math import comb

from bounds import best_lower_bound, get_bounds, ljcr_known_best
from solver import CoveringDesignSolver


# All parameter combos within the project spec: n=7..25, k=4..7, s<=j<=k, 3<=s<=7
# We test a representative subset covering all strategy paths
TEST_CASES: list[tuple[int, int, int, int, str]] = [
    # --- PDF examples (known optimal) ---
    (7, 6, 5, 5, "PDF-1"),
    (8, 6, 5, 5, "PDF-2"),
    (8, 6, 4, 4, "PDF-3"),
    (9, 6, 4, 4, "PDF-4"),
    (8, 6, 6, 5, "PDF-5"),
    (9, 6, 5, 4, "PDF-6"),
    (10, 6, 6, 4, "PDF-7"),
    (12, 6, 6, 4, "PDF-8"),
    # --- Containment s==j (LJCR ground truth available) ---
    (10, 6, 4, 4, "LJCR-1"),
    (12, 6, 4, 4, "LJCR-2"),
    (15, 6, 4, 4, "LJCR-3"),
    (10, 6, 5, 5, "LJCR-4"),
    (12, 6, 5, 5, "LJCR-5"),
    (15, 6, 5, 5, "LJCR-6"),
    (10, 6, 3, 3, "LJCR-7"),
    (12, 6, 3, 3, "LJCR-8"),
    (15, 6, 3, 3, "LJCR-9"),
    # --- Non-containment (s<j, volume bound only) ---
    (10, 6, 5, 4, "NC-1"),
    (10, 6, 5, 3, "NC-2"),
    (12, 6, 5, 4, "NC-3"),
    (15, 6, 5, 4, "NC-4"),
    (15, 6, 6, 5, "NC-5"),
    (12, 6, 6, 5, "NC-6"),
    # --- Larger (performance + quality) ---
    (18, 6, 5, 4, "LG-1"),
    (18, 6, 5, 5, "LG-2"),
    (20, 6, 5, 5, "LG-3"),
    (20, 6, 6, 4, "LG-4"),
    # --- Different k values ---
    (8, 4, 4, 3, "k4-1"),
    (10, 4, 4, 4, "k4-2"),
    (8, 5, 4, 4, "k5-1"),
    (10, 5, 5, 5, "k5-2"),
    (8, 7, 5, 5, "k7-1"),
    (10, 7, 6, 6, "k7-2"),
    (12, 7, 5, 5, "k7-3"),
]


def run_validation(timeout: float = 120.0) -> None:
    max_cases = int(sys.argv[1]) if len(sys.argv) > 1 else len(TEST_CASES)

    print("=" * 90)
    print("Covering Design Solver Validation")
    print("=" * 90)
    print(f"{'Case':<8} {'L(n,k,j,s)':<16} {'Result':>7} {'LB':>6} {'LJCR':>6} "
          f"{'Ratio':>7} {'Grade':>6} {'Time':>7} {'OK':>3}")
    print("-" * 90)

    total = 0
    passed = 0
    grades: list[float] = []

    for n, k, j, s, desc in TEST_CASES[:max_cases]:
        total += 1
        t0 = time.time()
        bounds = get_bounds(n, k, j, s)
        lb = bounds["lower_bound"]
        ljcr = bounds.get("ljcr_best")

        try:
            solver = CoveringDesignSolver(
                n=n, k=k, j=j, s=s, num_attempts=3,
                cancel_fn=lambda: (time.time() - t0) > timeout,
            )
            result = solver.solve()
            elapsed = time.time() - t0
            got = result.num_groups
            verified = result.verified

            # Quality ratio: 1.0 = optimal (matching lower bound)
            if ljcr is not None:
                ratio = got / ljcr
                ratio_str = f"{ratio:.3f}"
            else:
                ratio = got / lb if lb > 0 else float("inf")
                ratio_str = f"~{ratio:.2f}"

            # Grade: A = within 10% of best known, B = within 25%, C = within 50%, D = worse
            if ljcr is not None:
                if got <= ljcr:
                    grade = "A+"
                elif got <= ljcr * 1.1:
                    grade = "A"
                elif got <= ljcr * 1.25:
                    grade = "B"
                elif got <= ljcr * 1.5:
                    grade = "C"
                else:
                    grade = "D"
            else:
                if ratio <= 1.5:
                    grade = "A~"
                elif ratio <= 2.0:
                    grade = "B~"
                elif ratio <= 3.0:
                    grade = "C~"
                else:
                    grade = "D~"

            ok = "✓" if verified else "✗"
            if verified:
                passed += 1
                grades.append(ratio)

            ljcr_str = str(ljcr) if ljcr is not None else "-"
            print(f"{desc:<8} L({n},{k},{j},{s}){'':<{8-len(f'{n},{k},{j},{s}')}} "
                  f"{got:>7} {lb:>6} {ljcr_str:>6} "
                  f"{ratio_str:>7} {grade:>6} {elapsed:>6.1f}s {ok:>3}")

        except Exception as exc:
            elapsed = time.time() - t0
            ljcr_str = str(ljcr) if ljcr is not None else "-"
            print(f"{desc:<8} L({n},{k},{j},{s}){'':<{8-len(f'{n},{k},{j},{s}')}} "
                  f"{'ERR':>7} {lb:>6} {ljcr_str:>6} "
                  f"{'---':>7} {'---':>6} {elapsed:>6.1f}s {'✗':>3}  {exc}")

    print("-" * 90)
    print(f"Verified: {passed}/{total}")
    if grades:
        avg = sum(grades) / len(grades)
        best_r = min(grades)
        worst_r = max(grades)
        print(f"Quality ratio (vs LJCR/LB): avg={avg:.3f}, best={best_r:.3f}, worst={worst_r:.3f}")
        a_count = sum(1 for r in grades if r <= 1.1)
        b_count = sum(1 for r in grades if 1.1 < r <= 1.25)
        c_count = sum(1 for r in grades if 1.25 < r <= 1.5)
        d_count = sum(1 for r in grades if r > 1.5)
        print(f"Grades: A={a_count}, B={b_count}, C={c_count}, D={d_count}")


if __name__ == "__main__":
    run_validation()
