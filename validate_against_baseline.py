from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from pathlib import Path

from optimal_samples import Problem, solve_problem, verify_solution


BASELINE_FILE = Path("coveringrepo_n_lt_26_baselines(1).json")


@dataclass(frozen=True)
class BaselineCase:
    case_id: str
    n: int
    k: int
    j: int
    s: int
    baseline_blocks: int


def load_cases(path: Path, max_n: int) -> list[BaselineCase]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = []
    for item in data["cases"]:
        n = int(item["n"])
        if 15 <= n <= max_n:
            cases.append(
                BaselineCase(
                    case_id=str(item["id"]),
                    n=n,
                    k=int(item["k"]),
                    j=int(item["j"]),
                    s=int(item["s"]),
                    baseline_blocks=int(item["baseline_blocks"]),
                )
            )
    return cases


def run_case(case: BaselineCase, time_limit: float, ratio_threshold: float) -> dict[str, object]:
    problem = Problem(m=45, n=case.n, k=case.k, j=case.j, s=case.s)
    samples = tuple(range(1, case.n + 1))
    started = time.monotonic()
    result = solve_problem(problem, samples, time_limit=time_limit)
    verified = verify_solution(problem, result.index_blocks)
    groups = len(result.blocks)
    ratio = groups / case.baseline_blocks
    return {
        "id": case.case_id,
        "n": case.n,
        "k": case.k,
        "j": case.j,
        "s": case.s,
        "baseline_blocks": case.baseline_blocks,
        "groups": groups,
        "ratio": round(ratio, 4),
        "within_threshold": ratio <= ratio_threshold,
        "verified_full": verified,
        "strategy": result.strategy,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run full n=15/n=16 validation against baseline block counts")
    parser.add_argument("--baseline", type=Path, default=BASELINE_FILE)
    parser.add_argument("--max-n", type=int, default=16)
    parser.add_argument("--time-limit", type=float, default=120.0)
    parser.add_argument("--ratio-threshold", type=float, default=1.15, help="quality target ratio against baseline block count")
    parser.add_argument("--only", help="comma-separated case ids to run")
    parser.add_argument("--output", type=Path, default=Path("baseline_validation_results.csv"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    cases = load_cases(args.baseline, args.max_n)
    if args.only:
        wanted = {case_id.strip() for case_id in args.only.split(",") if case_id.strip()}
        cases = [case for case in cases if case.case_id in wanted]
    rows = []
    failures = 0
    for index, case in enumerate(cases, 1):
        row = run_case(case, args.time_limit, args.ratio_threshold)
        rows.append(row)
        if not row["verified_full"] or not row["within_threshold"]:
            failures += 1
        print(
            f"{index}/{len(cases)} {row['id']} groups={row['groups']} baseline={row['baseline_blocks']} "
            f"ratio={row['ratio']} verified={row['verified_full']} strategy={row['strategy']}"
        )
    if rows:
        with args.output.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        worst = max(rows, key=lambda row: float(row["ratio"]))
        within = sum(1 for row in rows if row["within_threshold"])
        print(f"Wrote {args.output}")
        print(f"within_threshold={within}/{len(rows)} threshold={args.ratio_threshold} worst={worst['id']} ratio={worst['ratio']}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())