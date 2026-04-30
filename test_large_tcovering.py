"""Test large t-covering instances to verify optimizations."""

import time
from n_algorithms.shared.solver_core import CoveringDesignSolver

def test_large_instance():
    """Test L(20,6,5,4) t=4 - very large instance."""
    print("=" * 80)
    print("Testing L(20,6,5,4) t=4 - Very Large Instance")
    print("=" * 80)
    
    n, k, j, s, t = 20, 6, 5, 4, 4
    time_budget = 120.0
    
    print(f"\nParameters: n={n}, k={k}, j={j}, s={s}, t={t}")
    print(f"Time budget: {time_budget}s")
    
    def progress_callback(prog):
        print(f"[{prog.elapsed:.1f}s] {prog.phase}: {prog.message}")
    
    start = time.time()
    
    try:
        solver = CoveringDesignSolver(
            n=n, k=k, j=j, s=s, t=t,
            progress_cb=progress_callback,
            num_attempts=5,
            time_budget_sec=time_budget,
        )
        
        result = solver.solve()
        elapsed = time.time() - start
        
        print("\n" + "=" * 80)
        print("RESULT")
        print("=" * 80)
        print(f"Groups found: {result.num_groups}")
        print(f"Time elapsed: {elapsed:.2f}s")
        print(f"First legal at: {result.first_legal_elapsed:.2f}s" if result.first_legal_elapsed else "N/A")
        print(f"Verified: {result.verified}")
        
        if elapsed <= time_budget:
            print(f"\n✅ SUCCESS: Completed within time budget ({elapsed:.2f}s / {time_budget}s)")
        else:
            print(f"\n⚠️ TIMEOUT: Exceeded time budget ({elapsed:.2f}s / {time_budget}s)")
        
        # Show first few groups
        if result.groups:
            print(f"\nFirst 3 groups:")
            for i, group in enumerate(result.groups[:3]):
                print(f"  Group {i+1}: {group}")
        
        return result
        
    except Exception as e:
        elapsed = time.time() - start
        print(f"\n❌ ERROR after {elapsed:.2f}s: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_medium_instance():
    """Test L(16,6,5,4) t=3 - medium instance."""
    print("\n" + "=" * 80)
    print("Testing L(16,6,5,4) t=3 - Medium Instance")
    print("=" * 80)
    
    n, k, j, s, t = 16, 6, 5, 4, 3
    time_budget = 120.0
    
    print(f"\nParameters: n={n}, k={k}, j={j}, s={s}, t={t}")
    print(f"Time budget: {time_budget}s")
    
    def progress_callback(prog):
        if prog.iteration % 50 == 0 or prog.phase in ["start", "complete", "improve", "timeout"]:
            print(f"[{prog.elapsed:.1f}s] {prog.phase}: {prog.message}")
    
    start = time.time()
    
    try:
        solver = CoveringDesignSolver(
            n=n, k=k, j=j, s=s, t=t,
            progress_cb=progress_callback,
            num_attempts=5,
            time_budget_sec=time_budget,
        )
        
        result = solver.solve()
        elapsed = time.time() - start
        
        print("\n" + "=" * 80)
        print("RESULT")
        print("=" * 80)
        print(f"Groups found: {result.num_groups}")
        print(f"Time elapsed: {elapsed:.2f}s")
        print(f"First legal at: {result.first_legal_elapsed:.2f}s" if result.first_legal_elapsed else "N/A")
        
        if elapsed <= time_budget:
            print(f"\n✅ SUCCESS: Completed within time budget ({elapsed:.2f}s / {time_budget}s)")
        else:
            print(f"\n⚠️ TIMEOUT: Exceeded time budget ({elapsed:.2f}s / {time_budget}s)")
        
        return result
        
    except Exception as e:
        elapsed = time.time() - start
        print(f"\n❌ ERROR after {elapsed:.2f}s: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("LARGE T-COVERING OPTIMIZATION TEST")
    print("=" * 80)
    
    # Test medium instance first
    result1 = test_medium_instance()
    
    # Test large instance
    result2 = test_large_instance()
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if result1:
        print(f"✅ L(16,6,5,4) t=3: {result1.num_groups} groups")
    else:
        print("❌ L(16,6,5,4) t=3: FAILED")
    
    if result2:
        print(f"✅ L(20,6,5,4) t=4: {result2.num_groups} groups")
    else:
        print("❌ L(20,6,5,4) t=4: FAILED")
    
    print("\n" + "=" * 80)
