"""Test n=13 problem cases that had >10% error"""
import time
from solver import CoveringDesignSolver

problem_cases = [
    {"id": "L_13_5_5_3", "n": 13, "k": 5, "j": 5, "s": 3, "baseline": 8},
    {"id": "L_13_5_5_4", "n": 13, "k": 5, "j": 5, "s": 4, "baseline": 48},
    {"id": "L_13_6_5_5", "n": 13, "k": 6, "j": 5, "s": 5, "baseline": 245},
    {"id": "L_13_6_6_4", "n": 13, "k": 6, "j": 6, "s": 4, "baseline": 10},
    {"id": "L_13_6_6_5", "n": 13, "k": 6, "j": 6, "s": 5, "baseline": 61},
    {"id": "L_13_7_7_5", "n": 13, "k": 7, "j": 7, "s": 5, "baseline": 10},
    {"id": "L_13_7_7_6", "n": 13, "k": 7, "j": 7, "s": 6, "baseline": 61},
]

print("Testing n=13 problem cases (previously >10% error)")
print("=" * 60)

for case in problem_cases:
    print(f"\nTesting: {case['id']}")
    print(f"Parameters: n={case['n']}, k={case['k']}, j={case['j']}, s={case['s']}")
    print(f"Baseline optimal: {case['baseline']} blocks")
    print(f"Time budget: 120s")
    
    start = time.time()
    solver = CoveringDesignSolver(
        n=case['n'],
        k=case['k'],
        j=case['j'],
        s=case['s'],
        t=1,
        num_attempts=3,
        time_budget_sec=120
    )
    result = solver.solve()
    elapsed = time.time() - start
    
    baseline = case['baseline']
    actual = result.num_groups
    error_pct = ((actual - baseline) / baseline * 100) if baseline > 0 else 0
    
    if actual == baseline:
        status = "✓ OPTIMAL"
    elif actual < baseline:
        status = f"✓ BETTER ({actual} < {baseline})"
    elif error_pct <= 10:
        status = f"✓ ACCEPTABLE ({error_pct:.1f}% error ≤ 10%)"
    else:
        status = f"✗ WORSE ({error_pct:.1f}% error > 10%)"
    
    print(f"Result: {actual} blocks (verified={result.verified})")
    print(f"Status: {status}")
    print(f"Time: {elapsed:.2f}s")
    print("=" * 60)
