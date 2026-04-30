"""Test t-covering optimization improvements."""

import time
from tcovering_solver import TCoveringSolver


def test_tcovering_case(n, k, j, s, t, time_budget=120):
    """Test a single t-covering case."""
    print(f"\n{'='*60}")
    print(f"Testing L({n},{k},{j},{s}) with t={t}")
    print(f"{'='*60}")
    
    solver = TCoveringSolver(
        n=n,
        k=k,
        j=j,
        s=s,
        t=t,
        num_attempts=3,
        time_budget_sec=time_budget,
    )
    
    start = time.time()
    result = solver.solve()
    elapsed = time.time() - start
    
    print(f"\nResult:")
    print(f"  Groups: {result.num_groups}")
    print(f"  Time: {elapsed:.2f}s")
    print(f"  First legal: {result.first_legal_elapsed:.2f}s" if result.first_legal_elapsed else "  No solution found")
    print(f"  Verified: {result.verified}")
    
    if result.num_groups > 0:
        print(f"  ✓ Solution found")
    else:
        print(f"  ✗ No solution found")
    
    return result


def main():
    """Run t-covering optimization tests."""
    print("T-Covering Optimization Test Suite")
    print("="*60)
    
    # Test cases from small to large
    test_cases = [
        # Small cases (should be fast)
        (8, 4, 4, 3, 2, 30),   # L(8,4,4,3) t=2
        (9, 5, 4, 3, 2, 60),   # L(9,5,4,3) t=2
        
        # Medium cases
        (10, 5, 4, 3, 2, 90),  # L(10,5,4,3) t=2
        (11, 5, 4, 3, 2, 120), # L(11,5,4,3) t=2
        
        # Large cases (challenging)
        (12, 6, 5, 4, 2, 120), # L(12,6,5,4) t=2
        (13, 6, 5, 4, 2, 120), # L(13,6,5,4) t=2
    ]
    
    results = []
    for n, k, j, s, t, budget in test_cases:
        try:
            result = test_tcovering_case(n, k, j, s, t, budget)
            results.append((n, k, j, s, t, result.num_groups, result.elapsed))
        except Exception as e:
            print(f"  ✗ Error: {e}")
            results.append((n, k, j, s, t, -1, -1))
    
    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    print(f"{'Case':<20} {'Groups':<10} {'Time':<10} {'Status'}")
    print("-"*60)
    
    for n, k, j, s, t, groups, elapsed in results:
        case_str = f"L({n},{k},{j},{s}) t={t}"
        if groups > 0:
            status = "✓ OK" if elapsed < 120 else "⚠ SLOW"
            print(f"{case_str:<20} {groups:<10} {elapsed:>8.2f}s {status}")
        else:
            print(f"{case_str:<20} {'FAILED':<10} {elapsed:>8.2f}s ✗ FAIL")


if __name__ == "__main__":
    main()
