"""Tests verifying solver against the PDF examples."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from solver import CoveringDesignSolver


def _run(n: int, k: int, j: int, s: int, expected_max: int) -> int:
    """Run solver and verify coverage; return number of groups found."""
    solver = CoveringDesignSolver(n=n, k=k, j=j, s=s, num_attempts=5)
    result = solver.solve()
    assert result.verified, f"L({n},{k},{j},{s}): coverage verification failed!"
    print(f"  L({n},{k},{j},{s}): {result.num_groups} groups "
          f"(optimal ≤ {expected_max}) [{result.elapsed:.2f}s]")
    return result.num_groups


def test_eg1():
    """E.g.1: n=7, k=6, j=5, s=5 → ≤ 6 groups."""
    g = _run(7, 6, 5, 5, 6)
    assert g <= 7, f"Too many groups: {g}"


def test_eg3():
    """E.g.3: n=8, k=6, j=4, s=4 → ≤ 7 groups."""
    g = _run(8, 6, 4, 4, 7)
    assert g <= 8


def test_eg5():
    """E.g.5: n=8, k=6, j=6, s=5 → ≤ 4 groups."""
    g = _run(8, 6, 6, 5, 4)
    assert g <= 5


def test_eg7():
    """E.g.7: n=9, k=6, j=5, s=4 → ≤ 3 groups."""
    g = _run(9, 6, 5, 4, 3)
    assert g <= 4


def test_eg8():
    """E.g.8: n=10, k=6, j=6, s=4 → ≤ 3 groups."""
    g = _run(10, 6, 6, 4, 3)
    assert g <= 4


def test_eg9():
    """E.g.9: n=12, k=6, j=6, s=4 → ≤ 6 groups."""
    g = _run(12, 6, 6, 4, 6)
    assert g <= 7


def test_eg2():
    """E.g.2: n=8, k=6, j=5, s=5 → ≤ 12 groups."""
    g = _run(8, 6, 5, 5, 12)
    assert g <= 14


def test_eg4():
    """E.g.4: n=9, k=6, j=4, s=4 → ≤ 12 groups."""
    g = _run(9, 6, 4, 4, 12)
    assert g <= 14


if __name__ == "__main__":
    tests = [test_eg1, test_eg3, test_eg5, test_eg7, test_eg8, test_eg9,
             test_eg2, test_eg4]
    print("Running verification tests against PDF examples:\n")
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {t.__doc__} -- {e}")
        except Exception as e:
            print(f"  ERROR: {t.__doc__} -- {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
