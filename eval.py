from __future__ import annotations

import argparse
import json
import os
import platform
import random
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from bounds import get_bounds
from solver import CoveringDesignSolver


ROOT = Path(__file__).resolve().parent
DEFAULT_BENCHMARKS = ROOT / "benchmark_cases.json"
RESULTS_DIR = ROOT / "results"
DEFAULT_OUTPUT = RESULTS_DIR / "latest_eval.json"
DEFAULT_BASELINE = RESULTS_DIR / "baseline.json"


def _git_value(*args: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None
    return out or None


def load_benchmarks(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_cases(data: dict[str, Any], suite: str) -> list[dict[str, Any]]:
    cases = [case for case in data["cases"] if suite in case["suites"]]
    if not cases:
        raise ValueError(f"No benchmark cases found for suite '{suite}'")
    return cases


def resolve_reference(case: dict[str, Any], bounds: dict[str, Any]) -> dict[str, Any]:
    ref = dict(case.get("reference", {}))
    ref_type = ref.get("type", "lower_bound")
    if ref_type in {"exact", "ljcr"}:
        value = ref.get("value")
        if value is None:
            raise ValueError(f"Case {case['id']} is missing reference value")
    elif ref_type == "lower_bound":
        value = bounds["lower_bound"]
    else:
        raise ValueError(f"Unsupported reference type '{ref_type}' for {case['id']}")

    return {
        "type": ref_type,
        "value": int(value),
        "source": ref.get("source", ""),
    }


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    n = int(case["n"])
    k = int(case["k"])
    j = int(case["j"])
    s = int(case["s"])
    num_attempts = int(case["num_attempts"])
    timeout_sec = float(case["timeout_sec"])
    seed = int(case["seed"])

    random.seed(seed)
    np.random.seed(seed)

    bounds = get_bounds(n, k, j, s)
    reference = resolve_reference(case, bounds)

    started_at = time.time()
    error = None
    result_payload: dict[str, Any]

    try:
        solver = CoveringDesignSolver(
            n=n,
            k=k,
            j=j,
            s=s,
            num_attempts=num_attempts,
            cancel_fn=lambda t0=started_at, limit=timeout_sec: (time.time() - t0) > limit,
        )
        solved = solver.solve()
        elapsed = time.time() - started_at
        ratio = solved.num_groups / reference["value"]
        quality_index = reference["value"] / solved.num_groups if solved.num_groups else 0.0
        status = "ok"
        if elapsed >= timeout_sec:
            status = "timeout"
        preview_limit = 20
        stored_groups = solved.groups if len(solved.groups) <= preview_limit else solved.groups[:preview_limit]
        result_payload = {
            "status": status,
            "verified": bool(solved.verified),
            "num_groups": int(solved.num_groups),
            "elapsed_sec": round(float(elapsed), 6),
            "first_legal_elapsed_sec": (
                round(float(solved.first_legal_elapsed), 6)
                if solved.first_legal_elapsed is not None
                else None
            ),
            "timed_out": elapsed >= timeout_sec,
            "ratio_to_reference": round(float(ratio), 6),
            "quality_index": round(float(quality_index), 6),
            "groups_preview": stored_groups,
            "groups_truncated": len(solved.groups) > preview_limit,
        }
    except Exception as exc:
        elapsed = time.time() - started_at
        error = str(exc)
        result_payload = {
            "status": "error",
            "verified": False,
            "num_groups": None,
            "elapsed_sec": round(float(elapsed), 6),
            "first_legal_elapsed_sec": None,
            "timed_out": elapsed >= timeout_sec,
            "ratio_to_reference": None,
            "quality_index": 0.0,
            "groups_preview": [],
            "groups_truncated": False,
        }

    return {
        "id": case["id"],
        "name": case["name"],
        "params": {"n": n, "k": k, "j": j, "s": s},
        "weight": float(case["weight"]),
        "seed": seed,
        "num_attempts": num_attempts,
        "timeout_sec": timeout_sec,
        "suites": list(case["suites"]),
        "reference": reference,
        "bounds": bounds,
        "result": result_payload,
        "error": error,
    }


def summarize_run(cases: list[dict[str, Any]], suite: str) -> dict[str, Any]:
    total_cases = len(cases)
    verified_cases = sum(1 for case in cases if case["result"]["verified"])
    failed_cases = total_cases - verified_cases
    total_weight = sum(case["weight"] for case in cases)
    weighted_quality = sum(case["weight"] * case["result"]["quality_index"] for case in cases) / total_weight

    verified_ratio_terms = [
        case["weight"] * case["result"]["ratio_to_reference"]
        for case in cases
        if case["result"]["verified"] and case["result"]["ratio_to_reference"] is not None
    ]
    verified_ratio_weight = sum(
        case["weight"]
        for case in cases
        if case["result"]["verified"] and case["result"]["ratio_to_reference"] is not None
    )
    weighted_quality_ratio = None
    if verified_ratio_terms and verified_ratio_weight:
        weighted_quality_ratio = sum(verified_ratio_terms) / verified_ratio_weight

    total_elapsed = sum(case["result"]["elapsed_sec"] for case in cases)
    total_timeout_budget = sum(case["timeout_sec"] for case in cases)
    score = (10000.0 * weighted_quality) - (10.0 * total_elapsed) - (5000.0 * failed_cases)

    reference_breakdown: dict[str, int] = {}
    for case in cases:
        ref_type = case["reference"]["type"]
        reference_breakdown[ref_type] = reference_breakdown.get(ref_type, 0) + 1

    return {
        "suite": suite,
        "case_count": total_cases,
        "verified_count": verified_cases,
        "failed_count": failed_cases,
        "weighted_quality": round(float(weighted_quality), 6),
        "weighted_quality_ratio_verified_only": (
            round(float(weighted_quality_ratio), 6) if weighted_quality_ratio is not None else None
        ),
        "total_elapsed_sec": round(float(total_elapsed), 6),
        "total_timeout_budget_sec": round(float(total_timeout_budget), 6),
        "score": round(float(score), 6),
        "reference_breakdown": reference_breakdown,
    }


def load_previous_run(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def compare_against_baseline(
    current_cases: list[dict[str, Any]],
    current_summary: dict[str, Any],
    baseline_payload: dict[str, Any] | None,
    baseline_path: Path,
) -> dict[str, Any] | None:
    if baseline_payload is None:
        return None

    baseline_cases = {case["id"]: case for case in baseline_payload.get("cases", [])}
    common_ids = [case["id"] for case in current_cases if case["id"] in baseline_cases]
    if not common_ids:
        return {
            "baseline_path": str(baseline_path),
            "baseline_suite": baseline_payload.get("summary", {}).get("suite"),
            "overlap_case_count": 0,
            "note": "No overlapping benchmark case IDs between the current run and the baseline."
        }

    improved_quality: list[str] = []
    regressed_quality: list[str] = []
    faster_cases: list[str] = []
    slower_cases: list[str] = []

    baseline_weight = 0.0
    baseline_weighted_quality = 0.0
    baseline_elapsed = 0.0
    baseline_verified = 0

    for case_id in common_ids:
        baseline_case = baseline_cases[case_id]
        baseline_weight += float(baseline_case["weight"])
        baseline_weighted_quality += float(baseline_case["weight"]) * float(
            baseline_case["result"]["quality_index"]
        )
        baseline_elapsed += float(baseline_case["result"]["elapsed_sec"])
        if baseline_case["result"]["verified"]:
            baseline_verified += 1

    current_case_map = {case["id"]: case for case in current_cases}
    current_weight = 0.0
    current_weighted_quality = 0.0
    current_elapsed = 0.0
    current_verified = 0

    for case_id in common_ids:
        current_case = current_case_map[case_id]
        baseline_case = baseline_cases[case_id]
        current_weight += float(current_case["weight"])
        current_weighted_quality += float(current_case["weight"]) * float(
            current_case["result"]["quality_index"]
        )
        current_elapsed += float(current_case["result"]["elapsed_sec"])
        if current_case["result"]["verified"]:
            current_verified += 1

        curr_groups = current_case["result"]["num_groups"]
        base_groups = baseline_case["result"]["num_groups"]
        curr_verified_case = current_case["result"]["verified"]
        base_verified_case = baseline_case["result"]["verified"]

        if curr_verified_case and not base_verified_case:
            improved_quality.append(case_id)
        elif base_verified_case and not curr_verified_case:
            regressed_quality.append(case_id)
        elif curr_verified_case and base_verified_case:
            if curr_groups < base_groups:
                improved_quality.append(case_id)
            elif curr_groups > base_groups:
                regressed_quality.append(case_id)

        curr_elapsed_case = float(current_case["result"]["elapsed_sec"])
        base_elapsed_case = float(baseline_case["result"]["elapsed_sec"])
        if curr_elapsed_case < base_elapsed_case:
            faster_cases.append(case_id)
        elif curr_elapsed_case > base_elapsed_case:
            slower_cases.append(case_id)

    baseline_overlap_quality = baseline_weighted_quality / baseline_weight if baseline_weight else 0.0
    current_overlap_quality = current_weighted_quality / current_weight if current_weight else 0.0
    baseline_overlap_score = (10000.0 * baseline_overlap_quality) - (10.0 * baseline_elapsed) - (
        5000.0 * (len(common_ids) - baseline_verified)
    )
    current_overlap_score = (10000.0 * current_overlap_quality) - (10.0 * current_elapsed) - (
        5000.0 * (len(common_ids) - current_verified)
    )

    return {
        "baseline_path": str(baseline_path),
        "baseline_suite": baseline_payload.get("summary", {}).get("suite"),
        "overlap_case_count": len(common_ids),
        "delta_score_on_overlap": round(float(current_overlap_score - baseline_overlap_score), 6),
        "delta_weighted_quality_on_overlap": round(
            float(current_overlap_quality - baseline_overlap_quality), 6
        ),
        "delta_total_elapsed_sec_on_overlap": round(float(current_elapsed - baseline_elapsed), 6),
        "delta_verified_count_on_overlap": int(current_verified - baseline_verified),
        "quality_improved_case_ids": improved_quality,
        "quality_regressed_case_ids": regressed_quality,
        "faster_case_ids": faster_cases,
        "slower_case_ids": slower_cases,
        "current_run_score": current_summary["score"],
    }


def build_payload(
    suite: str,
    benchmark_path: Path,
    cases: list[dict[str, Any]],
    baseline_payload: dict[str, Any] | None,
    baseline_path: Path,
) -> dict[str, Any]:
    summary = summarize_run(cases, suite)
    comparison = compare_against_baseline(cases, summary, baseline_payload, baseline_path)

    return {
        "format_version": 1,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "benchmark_file": str(benchmark_path),
        "repo": {
            "git_branch": _git_value("branch", "--show-current"),
            "git_commit": _git_value("rev-parse", "HEAD"),
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "ck_use_gpu": os.environ.get("CK_USE_GPU"),
            "ck_batch_bytes": os.environ.get("CK_BATCH_BYTES"),
        },
        "summary": summary,
        "comparison_to_baseline": comparison,
        "cases": cases,
    }


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def print_report(payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    print("=" * 110)
    print(f"Suite: {summary['suite']}")
    print("=" * 110)
    print(
        f"{'Case':<14} {'L(n,k,j,s)':<16} {'Ref':<14} {'Groups':>7} "
        f"{'Ratio':>8} {'Time':>9} {'1stOK':>9} {'OK':>4}"
    )
    print("-" * 110)
    for case in payload["cases"]:
        params = case["params"]
        result = case["result"]
        param_str = f"L({params['n']},{params['k']},{params['j']},{params['s']})"
        ref = case["reference"]
        ref_str = f"{ref['type']}:{ref['value']}"
        groups = result["num_groups"] if result["num_groups"] is not None else "ERR"
        ratio = (
            f"{result['ratio_to_reference']:.3f}"
            if result["ratio_to_reference"] is not None
            else "---"
        )
        ok = "yes" if result["verified"] else "no"
        first_legal = (
            f"{result['first_legal_elapsed_sec']:.2f}s"
            if result["first_legal_elapsed_sec"] is not None
            else "---"
        )
        print(
            f"{case['id']:<14} {param_str:<16} {ref_str:<14} {str(groups):>7} "
            f"{ratio:>8} {result['elapsed_sec']:>8.2f}s {first_legal:>9} {ok:>4}"
        )

    print("-" * 110)
    print(f"Verified: {summary['verified_count']}/{summary['case_count']}")
    print(f"Weighted quality: {summary['weighted_quality']:.6f}")
    ratio = summary["weighted_quality_ratio_verified_only"]
    if ratio is not None:
        print(f"Weighted ratio (verified only, lower is better): {ratio:.6f}")
    print(
        f"Total elapsed: {summary['total_elapsed_sec']:.2f}s / "
        f"{summary['total_timeout_budget_sec']:.2f}s budget"
    )
    print(f"Score: {summary['score']:.6f}")

    comparison = payload.get("comparison_to_baseline")
    if comparison:
        print()
        print(f"Compared with: {comparison['baseline_path']}")
        if comparison["overlap_case_count"] == 0:
            print(comparison["note"])
        else:
            print(f"Overlap cases: {comparison['overlap_case_count']}")
            print(f"Delta score: {comparison['delta_score_on_overlap']:+.6f}")
            print(
                "Delta weighted quality: "
                f"{comparison['delta_weighted_quality_on_overlap']:+.6f}"
            )
            print(
                "Delta total elapsed: "
                f"{comparison['delta_total_elapsed_sec_on_overlap']:+.6f}s"
            )
            print(
                "Quality improved on: "
                + (", ".join(comparison["quality_improved_case_ids"]) or "none")
            )
            print(
                "Quality regressed on: "
                + (", ".join(comparison["quality_regressed_case_ids"]) or "none")
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run deterministic solver benchmarks.")
    parser.add_argument(
        "--suite",
        choices=["smoke", "core", "full"],
        default=None,
        help="Benchmark suite to run (default: benchmark_cases.json default_suite).",
    )
    parser.add_argument(
        "--benchmarks",
        default=str(DEFAULT_BENCHMARKS),
        help="Path to benchmark_cases.json",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to write the latest evaluation JSON",
    )
    parser.add_argument(
        "--baseline",
        default=str(DEFAULT_BASELINE),
        help="Path to the stable baseline JSON",
    )
    parser.add_argument(
        "--write-baseline",
        action="store_true",
        help="Also overwrite the baseline JSON with the current run.",
    )
    args = parser.parse_args()

    benchmark_path = Path(args.benchmarks).resolve()
    output_path = Path(args.output).resolve()
    baseline_path = Path(args.baseline).resolve()

    benchmark_data = load_benchmarks(benchmark_path)
    suite = args.suite or benchmark_data.get("default_suite", "core")
    selected = select_cases(benchmark_data, suite)
    baseline_payload = load_previous_run(baseline_path)

    cases = [run_case(case) for case in selected]
    payload = build_payload(suite, benchmark_path, cases, baseline_payload, baseline_path)

    save_json(output_path, payload)
    if args.write_baseline:
        baseline_copy = dict(payload)
        baseline_copy["comparison_to_baseline"] = None
        save_json(baseline_path, baseline_copy)

    print_report(payload)


if __name__ == "__main__":
    main()
