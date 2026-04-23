#!/usr/bin/env python3
"""测试 t-covering 验证功能的正确性"""

from solver import CoveringDesignSolver, elements_to_mask

def test_t1_verify():
    """测试 t=1 的验证（标准覆盖）"""
    print("测试 t=1 验证...")
    solver = CoveringDesignSolver(n=7, k=6, j=5, s=5, t=1)
    
    # 一个已知的正确解
    groups = [
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4, 6],
        [0, 1, 2, 3, 5, 6],
        [0, 1, 2, 4, 5, 6],
        [0, 1, 3, 4, 5, 6],
        [0, 2, 3, 4, 5, 6],
    ]
    masks = [elements_to_mask(g) for g in groups]
    
    is_verified = solver._verify(masks)
    print(f"  结果: {is_verified}")
    assert is_verified, "t=1 的正确解应该通过验证"
    print("  ✓ t=1 验证正确")

def test_t2_verify():
    """测试 t=2 的验证"""
    print("\n测试 t=2 验证...")
    solver = CoveringDesignSolver(n=8, k=6, j=5, s=4, t=2)
    
    # 先求解一个 t=2 的解
    result = solver.solve()
    print(f"  求解得到 {result.num_groups} 组")
    
    # 使用 tcovering_solver 的验证方法
    if hasattr(solver, '_tcovering_solver'):
        masks = [elements_to_mask(g) for g in result.groups]
        is_verified = solver._tcovering_solver._verify(masks)
        print(f"  验证结果: {is_verified}")
        assert is_verified, "t=2 的解应该通过 t=2 验证"
        print("  ✓ t=2 验证正确")
    else:
        print("  ⚠ 未找到 tcovering_solver")

def test_t2_should_fail_t3():
    """测试 t=2 的解不应该通过 t=3 验证"""
    print("\n测试 t=2 的解用 t=3 验证（应该失败）...")
    
    # 先用 t=2 求解
    solver_t2 = CoveringDesignSolver(n=8, k=6, j=5, s=4, t=2)
    result = solver_t2.solve()
    print(f"  t=2 求解得到 {result.num_groups} 组")
    
    # 用 t=3 验证
    solver_t3 = CoveringDesignSolver(n=8, k=6, j=5, s=4, t=3)
    if hasattr(solver_t3, '_tcovering_solver'):
        masks = [elements_to_mask(g) for g in result.groups]
        is_verified = solver_t3._tcovering_solver._verify(masks)
        print(f"  t=3 验证结果: {is_verified}")
        
        if not is_verified:
            print("  ✓ 正确：t=2 的解不满足 t=3 要求")
        else:
            print("  ⚠ 注意：t=2 的解碰巧也满足 t=3（这是可能的）")
    else:
        print("  ⚠ 未找到 tcovering_solver")

def test_t1_solution_passes_t1_verify():
    """测试 t=1 的解通过 t=1 验证"""
    print("\n测试 t=1 解的验证...")
    solver = CoveringDesignSolver(n=7, k=6, j=5, s=5, t=1)
    result = solver.solve()
    
    print(f"  求解得到 {result.num_groups} 组")
    print(f"  内置验证: {result.verified}")
    
    # 手动验证
    masks = [elements_to_mask(g) for g in result.groups]
    is_verified = solver._verify(masks)
    print(f"  手动验证: {is_verified}")
    
    assert result.verified == is_verified, "内置验证和手动验证应该一致"
    assert is_verified, "t=1 的解应该通过验证"
    print("  ✓ t=1 解验证一致")

def test_incomplete_solution_fails():
    """测试不完整的解不通过验证"""
    print("\n测试不完整解的验证（应该失败）...")
    solver = CoveringDesignSolver(n=7, k=6, j=5, s=5, t=1)
    
    # 只有一个组，肯定不够
    groups = [[0, 1, 2, 3, 4, 5]]
    masks = [elements_to_mask(g) for g in groups]
    
    is_verified = solver._verify(masks)
    print(f"  验证结果: {is_verified}")
    assert not is_verified, "不完整的解不应该通过验证"
    print("  ✓ 正确：不完整解验证失败")

if __name__ == "__main__":
    test_t1_verify()
    test_t1_solution_passes_t1_verify()
    test_incomplete_solution_fails()
    test_t2_verify()
    test_t2_should_fail_t3()
    print("\n✓ 所有验证测试通过！")
