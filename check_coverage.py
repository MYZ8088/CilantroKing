#!/usr/bin/env python3
"""检查result.md中的解是否覆盖所有j-子集"""

from itertools import combinations

# 参数
n = 20
k = 6
j = 5
s = 4

# 选中的样本
samples = [1, 3, 4, 6, 7, 10, 11, 14, 17, 18, 19, 20, 22, 23, 24, 26, 33, 35, 43, 44]

# 从result.md读取所有组
groups = []
with open('result.md', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Group' in line and ':' in line:
            parts = line.split(':')
            if len(parts) == 2:
                nums_str = parts[1].strip()
                nums = [int(x.strip()) for x in nums_str.split(',')]
                groups.append(set(nums))

print(f"总共 {len(groups)} 个组")
print(f"参数: n={n}, k={k}, j={j}, s={s}")
print(f"样本: {samples}\n")

# 生成所有j-子集
all_j_subsets = list(combinations(samples, j))
print(f"需要覆盖的 {j}-子集总数: {len(all_j_subsets)}\n")

# 检查每个j-子集是否被覆盖
uncovered = []
for subset in all_j_subsets:
    subset_set = set(subset)
    covered = False
    for group in groups:
        # 检查group中是否包含subset的至少s个元素
        overlap = len(subset_set & group)
        if overlap >= s:
            covered = True
            break
    if not covered:
        uncovered.append(subset)

if uncovered:
    print(f"❌ 发现 {len(uncovered)} 个未覆盖的 {j}-子集:")
    for i, subset in enumerate(uncovered[:10], 1):  # 只显示前10个
        print(f"  {i}. {subset}")
        # 检查每个组能覆盖多少个
        best_overlap = 0
        best_group = None
        for group in groups:
            overlap = len(set(subset) & group)
            if overlap > best_overlap:
                best_overlap = overlap
                best_group = group
        print(f"     最佳组覆盖 {best_overlap} 个: {sorted(best_group)}")
    if len(uncovered) > 10:
        print(f"  ... 还有 {len(uncovered) - 10} 个未显示")
else:
    print("✅ 所有 {j}-子集都被正确覆盖!")
