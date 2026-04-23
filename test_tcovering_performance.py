#!/usr/bin/env python3
"""测试 t-covering 性能和质量"""

import time
from solver import CoveringDesignSolver

def test_small_instance():
    """小实例测试"""
    print("=" * 60)
    print("小实例测试: n=8, k=6, j=5, s=4")
    print("=" * 60)
    
    for t in [1, 2, 3, 4]:
        print(f"\nt={t}:")
        start = time.time()
        solver = CoveringDesignSolver(n=8, k=6, j=5, s=4, t=t, num_attempts=3)
        result = solver.solve()
        elapsed = time.time() - start
        
        print(f"  组数: {result.num_groups}")
        print(f"  验证: {result.verified}")
        print(f"  时间: {elapsed:.2f}s")

def test_medium_instance():
    """中等实例测试"""
    print("\n" + "=" * 60)
    print("中等实例测试: n=10, k=6, j=5, s=4")
    print("=" * 60)
    
    for t in [1, 2, 3]:
        print(f"\nt={t}:")
        start = time.time()
        solver = CoveringDesignSolver(n=10, k=6, j=5, s=4, t=t, num_attempts=3, time_budget_sec=60)
        result = solver.solve()
        elapsed = time.time() - start
        
        print(f"  组数: {result.num_groups}")
        print(f"  验证: {result.verified}")
        print(f"  时间: {elapsed:.2f}s")

def test_large_instance():
    """大实例测试"""
    print("\n" + "=" * 60)
    print("大实例测试: n=12, k=6, j=5, s=4")
    print("=" * 60)
    
    for t in [1, 2]:
        print(f"\nt={t}:")
        start = time.time()
        solver = CoveringDesignSolver(n=12, k=6, j=5, s=4, t=t, num_attempts=2, time_budget_sec=90)
        result = solver.solve()
        elapsed = time.time() - start
        
        print(f"  组数: {result.num_groups}")
        print(f"  验证: {result.verified}")
        print(f"  时间: {elapsed:.2f}s")

def test_quality_comparison():
    """质量对比测试"""
    print("\n" + "=" * 60)
    print("质量对比: 多次运行查看稳定性")
    print("=" * 60)
    
    n, k, j, s, t = 8, 6, 5, 4, 2
    print(f"\n参数: n={n}, k={k}, j={j}, s={s}, t={t}")
    
    results = []
    for run in range(5):
        solver = CoveringDesignSolver(n=n, k=k, j=j, s=s, t=t, num_attempts=3)
        result = solver.solve()
        results.append(result.num_groups)
        print(f"  Run {run+1}: {result.num_groups} groups")
    
    print(f"\n  最优: {min(results)} groups")
    print(f"  平均: {sum(results)/len(results):.1f} groups")
    print(f"  最差: {max(results)} groups")

if __name__ == "__main__":
    test_small_instance()
    test_medium_instance()
    test_large_instance()
    test_quality_comparison()
    print("\n" + "=" * 60)
    print("✓ 性能测试完成！")
    print("=" * 60)
