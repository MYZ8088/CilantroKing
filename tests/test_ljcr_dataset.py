"""基于 LJCR 数据集的全面测试: 验证求解器结果不超过已知最优值.

测试分三类:
  1. 绝对正确 (PROVEN): 求解器结果必须 >= LJCR值 (LJCR值是真正最优值)
  2. 可能最优 (BEST_KNOWN): 求解器结果与 LJCR 值比较, 计算接近度
  3. 快速冒烟测试: 小参数已证明最优值, 验证基本正确性
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import time
from ljcr_dataset import (
    LJCR_DATASET, PROVEN, BEST_KNOWN,
    get_proven_optimal, get_best_known, get_small_proven, summary,
)
from solver import CoveringDesignSolver


def test_proven_small(timeout: float = 60.0) -> None:
    """快速冒烟测试: 仅测试 n<=12 的已证明最优参数."""
    cases = get_small_proven(max_n=12)
    print("=" * 80)
    print(f"冒烟测试: {len(cases)} 个小参数已证明最优值 (n<=12)")
    print("=" * 80)
    print(f"{'C(n,k,t)':<14} {'LJCR':>6} {'Result':>7} {'Match':>6} {'Time':>7}")
    print("-" * 80)

    passed = 0
    for n, k, t, ljcr_val in cases:
        t0 = time.time()
        try:
            solver = CoveringDesignSolver(
                n=n, k=k, j=t, s=t, num_attempts=3,
                cancel_fn=lambda _t0=t0: (time.time() - _t0) > timeout,
            )
            result = solver.solve()
            elapsed = time.time() - t0
            got = result.num_groups
            match = "✓" if got <= ljcr_val else f"+{got - ljcr_val}"
            if got <= ljcr_val:
                passed += 1
            print(f"C({n},{k},{t}){'':<{7-len(f'{n},{k},{t}')}} "
                  f"{ljcr_val:>6} {got:>7} {match:>6} {elapsed:>6.1f}s")
        except Exception as exc:
            elapsed = time.time() - t0
            print(f"C({n},{k},{t}){'':<{7-len(f'{n},{k},{t}')}} "
                  f"{ljcr_val:>6} {'ERR':>7} {'✗':>6} {elapsed:>6.1f}s  {exc}")

    print("-" * 80)
    print(f"通过: {passed}/{len(cases)}")


def test_full_dataset(max_n: int = 25, timeout: float = 120.0,
                      max_cases: int | None = None) -> None:
    """全面测试: 验证所有 LJCR 数据集条目."""
    dataset = [r for r in LJCR_DATASET if r[0] <= max_n]
    if max_cases:
        dataset = dataset[:max_cases]

    stats = summary()
    print("=" * 95)
    print(f"LJCR 全面测试 (共 {len(dataset)} 项, "
          f"绝对正确={stats['proven_optimal']}, 可能最优={stats['best_known']})")
    print("=" * 95)
    print(f"{'C(n,k,t)':<14} {'Status':<6} {'LJCR':>6} {'Sch':>6} "
          f"{'Result':>7} {'Ratio':>7} {'Grade':>6} {'Time':>7}")
    print("-" * 95)

    total = 0
    verified = 0
    grades = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0}

    for n, k, t, ljcr_val, sch_val, status, gap in dataset:
        total += 1
        status_short = "证明" if status == PROVEN else "最优"
        t0 = time.time()
        try:
            solver = CoveringDesignSolver(
                n=n, k=k, j=t, s=t, num_attempts=3,
                cancel_fn=lambda _t0=t0: (time.time() - _t0) > timeout,
            )
            result = solver.solve()
            elapsed = time.time() - t0
            got = result.num_groups

            if not result.verified:
                print(f"C({n},{k},{t}){'':<{7-len(f'{n},{k},{t}')}} "
                      f"{status_short:<6} {ljcr_val:>6} {sch_val:>6} "
                      f"{got:>7} {'---':>7} {'ERR':>6} {elapsed:>6.1f}s  未验证")
                continue

            verified += 1
            ratio = got / ljcr_val

            if got <= ljcr_val:
                grade = "A+"
            elif got <= ljcr_val * 1.10:
                grade = "A"
            elif got <= ljcr_val * 1.25:
                grade = "B"
            elif got <= ljcr_val * 1.50:
                grade = "C"
            else:
                grade = "D"
            grades[grade] = grades.get(grade, 0) + 1

            print(f"C({n},{k},{t}){'':<{7-len(f'{n},{k},{t}')}} "
                  f"{status_short:<6} {ljcr_val:>6} {sch_val:>6} "
                  f"{got:>7} {ratio:>7.3f} {grade:>6} {elapsed:>6.1f}s")

        except Exception as exc:
            elapsed = time.time() - t0
            print(f"C({n},{k},{t}){'':<{7-len(f'{n},{k},{t}')}} "
                  f"{status_short:<6} {ljcr_val:>6} {sch_val:>6} "
                  f"{'ERR':>7} {'---':>7} {'---':>6} {elapsed:>6.1f}s  {exc}")

    print("-" * 95)
    print(f"验证通过: {verified}/{total}")
    print(f"评级分布: A+={grades.get('A+',0)}, A={grades.get('A',0)}, "
          f"B={grades.get('B',0)}, C={grades.get('C',0)}, D={grades.get('D',0)}")
    if verified > 0:
        a_pct = (grades.get("A+", 0) + grades.get("A", 0)) / verified
        print(f"A级及以上比例: {a_pct:.1%}")


def print_dataset_summary() -> None:
    """打印数据集统计."""
    stats = summary()
    print("LJCR 测试数据集统计:")
    for key, val in stats.items():
        print(f"  {key}: {val}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LJCR 数据集测试")
    parser.add_argument("--mode", choices=["smoke", "full", "summary"],
                        default="smoke", help="测试模式")
    parser.add_argument("--max-n", type=int, default=15,
                        help="最大 n 值 (full 模式, 默认 15)")
    parser.add_argument("--max-cases", type=int, default=None,
                        help="最大测试数量")
    parser.add_argument("--timeout", type=float, default=120.0,
                        help="单项超时(秒)")
    args = parser.parse_args()

    if args.mode == "summary":
        print_dataset_summary()
    elif args.mode == "smoke":
        test_proven_small(timeout=args.timeout)
    elif args.mode == "full":
        test_full_dataset(max_n=args.max_n, timeout=args.timeout,
                          max_cases=args.max_cases)
