#!/usr/bin/env python3
"""测试单个案例并查看详细日志"""

from solver import CoveringDesignSolver
import time

case_id = 'L_13_6_6_4'
n, k, j, s = 13, 6, 6, 4
baseline = 10

print(f"测试 {case_id}: n={n}, k={k}, j={j}, s={s}")
print(f"  Baseline: {baseline} 组")
print()

solver = CoveringDesignSolver(
    n=n, k=k, j=j, s=s, t=1,
    num_attempts=3, time_budget_sec=120
)

start = time.time()
result = solver.solve()
elapsed = time.time() - start

ratio = len(result.groups) / baseline
status = "✓" if len(result.groups) <= baseline else "✗"

print()
print(f"  结果: {len(result.groups)} 组 (比例: {ratio:.2f}) {status}")
print(f"  时间: {elapsed:.1f}s, 验证: {result.verified}")
