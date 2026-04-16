#!/usr/bin/env python3
"""验证 t-covering 的两种定义"""

from itertools import combinations

def check_definition2(groups, samples, j, s, t):
    """
    定义2：至少 t 个不同的 s-子集被覆盖
    一个 s-子集被多个组覆盖也只算1次
    """
    all_j_subsets = list(combinations(samples, j))
    failed = []
    
    for j_subset in all_j_subsets:
        all_s_subsets = list(combinations(j_subset, s))
        covered_s_count = 0
        
        for s_subset in all_s_subsets:
            s_set = set(s_subset)
            for group in groups:
                if s_set.issubset(group):
                    covered_s_count += 1
                    break
        
        if covered_s_count < t:
            failed.append((j_subset, covered_s_count))
    
    return failed

def check_definition3(groups, samples, j, s, t):
    """
    定义3：总覆盖次数 ≥ t
    如果一个 s-子集被多个组覆盖，每次都计数
    """
    all_j_subsets = list(combinations(samples, j))
    failed = []
    
    for j_subset in all_j_subsets:
        all_s_subsets = list(combinations(j_subset, s))
        total_coverage = 0
        
        for s_subset in all_s_subsets:
            s_set = set(s_subset)
            for group in groups:
                if s_set.issubset(group):
                    total_coverage += 1
        
        if total_coverage < t:
            failed.append((j_subset, total_coverage))
    
    return failed

# Example 5: t=1
print("=" * 70)
print("Example 5 (t=1)")
print("=" * 70)

samples_5 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
groups_5 = [
    {'A', 'B', 'C', 'E', 'G', 'H'},
    {'A', 'B', 'D', 'F', 'G', 'H'},
    {'A', 'C', 'D', 'E', 'F', 'H'},
    {'B', 'C', 'D', 'E', 'F', 'G'},
]

failed_5_def2 = check_definition2(groups_5, samples_5, j=6, s=5, t=1)
failed_5_def3 = check_definition3(groups_5, samples_5, j=6, s=5, t=1)

print(f"定义2（不同s-子集数量≥t）: {'✓ 满足' if not failed_5_def2 else f'✗ {len(failed_5_def2)}个不满足'}")
print(f"定义3（总覆盖次数≥t）:     {'✓ 满足' if not failed_5_def3 else f'✗ {len(failed_5_def3)}个不满足'}")

# Example 6: t=4
print("\n" + "=" * 70)
print("Example 6 (t=4)")
print("=" * 70)

samples_6 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
groups_6 = [
    {'A', 'B', 'C', 'D', 'E', 'H'},
    {'A', 'B', 'C', 'E', 'F', 'H'},
    {'A', 'B', 'C', 'E', 'G', 'H'},
    {'A', 'B', 'D', 'E', 'F', 'G'},
    {'A', 'B', 'D', 'F', 'G', 'H'},
    {'A', 'C', 'D', 'E', 'F', 'G'},
    {'A', 'D', 'E', 'F', 'G', 'H'},
    {'B', 'C', 'D', 'E', 'G', 'H'},
    {'B', 'C', 'D', 'F', 'G', 'H'},
    {'B', 'D', 'E', 'F', 'G', 'H'},
]

failed_6_def2 = check_definition2(groups_6, samples_6, j=6, s=5, t=4)
failed_6_def3 = check_definition3(groups_6, samples_6, j=6, s=5, t=4)

print(f"定义2（不同s-子集数量≥t）: {'✓ 满足' if not failed_6_def2 else f'✗ {len(failed_6_def2)}个不满足'}")
print(f"定义3（总覆盖次数≥t）:     {'✓ 满足' if not failed_6_def3 else f'✗ {len(failed_6_def3)}个不满足'}")

if failed_6_def2:
    print(f"\n定义2不满足的 j-子集:")
    for j_sub, count in failed_6_def2[:3]:
        print(f"  {set(j_sub)}: {count}/6 个s-子集被覆盖")

# 详细分析一个例子
print("\n" + "=" * 70)
print("详细分析: j-子集 {A,B,C,D,F,G}")
print("=" * 70)

test_j = ('A', 'B', 'C', 'D', 'F', 'G')
all_s = list(combinations(test_j, 5))

print("\n6个 s-子集的覆盖情况:")
covered_count = 0
total_coverage = 0

for i, s_sub in enumerate(all_s, 1):
    s_set = set(s_sub)
    covering_groups = []
    for g_idx, g in enumerate(groups_6, 1):
        if s_set.issubset(g):
            covering_groups.append(g_idx)
    
    if covering_groups:
        covered_count += 1
        total_coverage += len(covering_groups)
        print(f"  {i}. {s_set}")
        print(f"     被 {len(covering_groups)} 个组覆盖: Group {covering_groups}")
    else:
        print(f"  {i}. {s_set}")
        print(f"     未被覆盖")

print(f"\n定义2结果: {covered_count}/6 个s-子集被覆盖, t=4要求≥4, {'✓' if covered_count >= 4 else '✗'}")
print(f"定义3结果: 总覆盖{total_coverage}次, t=4要求≥4, {'✓' if total_coverage >= 4 else '✗'}")

print("\n" + "=" * 70)
print("结论")
print("=" * 70)
print("根据 PDF Example 6 是正确的例子：")
print("- 定义2: ✗ 不满足 → 不是正确定义")
print("- 定义3: ✓ 满足   → 应该是正确定义")
