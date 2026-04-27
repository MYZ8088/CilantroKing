#!/usr/bin/env python3
"""测试特定的j=k案例"""

import json
from solver import CoveringDesignSolver
import time

# 使用与UI相同的默认time_budget
DEFAULT_TIME_BUDGET_SEC = 90.0

# 读取baseline
with open('results/baseline.json', 'r') as f:
    baseline_data = json.load(f)

# 创建案例ID到baseline的映射
baseline_map = {case['id']: case for case in baseline_data['cases']}

# 要测试的案例
test_ids = ['L_13_6_6_4', 'L_14_6_6_4', 'L_15_6_6_4', 'L_14_7_7_5', 'L_13_7_7_4']

print("测试 j=k 案例")
print("=" * 80)

results = []
for case_id in test_ids:
    if case_id not in baseline_map:
        print(f"\n{case_id}: 未找到baseline")
        continue
    
    case = baseline_map[case_id]
    print(f"\n{case_id}: n={case['n']}, k={case['k']}, j={case['j']}, s={case['s']}")
    print(f"  Baseline: {case['baseline_blocks']} 组")
    
    solver = CoveringDesignSolver(
        n=case['n'], k=case['k'], j=case['j'], s=case['s'], t=1,
        num_attempts=3, time_budget_sec=DEFAULT_TIME_BUDGET_SEC
    )
    
    start = time.time()
    result = solver.solve()
    elapsed = time.time() - start
    
    ratio = len(result.groups) / case['baseline_blocks']
    status = "✓" if len(result.groups) <= case['baseline_blocks'] else "✗"
    
    print(f"  结果: {len(result.groups)} 组 (比例: {ratio:.2f}) {status}")
    print(f"  时间: {elapsed:.1f}s, 验证: {result.verified}")
    
    results.append({
        'id': case_id,
        'baseline': case['baseline_blocks'],
        'result': len(result.groups),
        'ratio': ratio
    })

print("\n" + "=" * 80)
print("总结:")
better_or_equal = sum(1 for r in results if r['result'] <= r['baseline'])
print(f"  达到或优于baseline: {better_or_equal}/{len(results)}")
avg_ratio = sum(r['ratio'] for r in results) / len(results)
print(f"  平均比例: {avg_ratio:.2f}")
