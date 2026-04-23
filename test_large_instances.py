#!/usr/bin/env python3
"""测试大实例性能 (n=15-25)"""

import time
from solver import CoveringDesignSolver

def test_instance(n, k, j, s, t, timeout=120):
    """测试单个实例"""
    print(f"\n测试: n={n}, k={k}, j={j}, s={s}, t={t}")
    print("-" * 50)
    
    try:
        start = time.time()
        solver = CoveringDesignSolver(
            n=n, k=k, j=j, s=s, t=t,
            num_attempts=3,
            time_budget_sec=timeout
        )
        result = solver.solve()
        elapsed = time.time() - start
        
        print(f"  组数: {result.num_groups}")
        print(f"  验证: {result.verified}")
        print(f"  时间: {elapsed:.2f}s")
        print(f"  首次合法解: {result.first_legal_elapsed:.2f}s" if result.first_legal_elapsed else "  首次合法解: N/A")
        
        return result.num_groups, elapsed, result.verified
    except Exception as e:
        print(f"  错误: {e}")
        return None, None, False

def main():
    print("=" * 60)
    print("大实例性能测试 (n=15-25)")
    print("=" * 60)
    
    # n=15 测试
    print("\n" + "=" * 60)
    print("n=15 实例")
    print("=" * 60)
    test_instance(15, 6, 5, 4, 1, timeout=60)
    test_instance(15, 6, 5, 4, 2, timeout=90)
    
    # n=18 测试
    print("\n" + "=" * 60)
    print("n=18 实例")
    print("=" * 60)
    test_instance(18, 6, 5, 4, 1, timeout=90)
    test_instance(18, 6, 5, 4, 2, timeout=120)
    
    # n=20 测试
    print("\n" + "=" * 60)
    print("n=20 实例")
    print("=" * 60)
    test_instance(20, 6, 5, 4, 1, timeout=120)
    test_instance(20, 6, 5, 4, 2, timeout=150)
    
    # n=25 测试（最大）
    print("\n" + "=" * 60)
    print("n=25 实例（最大）")
    print("=" * 60)
    test_instance(25, 6, 5, 4, 1, timeout=180)
    test_instance(25, 6, 5, 4, 2, timeout=180)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
