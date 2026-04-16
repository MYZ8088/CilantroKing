#!/usr/bin/env python3
"""详细分析 {A,B,C,D,F,G} 的各种可能理解"""

from itertools import combinations

groups_6 = [
    {'A', 'B', 'C', 'D', 'E', 'H'},  # 1
    {'A', 'B', 'C', 'E', 'F', 'H'},  # 2
    {'A', 'B', 'C', 'E', 'G', 'H'},  # 3
    {'A', 'B', 'D', 'E', 'F', 'G'},  # 4
    {'A', 'B', 'D', 'F', 'G', 'H'},  # 5
    {'A', 'C', 'D', 'E', 'F', 'G'},  # 6
    {'A', 'D', 'E', 'F', 'G', 'H'},  # 7
    {'B', 'C', 'D', 'E', 'G', 'H'},  # 8
    {'B', 'C', 'D', 'F', 'G', 'H'},  # 9
    {'B', 'D', 'E', 'F', 'G', 'H'},  # 10
]

test_j = {'A', 'B', 'C', 'D', 'F', 'G'}

print("=" * 70)
print("分析 j-子集 {A, B, C, D, F, G}")
print("=" * 70)

print("\n理解1: 有多少个组与这个 j-子集共享至少5个元素")
print("-" * 70)
count1 = 0
for i, g in enumerate(groups_6, 1):
    shared = test_j & g
    if len(shared) >= 5:
        count1 += 1
        print(f"Group {i}: {g}")
        print(f"  共享: {shared} ({len(shared)}个)")
print(f"结果: {count1} 个组")

print("\n理解2: 这个 j-子集的多少个 s-子集被某个组完全包含")
print("-" * 70)
all_s = list(combinations(test_j, 5))
count2 = 0
for s_sub in all_s:
    s_set = set(s_sub)
    for i, g in enumerate(groups_6, 1):
        if s_set.issubset(g):
            count2 += 1
            print(f"{s_set} ⊆ Group {i}")
            break
print(f"结果: {count2}/6 个 s-子集被覆盖")

print("\n理解3: 所有 s-子集被覆盖的总次数（计算重复）")
print("-" * 70)
count3 = 0
for s_sub in all_s:
    s_set = set(s_sub)
    for i, g in enumerate(groups_6, 1):
        if s_set.issubset(g):
            count3 += 1
            print(f"{s_set} ⊆ Group {i}")
print(f"结果: 总共 {count3} 次覆盖")

print("\n理解4: 有多少个组包含这个 j-子集的至少一个 s-子集")
print("-" * 70)
groups_covering = set()
for s_sub in all_s:
    s_set = set(s_sub)
    for i, g in enumerate(groups_6, 1):
        if s_set.issubset(g):
            groups_covering.add(i)
            print(f"{s_set} ⊆ Group {i}")
print(f"结果: {len(groups_covering)} 个不同的组: {sorted(groups_covering)}")

print("\n" + "=" * 70)
print("总结")
print("=" * 70)
print(f"理解1（标准定义）: {count1} 个组覆盖这个 j-子集")
print(f"理解2（s-子集被覆盖）: {count2}/6 个 s-子集被覆盖")
print(f"理解3（总覆盖次数）: {count3} 次")
print(f"理解4（涉及的组数）: {len(groups_covering)} 个组")
print()
print("如果 t=4:")
print(f"  理解1: {count1} >= 4? {'✓' if count1 >= 4 else '✗'}")
print(f"  理解2: {count2} >= 4? {'✓' if count2 >= 4 else '✗'}")
print(f"  理解3: {count3} >= 4? {'✓' if count3 >= 4 else '✗'}")
print(f"  理解4: {len(groups_covering)} >= 4? {'✓' if len(groups_covering) >= 4 else '✗'}")
