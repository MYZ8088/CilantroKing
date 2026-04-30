"""Test script to verify n17/n18/n19 specialized modules are properly integrated."""

import sys
import time


def test_imports():
    """Test that all specialized modules can be imported."""
    print("Testing imports...")
    
    try:
        from n17_specialized_module import is_n17_special_case, run_n17_specialized_module
        print("✓ n17_specialized_module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import n17_specialized_module: {e}")
        return False
    
    try:
        from n18_specialized_module import is_n18_special_case, run_n18_specialized_module
        print("✓ n18_specialized_module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import n18_specialized_module: {e}")
        return False
    
    try:
        from n19_specialized_module import is_n19_special_case, run_n19_specialized_module
        print("✓ n19_specialized_module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import n19_specialized_module: {e}")
        return False
    
    return True


def test_n17_case():
    """Test an n=17 case."""
    print("\nTesting n=17 case: L(17,5,3,3)...")
    
    try:
        from solver import CoveringDesignSolver
        
        # Use a simpler case with longer timeout
        solver = CoveringDesignSolver(
            n=17, k=5, j=3, s=3,
            num_attempts=1,
            time_budget_sec=15.0,
        )
        
        print("  Solving...")
        result = solver.solve()
        print(f"✓ L(17,5,3,3) solved: {result.num_groups} groups, verified={result.verified}")
        print(f"  Elapsed: {result.elapsed:.2f}s")
        print(f"  Route: {result.route_module or 'main solver'}")
        
        # Check that it's using algorithm, not hardcoded
        if result.solution_source == "hardcoded":
            print("✗ WARNING: Solution is hardcoded!")
            return False
        else:
            print(f"  Solution source: {result.solution_source}")
        
        return result.verified
    except KeyboardInterrupt:
        print("✗ Test interrupted by user")
        return False
    except Exception as e:
        print(f"✗ Failed to solve L(17,5,3,3): {e}")
        import traceback
        traceback.print_exc()
        return False


def test_n18_case():
    """Test an n=18 case."""
    print("\nTesting n=18 case: L(18,5,5,4)...")
    
    try:
        from solver import CoveringDesignSolver
        
        solver = CoveringDesignSolver(
            n=18, k=5, j=5, s=4,
            num_attempts=1,
            time_budget_sec=15.0,
        )
        
        print("  Solving...")
        result = solver.solve()
        print(f"✓ L(18,5,5,4) solved: {result.num_groups} groups, verified={result.verified}")
        print(f"  Elapsed: {result.elapsed:.2f}s")
        print(f"  Route: {result.route_module or 'main solver'}")
        print(f"  Solution source: {result.solution_source}")
        
        return result.verified
    except KeyboardInterrupt:
        print("✗ Test interrupted by user")
        return False
    except Exception as e:
        print(f"✗ Failed to solve L(18,5,5,4): {e}")
        import traceback
        traceback.print_exc()
        return False


def test_n19_case():
    """Test an n=19 case."""
    print("\nTesting n=19 case: L(19,5,5,4)...")
    
    try:
        from solver import CoveringDesignSolver
        
        solver = CoveringDesignSolver(
            n=19, k=5, j=5, s=4,
            num_attempts=1,
            time_budget_sec=15.0,
        )
        
        print("  Solving...")
        result = solver.solve()
        print(f"✓ L(19,5,5,4) solved: {result.num_groups} groups, verified={result.verified}")
        print(f"  Elapsed: {result.elapsed:.2f}s")
        print(f"  Route: {result.route_module or 'main solver'}")
        print(f"  Solution source: {result.solution_source}")
        
        return result.verified
    except KeyboardInterrupt:
        print("✗ Test interrupted by user")
        return False
    except Exception as e:
        print(f"✗ Failed to solve L(19,5,5,4): {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("N17/N18/N19 Integration Test")
    print("=" * 60)
    
    # Test imports
    if not test_imports():
        print("\n✗ Import test failed!")
        return 1
    
    # Test n17
    n17_ok = test_n17_case()
    
    # Test n18
    n18_ok = test_n18_case()
    
    # Test n19
    n19_ok = test_n19_case()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  N17: {'✓ PASS' if n17_ok else '✗ FAIL'}")
    print(f"  N18: {'✓ PASS' if n18_ok else '✗ FAIL'}")
    print(f"  N19: {'✓ PASS' if n19_ok else '✗ FAIL'}")
    print("=" * 60)
    
    if n17_ok and n18_ok and n19_ok:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
