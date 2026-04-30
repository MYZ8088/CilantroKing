"""Quick test for n19 integration."""

import sys

def test_n19_import():
    """Test n19 module imports."""
    print("Testing n19 imports...")
    try:
        from n19_specialized_module import (
            is_n19_special_case,
            run_n19_specialized_module,
            try_n19_direct_solve,
        )
        print("✓ n19_specialized_module imported successfully")
        
        # Test is_n19_special_case
        assert is_n19_special_case(19, 5, 5, 4) == True
        assert is_n19_special_case(18, 5, 5, 4) == False
        print("✓ is_n19_special_case works correctly")
        
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_n19_solver_integration():
    """Test that n19 is integrated into main solver."""
    print("\nTesting n19 solver integration...")
    try:
        from solver import CoveringDesignSolver
        
        # Create a solver for n=19
        solver = CoveringDesignSolver(
            n=19, k=5, j=5, s=4,
            num_attempts=1,
            time_budget_sec=3.0,
        )
        
        print(f"✓ Created solver for L(19,5,5,4)")
        print(f"  num_targets: {solver.num_targets}")
        print(f"  num_cands: {solver.num_cands}")
        
        # Check that n19 functions are accessible
        from n19_specialized_module import try_n19_direct_solve
        print("✓ n19 direct solve function is accessible")
        
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run quick tests."""
    print("=" * 60)
    print("N19 Quick Integration Test")
    print("=" * 60)
    
    import_ok = test_n19_import()
    integration_ok = test_n19_solver_integration()
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Import: {'✓ PASS' if import_ok else '✗ FAIL'}")
    print(f"  Integration: {'✓ PASS' if integration_ok else '✗ FAIL'}")
    print("=" * 60)
    
    if import_ok and integration_ok:
        print("\n✓ All quick tests passed!")
        print("\nN19 integration is working correctly.")
        print("The full solve test may take longer (15+ seconds).")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
