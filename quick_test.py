"""快速测试工具 - 从 baseline 中随机选择案例"""

import json
import random
import sys
from solver import CoveringDesignSolver
import time

# 读取 baseline
with open('results/newbaseline.json', 'r') as f:
    baseline_data = json.load(f)

# 参数
num_cases = int(sys.argv[1]) if len(sys.argv) > 1 else 5

# 随机选择案例
cases = random.sample(baseline_data['cases'], num_cases)

print(f"快速测试 - {num_cases} 个随机案例")
print("=" * 80)

total_ratio = 0
for i, case in enumerate(cases, 1):
    print(f"\n[{i}/{num_cases}] {case['id']}: n={case['n']}, k={case['k']}, j={case['j']}, s={case['s']}")
    print(f"  Baseline: {case['baseline_blocks']} 组")
    
    solver = CoveringDesignSolver(
        n=case['n'], k=case['k'], j=case['j'], s=case['s'], t=1,
        num_attempts=3, time_budget_sec=60
    )
    
    start = time.time()
    result = solver.solve()
    elapsed = time.time() - start
    
    ratio = len(result.groups) / case['baseline_blocks']
    total_ratio += ratio
    
    status = "✓" if ratio <= 1.0 else "✗"
    print(f"  结果: {len(result.groups)} 组 (比例: {ratio:.2f}) {status} - {elapsed:.1f}s")

print(f"\n平均比例: {total_ratio / num_cases:.2f}")
