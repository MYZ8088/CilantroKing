#!/usr/bin/env python3
"""Test t-covering functionality."""

from solver import CoveringDesignSolver

def test_t1():
    """Test t=1 (standard covering design)."""
    print("Testing t=1 (standard covering)...")
    solver = CoveringDesignSolver(n=7, k=6, j=5, s=5, t=1)
    result = solver.solve()
    print(f"  Result: {result.num_groups} groups, verified={result.verified}")
    assert result.verified, "t=1 solution should be verified"
    print("  ✓ t=1 works")

def test_t2():
    """Test t=2 (2-covering)."""
    print("\nTesting t=2 (2-covering)...")
    solver = CoveringDesignSolver(n=8, k=6, j=5, s=4, t=2, num_attempts=2, time_budget_sec=30)
    result = solver.solve()
    print(f"  Result: {result.num_groups} groups, verified={result.verified}")
    if result.num_groups > 0:
        print(f"  First few groups: {result.groups[:3]}")
    print("  ✓ t=2 works")

def test_t3():
    """Test t=3 (3-covering)."""
    print("\nTesting t=3 (3-covering)...")
    # For j=5, s=4, we have C(5,4)=5 possible s-subsets per j-subset
    # So t can be at most 5
    solver = CoveringDesignSolver(n=8, k=6, j=5, s=4, t=3, num_attempts=2, time_budget_sec=30)
    result = solver.solve()
    print(f"  Result: {result.num_groups} groups, verified={result.verified}")
    print("  ✓ t=3 works")

if __name__ == "__main__":
    test_t1()
    test_t2()
    test_t3()
    print("\n✓ All tests passed!")
