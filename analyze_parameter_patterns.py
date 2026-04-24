"""分析不同参数组合的算法性能，识别可以改进的模式。

重点分析 n>12 时与最优解的差距，探索是否某些特定 k,j,s 参数组合
可以用不同的算法处理。
"""

import json
from math import comb
from typing import Dict, List, Tuple
from bounds import best_lower_bound


def load_baseline():
    """加载基准测试结果"""
    with open('results/baseline.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_case(case: dict) -> dict:
    """分析单个测试案例"""
    params = case['params']
    n, k, j, s = params['n'], params['k'], params['j'], params['s']
    
    result = case['result']
    num_groups = result['num_groups']
    
    # 获取参考值
    ref = case['reference']
    ref_type = ref['type']
    if ref_type == 'exact':
        ref_value = ref['value']
        gap_type = 'exact'
    elif ref_type == 'ljcr':
        ref_value = ref['value']
        gap_type = 'ljcr'
    else:  # lower_bound
        ref_value = case['bounds']['lower_bound']
        gap_type = 'lower_bound'
    
    gap = num_groups - ref_value
    gap_ratio = num_groups / ref_value if ref_value > 0 else float('inf')
    
    # 计算问题规模
    num_targets = comb(n, j)
    num_cands = comb(n, k)
    
    # 识别问题类型
    is_containment = (s == j)
    is_identity = (j == k and s == j)
    
    # 计算覆盖难度指标
    avg_coverage_per_cand = comb(k, j) if j <= k else 0
    coverage_density = avg_coverage_per_cand / num_targets if num_targets > 0 else 0
    
    return {
        'id': case['id'],
        'name': case['name'],
        'n': n,
        'k': k,
        'j': j,
        's': s,
        'num_groups': num_groups,
        'ref_value': ref_value,
        'ref_type': ref_type,
        'gap': gap,
        'gap_ratio': gap_ratio,
        'gap_type': gap_type,
        'num_targets': num_targets,
        'num_cands': num_cands,
        'is_containment': is_containment,
        'is_identity': is_identity,
        'avg_coverage_per_cand': avg_coverage_per_cand,
        'coverage_density': coverage_density,
        'elapsed_sec': result['elapsed_sec'],
    }


def categorize_by_pattern(analyses: List[dict]) -> Dict[str, List[dict]]:
    """按参数模式分类"""
    patterns = {
        'containment_small': [],      # s=j, n<=12
        'containment_large': [],      # s=j, n>12
        'non_containment_small': [],  # s<j, n<=12
        'non_containment_large': [],  # s<j, n>12
        'identity': [],               # j=k=s
        'j_equals_k': [],            # j=k, s<j
        'partial_overlap': [],        # s<j<k
    }
    
    for a in analyses:
        if a['is_identity']:
            patterns['identity'].append(a)
        elif a['is_containment']:
            if a['n'] <= 12:
                patterns['containment_small'].append(a)
            else:
                patterns['containment_large'].append(a)
        elif a['j'] == a['k']:
            patterns['j_equals_k'].append(a)
        else:
            if a['n'] <= 12:
                patterns['non_containment_small'].append(a)
            else:
                patterns['non_containment_large'].append(a)
        
        if a['s'] < a['j'] < a['k']:
            patterns['partial_overlap'].append(a)
    
    return patterns


def print_pattern_analysis(pattern_name: str, cases: List[dict]):
    """打印某个模式的分析结果"""
    if not cases:
        return
    
    print(f"\n{'='*80}")
    print(f"模式: {pattern_name}")
    print(f"案例数: {len(cases)}")
    print(f"{'='*80}")
    
    # 按 gap_ratio 排序
    cases_sorted = sorted(cases, key=lambda x: x['gap_ratio'], reverse=True)
    
    print(f"\n{'ID':<15} {'n':>3} {'k':>2} {'j':>2} {'s':>2} {'结果':>6} {'参考':>6} {'差距':>6} {'比例':>6} {'类型':<12}")
    print('-' * 80)
    
    for c in cases_sorted:
        print(f"{c['id']:<15} {c['n']:>3} {c['k']:>2} {c['j']:>2} {c['s']:>2} "
              f"{c['num_groups']:>6} {c['ref_value']:>6} {c['gap']:>6} "
              f"{c['gap_ratio']:>6.2f} {c['gap_type']:<12}")
    
    # 统计信息
    avg_gap_ratio = sum(c['gap_ratio'] for c in cases) / len(cases)
    max_gap_ratio = max(c['gap_ratio'] for c in cases)
    min_gap_ratio = min(c['gap_ratio'] for c in cases)
    
    print(f"\n统计:")
    print(f"  平均比例: {avg_gap_ratio:.3f}")
    print(f"  最大比例: {max_gap_ratio:.3f} ({cases_sorted[0]['id']})")
    print(f"  最小比例: {min_gap_ratio:.3f}")
    
    # 识别问题案例（gap_ratio > 1.5）
    problem_cases = [c for c in cases if c['gap_ratio'] > 1.5]
    if problem_cases:
        print(f"\n⚠️  问题案例 (比例 > 1.5): {len(problem_cases)}")
        for c in problem_cases:
            print(f"  - {c['id']}: n={c['n']}, k={c['k']}, j={c['j']}, s={c['s']}, "
                  f"比例={c['gap_ratio']:.2f}, 差距={c['gap']}")


def analyze_parameter_correlations(analyses: List[dict]):
    """分析参数与性能的相关性"""
    print(f"\n{'='*80}")
    print("参数相关性分析")
    print(f"{'='*80}")
    
    # 按 n 分组
    by_n = {}
    for a in analyses:
        n = a['n']
        if n not in by_n:
            by_n[n] = []
        by_n[n].append(a)
    
    print("\n按 n 分组的平均 gap_ratio:")
    for n in sorted(by_n.keys()):
        cases = by_n[n]
        avg_ratio = sum(c['gap_ratio'] for c in cases) / len(cases)
        print(f"  n={n:2d}: {avg_ratio:.3f} (案例数: {len(cases)})")
    
    # 按 k,j,s 组合分组
    by_kjs = {}
    for a in analyses:
        kjs = (a['k'], a['j'], a['s'])
        if kjs not in by_kjs:
            by_kjs[kjs] = []
        by_kjs[kjs].append(a)
    
    print("\n按 (k,j,s) 组合分组的平均 gap_ratio:")
    for kjs in sorted(by_kjs.keys()):
        cases = by_kjs[kjs]
        avg_ratio = sum(c['gap_ratio'] for c in cases) / len(cases)
        k, j, s = kjs
        print(f"  k={k}, j={j}, s={s}: {avg_ratio:.3f} (案例数: {len(cases)})")


def identify_algorithm_opportunities(patterns: Dict[str, List[dict]]):
    """识别可以用不同算法处理的机会"""
    print(f"\n{'='*80}")
    print("算法改进机会")
    print(f"{'='*80}")
    
    opportunities = []
    
    # 1. 大规模包含覆盖问题
    containment_large = patterns['containment_large']
    if containment_large:
        bad_cases = [c for c in containment_large if c['gap_ratio'] > 1.2]
        if bad_cases:
            opportunities.append({
                'pattern': '大规模包含覆盖 (n>12, s=j)',
                'cases': bad_cases,
                'suggestion': '考虑使用组合设计理论的构造方法，而不是贪心算法'
            })
    
    # 2. 大规模非包含覆盖问题
    non_containment_large = patterns['non_containment_large']
    if non_containment_large:
        bad_cases = [c for c in non_containment_large if c['gap_ratio'] > 2.0]
        if bad_cases:
            opportunities.append({
                'pattern': '大规模非包含覆盖 (n>12, s<j)',
                'cases': bad_cases,
                'suggestion': '考虑使用更强的局部搜索或元启发式算法（如遗传算法、禁忌搜索）'
            })
    
    # 3. j=k 的情况
    j_equals_k = patterns['j_equals_k']
    if j_equals_k:
        bad_cases = [c for c in j_equals_k if c['gap_ratio'] > 1.5]
        if bad_cases:
            opportunities.append({
                'pattern': 'j=k 的情况',
                'cases': bad_cases,
                'suggestion': '可以使用集合覆盖的专门算法，如整数规划或约束编程'
            })
    
    # 4. 特定 k,j,s 组合
    # 检查是否有特定组合表现特别差
    by_kjs = {}
    for pattern_cases in patterns.values():
        for c in pattern_cases:
            kjs = (c['k'], c['j'], c['s'])
            if kjs not in by_kjs:
                by_kjs[kjs] = []
            by_kjs[kjs].append(c)
    
    for kjs, cases in by_kjs.items():
        if len(cases) >= 2:  # 至少有2个案例
            avg_ratio = sum(c['gap_ratio'] for c in cases) / len(cases)
            if avg_ratio > 1.8:
                k, j, s = kjs
                opportunities.append({
                    'pattern': f'特定参数组合 k={k}, j={j}, s={s}',
                    'cases': cases,
                    'suggestion': f'这个参数组合平均比例 {avg_ratio:.2f}，需要专门优化'
                })
    
    # 打印机会
    if not opportunities:
        print("\n✓ 没有发现明显的算法改进机会")
        return
    
    for i, opp in enumerate(opportunities, 1):
        print(f"\n机会 {i}: {opp['pattern']}")
        print(f"  问题案例数: {len(opp['cases'])}")
        print(f"  建议: {opp['suggestion']}")
        print(f"  案例:")
        for c in opp['cases']:
            print(f"    - {c['id']}: n={c['n']}, 比例={c['gap_ratio']:.2f}, 差距={c['gap']}")


def main():
    print("="*80)
    print("覆盖设计算法参数模式分析")
    print("="*80)
    
    baseline = load_baseline()
    
    # 分析所有案例
    analyses = []
    for case in baseline['cases']:
        if case['result']['status'] == 'ok':
            analyses.append(analyze_case(case))
    
    print(f"\n总案例数: {len(analyses)}")
    
    # 按模式分类
    patterns = categorize_by_pattern(analyses)
    
    # 打印每个模式的分析
    for pattern_name, cases in patterns.items():
        print_pattern_analysis(pattern_name, cases)
    
    # 参数相关性分析
    analyze_parameter_correlations(analyses)
    
    # 识别算法改进机会
    identify_algorithm_opportunities(patterns)
    
    # 重点关注 n>12 的案例
    print(f"\n{'='*80}")
    print("重点: n>12 的案例分析")
    print(f"{'='*80}")
    
    large_n_cases = [a for a in analyses if a['n'] > 12]
    print(f"\nn>12 的案例数: {len(large_n_cases)}")
    
    if large_n_cases:
        print(f"\n{'ID':<20} {'n':>3} {'k':>2} {'j':>2} {'s':>2} {'结果':>6} {'参考':>6} {'差距':>6} {'比例':>6}")
        print('-' * 80)
        for c in sorted(large_n_cases, key=lambda x: x['gap_ratio'], reverse=True):
            print(f"{c['id']:<20} {c['n']:>3} {c['k']:>2} {c['j']:>2} {c['s']:>2} "
                  f"{c['num_groups']:>6} {c['ref_value']:>6} {c['gap']:>6} {c['gap_ratio']:>6.2f}")
        
        avg_ratio = sum(c['gap_ratio'] for c in large_n_cases) / len(large_n_cases)
        print(f"\nn>12 的平均比例: {avg_ratio:.3f}")
        
        # 最差的案例
        worst = max(large_n_cases, key=lambda x: x['gap_ratio'])
        print(f"\n最差案例: {worst['id']}")
        print(f"  参数: n={worst['n']}, k={worst['k']}, j={worst['j']}, s={worst['s']}")
        print(f"  结果: {worst['num_groups']} vs 参考 {worst['ref_value']}")
        print(f"  比例: {worst['gap_ratio']:.2f}")
        print(f"  类型: {'包含覆盖' if worst['is_containment'] else '非包含覆盖'}")


if __name__ == '__main__':
    main()
