from __future__ import annotations

import argparse
import json
import random
import re
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import requests

from solver import CoveringDesignSolver


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
DEFAULT_BASELINE_OUT = RESULTS_DIR / "coveringrepo_n_lt_12_baselines.json"
DEFAULT_COMPARE_OUT = RESULTS_DIR / "n_lt_12_coveringrepo_compare.json"

ROW_RE = re.compile(
    r"^\|\s*(\d{2})\s*\|\s*(\d{2})\s*\|\s*(\d{2})\s*\|\s*(\d{2})\s*\|\s*(\d+)\s*\|"
)


@dataclass(frozen=True)
class CaseKey:
    n: int
    k: int
    j: int
    s: int

    def as_id(self) -> str:
        return f"L_{self.n}_{self.k}_{self.j}_{self.s}"


def _page_url(k: int, j: int, s: int) -> str:
    return (
        "https://r.jina.ai/http://www.coveringrepository.com/"
        f"systems.aspx?k={k:02d}&m={j:02d}&t={s:02d}"
    )


def _fetch_text(url: str, session: requests.Session, retries: int = 12) -> str:
    last_err: Exception | None = None
    alt_url = url.replace(
        "http://www.coveringrepository.com/",
        "http://coveringrepository.com/",
    )
    for idx in range(retries):
        try:
            target = url if (idx % 2 == 0) else alt_url
            resp = session.get(target, timeout=120)
            if resp.status_code == 200 and "Title: Covering Repository" in resp.text:
                return resp.text
            if resp.status_code == 429:
                raise RuntimeError("status=429")
            raise RuntimeError(f"status={resp.status_code}")
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            wait_sec = 2.5 * (idx + 1)
            if "429" in str(exc):
                wait_sec = 10.0 * (idx + 1)
            time.sleep(wait_sec)
    raise RuntimeError(f"failed to fetch {url}: {last_err}")


def _parse_rows(text: str) -> list[tuple[int, int, int, int, int]]:
    rows: list[tuple[int, int, int, int, int]] = []
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        v, k, t, m_val, b = map(int, m.groups())
        rows.append((v, k, t, m_val, b))
    return rows


def collect_coveringrepo_baselines(
    *,
    n_min: int,
    n_max_exclusive: int,
) -> dict[CaseKey, dict[str, Any]]:
    out: dict[CaseKey, dict[str, Any]] = {}
    session = requests.Session()
    for k in range(4, 8):
        for s in range(3, min(7, k) + 1):
            for j in range(s, k + 1):
                source_url = _page_url(k, j, s)
                text = _fetch_text(source_url, session)
                rows = _parse_rows(text)
                if not rows:
                    continue
                time.sleep(1.5)
                for v, row_k, row_t, row_m, blocks in rows:
                    if not (n_min <= v < n_max_exclusive):
                        continue
                    if not (4 <= row_k <= 7 and 3 <= row_t <= 7 and row_t <= row_m <= row_k):
                        continue
                    if v < row_k:
                        continue
                    key = CaseKey(n=v, k=row_k, j=row_m, s=row_t)
                    prev = out.get(key)
                    if prev is None or blocks < int(prev["baseline_blocks"]):
                        out[key] = {
                            "baseline_blocks": int(blocks),
                            "source_page": source_url,
                        }
    return out


def _independent_verify(groups: list[list[int]], n: int, j: int, s: int) -> bool:
    group_sets = [set(g) for g in groups]
    universe = range(n)
    for tgt in combinations(universe, j):
        tgt_set = set(tgt)
        ok = False
        for grp in group_sets:
            if len(tgt_set & grp) >= s:
                ok = True
                break
        if not ok:
            return False
    return True


def _case_family(n: int, k: int, j: int, s: int) -> str:
    if s == j == k:
        return "identity_cover"
    if s == j and j < k:
        return "containment_s_eq_j"
    if j == k and s < j:
        if n <= 9:
            return "j_eq_k_noncontain_small_n"
        return "j_eq_k_noncontain_medium_n"
    return "general_noncontain"


def run_solver_compare(
    cases: list[dict[str, Any]],
    *,
    timeout_sec: float,
    num_attempts: int,
    base_seed: int,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    total = len(cases)
    for idx, case in enumerate(cases):
        n = int(case["n"])
        k = int(case["k"])
        j = int(case["j"])
        s = int(case["s"])
        baseline = int(case["baseline_blocks"])
        print(
            f"[{idx + 1:03d}/{total:03d}] solve L({n},{k},{j},{s}) baseline={baseline}",
            flush=True,
        )
        seed = base_seed + idx * 17 + n * 101 + k * 29 + j * 13 + s

        random.seed(seed)
        np.random.seed(seed)

        started = time.time()
        solver = CoveringDesignSolver(
            n=n,
            k=k,
            j=j,
            s=s,
            num_attempts=num_attempts,
            time_budget_sec=timeout_sec,
            cancel_fn=lambda t0=started, lim=timeout_sec: (time.time() - t0) > lim,
        )
        solved = solver.solve()
        elapsed = time.time() - started
        num_groups = int(solved.num_groups)
        gap_ratio = (num_groups - baseline) / baseline
        abs_gap_ratio = abs(gap_ratio)

        independent_verified = _independent_verify(solved.groups, n=n, j=j, s=s)
        better_than_baseline = num_groups < baseline
        worse_than_baseline = num_groups > baseline
        over_10 = abs_gap_ratio > 0.10

        proof: dict[str, Any] | None = None
        if better_than_baseline:
            proof = {
                "required": True,
                "solver_verified": bool(solved.verified),
                "independent_verified": bool(independent_verified),
                "proved": bool(solved.verified and independent_verified),
            }
        elif over_10:
            proof = {
                "required": False,
                "solver_verified": bool(solved.verified),
                "independent_verified": bool(independent_verified),
            }

        results.append(
            {
                "id": case["id"],
                "n": n,
                "k": k,
                "j": j,
                "s": s,
                "family": _case_family(n, k, j, s),
                "baseline_blocks": baseline,
                "solver_blocks": num_groups,
                "elapsed_sec": round(float(elapsed), 6),
                "first_legal_elapsed_sec": (
                    round(float(solved.first_legal_elapsed), 6)
                    if solved.first_legal_elapsed is not None
                    else None
                ),
                "solver_verified": bool(solved.verified),
                "independent_verified": bool(independent_verified),
                "gap_ratio": round(float(gap_ratio), 6),
                "abs_gap_ratio": round(float(abs_gap_ratio), 6),
                "over_10_percent": bool(over_10),
                "worse_than_baseline": bool(worse_than_baseline),
                "better_than_baseline": bool(better_than_baseline),
                "needs_optimization": bool(worse_than_baseline and over_10),
                "source_page": case["source_page"],
                "proof": proof,
            }
        )
        print(
            f"         -> solver={num_groups} gap={gap_ratio:+.3%} "
            f"elapsed={elapsed:.2f}s verified={bool(solved.verified and independent_verified)}",
            flush=True,
        )
    return results


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    over_10 = [r for r in results if r["over_10_percent"]]
    needs_opt = [r for r in results if r["needs_optimization"]]
    better = [r for r in results if r["better_than_baseline"]]
    better_and_over10 = [r for r in better if r["over_10_percent"]]
    unverified = [r for r in results if not r["solver_verified"] or not r["independent_verified"]]

    buckets: dict[str, dict[str, Any]] = {}
    for row in needs_opt:
        fam = row["family"]
        b = buckets.setdefault(
            fam,
            {
                "count": 0,
                "avg_gap_ratio": 0.0,
                "max_gap_ratio": 0.0,
                "cases": [],
            },
        )
        b["count"] += 1
        b["avg_gap_ratio"] += float(row["gap_ratio"])
        b["max_gap_ratio"] = max(float(b["max_gap_ratio"]), float(row["gap_ratio"]))
        b["cases"].append(row["id"])

    for fam, b in buckets.items():
        if b["count"] > 0:
            b["avg_gap_ratio"] = round(float(b["avg_gap_ratio"] / b["count"]), 6)
        b["max_gap_ratio"] = round(float(b["max_gap_ratio"]), 6)
        b["cases"] = sorted(b["cases"])
        buckets[fam] = b

    worst = sorted(needs_opt, key=lambda x: x["gap_ratio"], reverse=True)[:30]

    return {
        "total_cases": total,
        "over_10_percent_count": len(over_10),
        "needs_optimization_count": len(needs_opt),
        "better_than_baseline_count": len(better),
        "better_than_baseline_over_10_count": len(better_and_over10),
        "all_results_verified_count": total - len(unverified),
        "unverified_case_count": len(unverified),
        "optimization_buckets": buckets,
        "worst_cases_top30": [
            {
                "id": r["id"],
                "n": r["n"],
                "k": r["k"],
                "j": r["j"],
                "s": r["s"],
                "baseline_blocks": r["baseline_blocks"],
                "solver_blocks": r["solver_blocks"],
                "gap_ratio": r["gap_ratio"],
                "family": r["family"],
            }
            for r in worst
        ],
    }


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="对比 n<12 的 CoveringRepository 基线与当前求解器结果。"
    )
    parser.add_argument("--timeout-sec", type=float, default=120.0)
    parser.add_argument("--num-attempts", type=int, default=3)
    parser.add_argument("--base-seed", type=int, default=20260424)
    parser.add_argument("--n-min", type=int, default=7)
    parser.add_argument("--n-max-exclusive", type=int, default=12)
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument("--skip-solve", action="store_true")
    parser.add_argument("--refresh-baseline", action="store_true")
    parser.add_argument("--baseline-out", type=Path, default=DEFAULT_BASELINE_OUT)
    parser.add_argument("--compare-out", type=Path, default=DEFAULT_COMPARE_OUT)
    args = parser.parse_args()

    baseline_cases: list[dict[str, Any]]
    should_write_baseline = False
    if args.baseline_out.exists() and not args.refresh_baseline:
        cached = json.loads(args.baseline_out.read_text(encoding="utf-8"))
        baseline_cases = list(cached.get("cases", []))
        if not baseline_cases:
            raise RuntimeError(
                f"cached baseline file is empty: {args.baseline_out}. "
                "Use --refresh-baseline to rebuild."
            )
    else:
        baselines = collect_coveringrepo_baselines(
            n_min=int(args.n_min),
            n_max_exclusive=int(args.n_max_exclusive),
        )
        baseline_cases = []
        for key in sorted(baselines.keys(), key=lambda x: (x.n, x.k, x.j, x.s)):
            rec = baselines[key]
            baseline_cases.append(
                {
                    "id": key.as_id(),
                    "n": key.n,
                    "k": key.k,
                    "j": key.j,
                    "s": key.s,
                    "baseline_blocks": int(rec["baseline_blocks"]),
                    "source_page": rec["source_page"],
                }
            )
        should_write_baseline = True

    full_baseline_cases = list(baseline_cases)
    if args.max_cases is not None:
        baseline_cases = baseline_cases[: max(0, args.max_cases)]

    if should_write_baseline:
        baseline_payload = {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "source": "https://www.coveringrepository.com/systems.aspx",
            "proxy": "https://r.jina.ai/http://www.coveringrepository.com",
            "filters": {
                "n_min": int(args.n_min),
                "n_max_exclusive": int(args.n_max_exclusive),
                "k_min": 4,
                "k_max": 7,
                "s_min": 3,
                "s_max": 7,
                "constraint": "s <= j <= k and n >= k",
            },
            "case_count": len(full_baseline_cases),
            "cases": full_baseline_cases,
        }
        save_json(args.baseline_out, baseline_payload)

    if args.skip_solve:
        print(f"Collected baseline cases: {len(baseline_cases)}")
        print(f"Baseline saved to: {args.baseline_out}")
        return

    compared = run_solver_compare(
        baseline_cases,
        timeout_sec=float(args.timeout_sec),
        num_attempts=max(1, int(args.num_attempts)),
        base_seed=int(args.base_seed),
    )
    summary = summarize(compared)

    compare_payload = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "config": {
            "timeout_sec": float(args.timeout_sec),
            "num_attempts": int(args.num_attempts),
            "base_seed": int(args.base_seed),
            "max_cases": args.max_cases,
        },
        "source_baseline_file": str(args.baseline_out),
        "summary": summary,
        "cases": compared,
    }
    save_json(args.compare_out, compare_payload)

    print(f"Compared cases: {len(compared)}")
    print(f"Needs optimization (>10% worse): {summary['needs_optimization_count']}")
    print(f"Over 10% total deviations: {summary['over_10_percent_count']}")
    print(f"All verified count: {summary['all_results_verified_count']}/{summary['total_cases']}")
    print(f"Baseline saved to: {args.baseline_out}")
    print(f"Compare report saved to: {args.compare_out}")


if __name__ == "__main__":
    main()
