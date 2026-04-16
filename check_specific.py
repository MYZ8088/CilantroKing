#!/usr/bin/env python3
"""检查包含{1,3,6,7}的所有5-子集如何被覆盖"""

from itertools import combinations

# 参数
samples = [1, 3, 4, 6, 7, 10, 11, 14, 17, 18, 19, 20, 22, 23, 24, 26, 33, 35, 43, 44]
target_4 = {1, 3, 6, 7}

# 从result.md读取所有组
groups = []
with open('result.md', 'r', encoding='utf-8') as f:
    for line in f:
        if 'Group' in line and ':' in line:
            parts = line.split(':')
            if len(parts) == 2:
                group_name = parts[0].strip()
                nums_str = parts[1].strip()
                nums = [int(x.strip()) for x in nums_str.split(',')]
                groups.append((group_name, set(nums)))

print(f"检查包含 {target_4} 的所有5-子集:\n")

# 找出所有包含{1,3,6,7}的5-子集
count = 0
for fifth in samples:
    if fifth not in target_4:
        subset_5 = target_4 | {fifth}
        count += 1
        
        # 找出覆盖这个5-子集的组
        covering_groups = []
        for group_name, group in groups:
            overlap = len(subset_5 & group)
            if overlap >= 4:
                covering_groups.append((group_name, sorted(group), overlap))
        
        print(f"{count}. 5-子集 {sorted(subset_5)}:")
        if covering_groups:
            for gname, gnums, overlap in covering_groups[:2]:  # 只显示前2个
                print(f"   ✓ {gname}: {gnums} (覆盖{overlap}个)")
        else:
            print(f"   ❌ 未被覆盖!")
        print()

print(f"\n总结: 包含 {target_4} 的5-子集共有 {count} 个")
