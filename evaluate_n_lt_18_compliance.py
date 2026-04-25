from __future__ import annotations

import argparse
import importlib
import json
import math
import os
import random
import statistics
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
DEFAULT_BASELINE = RESULTS_DIR / "coveringrepo_n_lt_26_baselines.json"
DEFAULT_OUTPUT_JSON = RESULTS_DIR / "n_lt_18_compliance_120s_10pct_gpu.json"
DEFAULT_OUTPUT_MD = RESULTS_DIR / "n_lt_18_compliance_120s_10pct_gpu.md"
DEFAULT_SPLIT_MD = RESULTS_DIR / "n_lt_16_vs_n_ge_16_lt_18_analysis_gpu.md"


def _default_python_exe() -> str:
    if os.name == "nt":
        venv_python = ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def _classify_family(n: int, k: int, j: int, s: int) -> str:
    if j == k and s == k:
        return "identity_cover"
    if s == j:
        return "containment_s_eq_j"
    if j == k:
        return "j_eq_k_noncontain_medium_n"
    return "general_noncontain"


def _case_seed(n: int, k: int, j: int, s: int) -> int:
    return ((n * 1000 + k * 100 + j * 10 + s) * 104729) % (2**31 - 1)


def _safe_mean(values: list[float]) -> float | None:
    if not values:
        return None
    return float(statistics.mean(values))


def _safe_median(values: list[float]) -> float | None:
    if not values:
        return None
    return float(statistics.median(values))


def _fmt_float(value: float | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    return round(float(value), digits)


@dataclass(frozen=True)
class SolverDispatchConfig:
    profile_name: str
    ck_use_gpu: int
    ck_skip_gpu_probe: bool
    ck_n16_anchor_module: int
    ck_disable_cpsat: int
    ck_solver_module: str


def _resolve_solver_dispatch_config(*, n: int, args: argparse.Namespace) -> SolverDispatchConfig:
    if int(n) == 16:
        return SolverDispatchConfig(
            profile_name="n16_isolated",
            ck_use_gpu=int(args.ck_use_gpu_n16),
            ck_skip_gpu_probe=bool(int(args.ck_skip_gpu_probe_n16)),
            ck_n16_anchor_module=int(args.ck_n16_anchor_module_n16),
            ck_disable_cpsat=int(args.ck_disable_cpsat_n16),
            ck_solver_module=str(args.ck_solver_module_n16 or "solver_n16_isolated"),
        )
    return SolverDispatchConfig(
        profile_name="default",
        ck_use_gpu=int(args.ck_use_gpu),
        ck_skip_gpu_probe=bool(args.ck_skip_gpu_probe),
        ck_n16_anchor_module=int(args.ck_n16_anchor_module),
        ck_disable_cpsat=int(args.ck_disable_cpsat),
        ck_solver_module=str(args.ck_solver_module or "solver"),
    )


def _run_one_case_locally(
    *,
    n: int,
    k: int,
    j: int,
    s: int,
    timeout_sec: float,
    num_attempts: int,
    seed: int,
) -> dict[str, Any]:
    # Lazy import keeps startup light for parent process.
    solver_module_name = os.environ.get("CK_SOLVER_MODULE", "solver")
    solver_profile_name = os.environ.get("CK_SOLVER_PROFILE", "default")
    solver_module = importlib.import_module(solver_module_name)
    CoveringDesignSolver = getattr(solver_module, "CoveringDesignSolver")

    random.seed(seed)
    np.random.seed(seed)

    started_at = time.time()
    try:
        solver = CoveringDesignSolver(
            n=n,
            k=k,
            j=j,
            s=s,
            num_attempts=num_attempts,
            time_budget_sec=timeout_sec,
            cancel_fn=lambda t0=started_at, limit=timeout_sec: (time.time() - t0) > limit,
        )
        solved = solver.solve()
        elapsed = time.time() - started_at
        return {
            "status": "timeout" if elapsed > timeout_sec else "ok",
            "solver_blocks": int(solved.num_groups),
            "elapsed_sec": float(elapsed),
            "first_legal_elapsed_sec": (
                float(solved.first_legal_elapsed)
                if solved.first_legal_elapsed is not None
                else None
            ),
            "solver_verified": bool(solved.verified),
            "solver_module": solver_module_name,
            "solver_profile": solver_profile_name,
            "error": None,
        }
    except Exception as exc:  # pragma: no cover - defensive path.
        elapsed = time.time() - started_at
        return {
            "status": "error",
            "solver_blocks": None,
            "elapsed_sec": float(elapsed),
            "first_legal_elapsed_sec": None,
            "solver_verified": False,
            "solver_module": solver_module_name,
            "solver_profile": solver_profile_name,
            "error": str(exc),
        }


def _run_one_case_subprocess(
    *,
    n: int,
    k: int,
    j: int,
    s: int,
    timeout_sec: float,
    hard_timeout_sec: float,
    num_attempts: int,
    seed: int,
    python_exe: str,
    solver_config: SolverDispatchConfig,
) -> dict[str, Any]:
    solver_module_name = str(solver_config.ck_solver_module or "solver")
    cmd = [
        python_exe,
        str(Path(__file__).resolve()),
        "--run-one",
        "--n",
        str(n),
        "--k",
        str(k),
        "--j",
        str(j),
        "--s",
        str(s),
        "--timeout-sec",
        str(timeout_sec),
        "--num-attempts",
        str(num_attempts),
        "--seed",
        str(seed),
        "--ck-use-gpu",
        str(int(bool(solver_config.ck_use_gpu))),
        "--ck-n16-anchor-module",
        str(int(bool(solver_config.ck_n16_anchor_module))),
        "--ck-disable-cpsat",
        str(int(bool(solver_config.ck_disable_cpsat))),
        "--ck-solver-module",
        solver_module_name,
    ]
    if solver_config.ck_skip_gpu_probe:
        cmd.append("--ck-skip-gpu-probe")
    env = os.environ.copy()
    env["CK_USE_GPU"] = str(int(bool(solver_config.ck_use_gpu)))
    if solver_config.ck_skip_gpu_probe:
        env["CK_SKIP_GPU_PROBE"] = "1"
    else:
        env.pop("CK_SKIP_GPU_PROBE", None)
    env["CK_N16_ANCHOR_MODULE"] = str(int(bool(solver_config.ck_n16_anchor_module)))
    env["CK_DISABLE_CPSAT"] = str(int(bool(solver_config.ck_disable_cpsat)))
    env["CK_SOLVER_MODULE"] = solver_module_name
    env["CK_SOLVER_PROFILE"] = str(solver_config.profile_name or "default")

    started_at = time.time()
    try:
        completed = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=hard_timeout_sec,
            env=env,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.time() - started_at
        return {
            "status": "timeout",
            "solver_blocks": None,
            "elapsed_sec": float(elapsed),
            "first_legal_elapsed_sec": None,
            "solver_verified": False,
            "solver_module": solver_config.ck_solver_module,
            "solver_profile": solver_config.profile_name,
            "error": f"subprocess-timeout>{hard_timeout_sec:.1f}s",
        }

    elapsed = time.time() - started_at
    if completed.returncode != 0:
        err = completed.stderr.strip() or completed.stdout.strip() or f"returncode={completed.returncode}"
        return {
            "status": "error",
            "solver_blocks": None,
            "elapsed_sec": float(elapsed),
            "first_legal_elapsed_sec": None,
            "solver_verified": False,
            "solver_module": solver_config.ck_solver_module,
            "solver_profile": solver_config.profile_name,
            "error": err,
        }

    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        return {
            "status": "error",
            "solver_blocks": None,
            "elapsed_sec": float(elapsed),
            "first_legal_elapsed_sec": None,
            "solver_verified": False,
            "solver_module": solver_config.ck_solver_module,
            "solver_profile": solver_config.profile_name,
            "error": "child returned empty stdout",
        }

    try:
        payload = json.loads(lines[-1])
    except json.JSONDecodeError:
        return {
            "status": "error",
            "solver_blocks": None,
            "elapsed_sec": float(elapsed),
            "first_legal_elapsed_sec": None,
            "solver_verified": False,
            "solver_module": solver_config.ck_solver_module,
            "solver_profile": solver_config.profile_name,
            "error": f"child returned non-json output: {lines[-1][:200]}",
        }

    if "elapsed_sec" not in payload:
        payload["elapsed_sec"] = float(elapsed)
    payload.setdefault("solver_module", solver_config.ck_solver_module)
    payload.setdefault("solver_profile", solver_config.profile_name)
    return payload


def _evaluate_case(
    *,
    case: dict[str, Any],
    run_result: dict[str, Any],
    timeout_sec: float,
    quality_tolerance_ratio: float,
) -> dict[str, Any]:
    n = int(case["n"])
    k = int(case["k"])
    j = int(case["j"])
    s = int(case["s"])
    baseline = int(case["baseline_blocks"])
    solver_blocks = run_result.get("solver_blocks")
    elapsed_sec = float(run_result.get("elapsed_sec", 0.0))
    first_legal_elapsed = run_result.get("first_legal_elapsed_sec")
    status = str(run_result.get("status", "error"))
    solver_verified = bool(run_result.get("solver_verified", False))
    solver_module = str(run_result.get("solver_module", "solver"))
    solver_profile = str(run_result.get("solver_profile", "default"))

    gap_ratio = None
    abs_gap_ratio = None
    quality_ratio_to_baseline = None
    quality_ok = False
    if isinstance(solver_blocks, int) and solver_blocks > 0:
        gap_ratio = (solver_blocks - baseline) / baseline
        abs_gap_ratio = abs(gap_ratio)
        quality_ratio_to_baseline = solver_blocks / baseline
        quality_ok = quality_ratio_to_baseline <= (1.0 + quality_tolerance_ratio)

    runtime_ok = elapsed_sec <= timeout_sec
    verified_ok = solver_verified

    reasons: list[str] = []
    if not runtime_ok:
        reasons.append("timeout_over_120s")
    if not quality_ok:
        reasons.append("quality_over_10pct")
    if not verified_ok:
        reasons.append("verification_failed")
    if status == "timeout" and "timeout_over_120s" not in reasons:
        reasons.append("timeout_over_120s")
    if status == "error":
        reasons.append("status_error")

    compliant = runtime_ok and quality_ok and verified_ok and status == "ok"
    num_targets = math.comb(n, j)
    num_cands = math.comb(n, k)
    interaction_scale = num_targets * num_cands

    return {
        "id": case["id"],
        "n": n,
        "k": k,
        "j": j,
        "s": s,
        "family": _classify_family(n, k, j, s),
        "baseline_blocks": baseline,
        "baseline_source": "coveringrepo_cached",
        "source_page": case.get("source_page"),
        "status": status,
        "solver_blocks": solver_blocks,
        "gap_ratio": _fmt_float(gap_ratio),
        "abs_gap_ratio": _fmt_float(abs_gap_ratio),
        "quality_ratio_to_baseline": _fmt_float(quality_ratio_to_baseline),
        "elapsed_sec": _fmt_float(elapsed_sec),
        "first_legal_elapsed_sec": _fmt_float(first_legal_elapsed),
        "runtime_for_judge_sec": _fmt_float(elapsed_sec),
        "runtime_ok": runtime_ok,
        "quality_ok": quality_ok,
        "solver_verified": solver_verified,
        "solver_module": solver_module,
        "solver_profile": solver_profile,
        "verified_ok": verified_ok,
        "compliant": compliant,
        "error": run_result.get("error"),
        "num_targets": num_targets,
        "num_cands": num_cands,
        "interaction_scale": interaction_scale,
        "non_compliant_reasons": reasons,
    }


def _build_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(cases)
    compliant = sum(1 for c in cases if c["compliant"])
    non_compliant = total - compliant
    runtime_fail = sum(1 for c in cases if not c["runtime_ok"])
    quality_fail = sum(1 for c in cases if not c["quality_ok"])
    verify_fail = sum(1 for c in cases if not c["verified_ok"])
    status_timeout = sum(1 for c in cases if c["status"] == "timeout")
    status_error = sum(1 for c in cases if c["status"] == "error")
    elapsed_total = sum(float(c["elapsed_sec"] or 0.0) for c in cases)
    return {
        "total_cases": total,
        "compliant_count": compliant,
        "non_compliant_count": non_compliant,
        "runtime_fail_count": runtime_fail,
        "quality_fail_count": quality_fail,
        "verify_fail_count": verify_fail,
        "status_timeout_count": status_timeout,
        "status_error_count": status_error,
        "elapsed_total_sec": _fmt_float(elapsed_total),
    }


def _by_n_summary(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for n in sorted({int(c["n"]) for c in cases}):
        subset = [c for c in cases if int(c["n"]) == n]
        out.append(
            {
                "n": n,
                "total": len(subset),
                "compliant": sum(1 for c in subset if c["compliant"]),
                "non_compliant": sum(1 for c in subset if not c["compliant"]),
                "quality_fail": sum(1 for c in subset if not c["quality_ok"]),
                "runtime_fail": sum(1 for c in subset if not c["runtime_ok"]),
                "verify_fail": sum(1 for c in subset if not c["verified_ok"]),
                "avg_gap_ratio": _fmt_float(
                    _safe_mean(
                        [
                            float(c["gap_ratio"])
                            for c in subset
                            if c["gap_ratio"] is not None
                        ]
                    )
                ),
                "avg_elapsed_sec": _fmt_float(
                    _safe_mean([float(c["elapsed_sec"] or 0.0) for c in subset])
                ),
            }
        )
    return out


def _batch_analysis(cases: list[dict[str, Any]], label: str) -> dict[str, Any]:
    non_compliant = [c for c in cases if not c["compliant"]]
    gap_values = [float(c["gap_ratio"]) for c in cases if c["gap_ratio"] is not None]
    non_gap_values = [float(c["gap_ratio"]) for c in non_compliant if c["gap_ratio"] is not None]
    first_legal = [
        float(c["first_legal_elapsed_sec"])
        for c in cases
        if c["first_legal_elapsed_sec"] is not None
    ]
    elapsed = [float(c["elapsed_sec"] or 0.0) for c in cases]

    family_stats: dict[str, Any] = {}
    for fam in sorted({c["family"] for c in cases}):
        fam_cases = [c for c in cases if c["family"] == fam]
        fam_non = [c for c in fam_cases if not c["compliant"]]
        family_stats[fam] = {
            "total": len(fam_cases),
            "compliant": sum(1 for c in fam_cases if c["compliant"]),
            "non_compliant": len(fam_non),
            "quality_fail": sum(1 for c in fam_cases if not c["quality_ok"]),
            "runtime_fail": sum(1 for c in fam_cases if not c["runtime_ok"]),
            "verify_fail": sum(1 for c in fam_cases if not c["verified_ok"]),
            "avg_gap_ratio": _fmt_float(
                _safe_mean([float(c["gap_ratio"]) for c in fam_cases if c["gap_ratio"] is not None])
            ),
            "avg_elapsed_sec": _fmt_float(
                _safe_mean([float(c["elapsed_sec"] or 0.0) for c in fam_cases])
            ),
        }

    worst = sorted(
        [c for c in non_compliant if c["gap_ratio"] is not None],
        key=lambda c: float(c["gap_ratio"]),
        reverse=True,
    )[:15]
    slowest = sorted(non_compliant, key=lambda c: float(c["elapsed_sec"] or 0.0), reverse=True)[:15]

    return {
        "label": label,
        "summary": _build_summary(cases),
        "avg_gap_ratio": _fmt_float(_safe_mean(gap_values)),
        "median_gap_ratio": _fmt_float(_safe_median(gap_values)),
        "avg_gap_ratio_non_compliant": _fmt_float(_safe_mean(non_gap_values)),
        "median_gap_ratio_non_compliant": _fmt_float(_safe_median(non_gap_values)),
        "avg_elapsed_sec": _fmt_float(_safe_mean(elapsed)),
        "median_elapsed_sec": _fmt_float(_safe_median(elapsed)),
        "avg_first_legal_elapsed_sec": _fmt_float(_safe_mean(first_legal)),
        "family_stats": family_stats,
        "worst_gap_top15": [
            {
                "id": c["id"],
                "n": c["n"],
                "k": c["k"],
                "j": c["j"],
                "s": c["s"],
                "baseline_blocks": c["baseline_blocks"],
                "solver_blocks": c["solver_blocks"],
                "gap_ratio": c["gap_ratio"],
                "elapsed_sec": c["elapsed_sec"],
                "family": c["family"],
                "reasons": c["non_compliant_reasons"],
            }
            for c in worst
        ],
        "slowest_top15": [
            {
                "id": c["id"],
                "n": c["n"],
                "k": c["k"],
                "j": c["j"],
                "s": c["s"],
                "baseline_blocks": c["baseline_blocks"],
                "solver_blocks": c["solver_blocks"],
                "gap_ratio": c["gap_ratio"],
                "elapsed_sec": c["elapsed_sec"],
                "family": c["family"],
                "reasons": c["non_compliant_reasons"],
            }
            for c in slowest
        ],
    }


def _save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _render_main_markdown(payload: dict[str, Any]) -> str:
    cfg = payload["config"]
    summary = payload["summary"]
    lines: list[str] = []
    lines.append("# n<18 compliance rerun (120s + 10% + GPU)")
    lines.append("")
    lines.append(f"- generated_at: {payload['generated_at']}")
    lines.append(f"- baseline_file: `{payload['baseline_file']}`")
    lines.append(f"- n_range: [{cfg['n_min']}, {cfg['n_max_exclusive']})")
    lines.append(f"- timeout_sec: {cfg['timeout_sec']}")
    lines.append(f"- hard_timeout_sec: {cfg['hard_timeout_sec']}")
    lines.append(f"- num_attempts: {cfg['num_attempts']}")
    lines.append(f"- workers: {cfg.get('workers', 1)}")
    lines.append(f"- CK_USE_GPU: {cfg['ck_use_gpu']}")
    lines.append("")
    lines.append("## summary")
    lines.append("")
    for key in [
        "total_cases",
        "compliant_count",
        "non_compliant_count",
        "runtime_fail_count",
        "quality_fail_count",
        "verify_fail_count",
        "status_timeout_count",
        "status_error_count",
        "elapsed_total_sec",
    ]:
        lines.append(f"- {key}: {summary[key]}")

    lines.append("")
    lines.append("## by_n")
    lines.append("")
    lines.append("| n | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in payload["by_n"]:
        lines.append(
            "| {n} | {total} | {compliant} | {non_compliant} | {quality_fail} | {runtime_fail} | {verify_fail} | {avg_gap_ratio} | {avg_elapsed_sec} |".format(
                **row
            )
        )

    non_compliant = [c for c in payload["cases"] if not c["compliant"]]
    non_compliant_sorted = sorted(
        [c for c in non_compliant if c["gap_ratio"] is not None],
        key=lambda c: float(c["gap_ratio"]),
        reverse=True,
    )[:40]
    lines.append("")
    lines.append("## non_compliant_top40_by_gap")
    lines.append("")
    lines.append("| id | n | k | j | s | baseline | solver | gap | elapsed_sec | family | reasons |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |")
    for c in non_compliant_sorted:
        lines.append(
            f"| {c['id']} | {c['n']} | {c['k']} | {c['j']} | {c['s']} | {c['baseline_blocks']} | {c['solver_blocks']} | {c['gap_ratio']} | {c['elapsed_sec']} | {c['family']} | {';'.join(c['non_compliant_reasons'])} |"
        )

    return "\n".join(lines) + "\n"


def _render_split_markdown(split_payload: dict[str, Any]) -> str:
    def render_block(name: str, block: dict[str, Any]) -> list[str]:
        s = block["summary"]
        lines: list[str] = []
        lines.append(f"## {name}")
        lines.append("")
        for key in [
            "total_cases",
            "compliant_count",
            "non_compliant_count",
            "quality_fail_count",
            "runtime_fail_count",
            "verify_fail_count",
            "elapsed_total_sec",
        ]:
            lines.append(f"- {key}: {s[key]}")
        lines.append(f"- avg_gap_ratio: {block['avg_gap_ratio']}")
        lines.append(f"- median_gap_ratio: {block['median_gap_ratio']}")
        lines.append(f"- avg_gap_ratio_non_compliant: {block['avg_gap_ratio_non_compliant']}")
        lines.append(f"- avg_elapsed_sec: {block['avg_elapsed_sec']}")
        lines.append("")
        lines.append("| family | total | compliant | non_compliant | quality_fail | runtime_fail | verify_fail | avg_gap | avg_elapsed_sec |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for fam, stat in block["family_stats"].items():
            lines.append(
                f"| {fam} | {stat['total']} | {stat['compliant']} | {stat['non_compliant']} | {stat['quality_fail']} | {stat['runtime_fail']} | {stat['verify_fail']} | {stat['avg_gap_ratio']} | {stat['avg_elapsed_sec']} |"
            )
        lines.append("")
        lines.append("### worst_gap_top15")
        lines.append("")
        lines.append("| id | params | baseline | solver | gap | elapsed_sec | family | reasons |")
        lines.append("| --- | --- | ---: | ---: | ---: | ---: | --- | --- |")
        for c in block["worst_gap_top15"]:
            lines.append(
                f"| {c['id']} | L({c['n']},{c['k']},{c['j']},{c['s']}) | {c['baseline_blocks']} | {c['solver_blocks']} | {c['gap_ratio']} | {c['elapsed_sec']} | {c['family']} | {';'.join(c['reasons'])} |"
            )
        lines.append("")
        lines.append("### slowest_top15")
        lines.append("")
        lines.append("| id | params | elapsed_sec | baseline | solver | gap | family | reasons |")
        lines.append("| --- | --- | ---: | ---: | ---: | ---: | --- | --- |")
        for c in block["slowest_top15"]:
            lines.append(
                f"| {c['id']} | L({c['n']},{c['k']},{c['j']},{c['s']}) | {c['elapsed_sec']} | {c['baseline_blocks']} | {c['solver_blocks']} | {c['gap_ratio']} | {c['family']} | {';'.join(c['reasons'])} |"
            )
        lines.append("")
        return lines

    lines: list[str] = []
    lines.append("# Split Analysis: n<16 vs 16<=n<18")
    lines.append("")
    lines.append(f"- generated_at: {split_payload['generated_at']}")
    lines.append(f"- source_json: `{split_payload['source_json']}`")
    lines.append("")
    lines.extend(render_block("Batch A: n<16", split_payload["batch_n_lt_16"]))
    lines.extend(render_block("Batch B: 16<=n<18", split_payload["batch_n_ge_16_lt_18"]))
    return "\n".join(lines) + "\n"


def _load_existing_cases(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    existing = {}
    for case in payload.get("cases", []):
        if isinstance(case, dict) and "id" in case:
            existing[str(case["id"])] = case
    return existing


def _case_sort_key(case: dict[str, Any]) -> tuple[int, int, int, int]:
    return (int(case["n"]), int(case["k"]), int(case["j"]), int(case["s"]))


def _main_eval(args: argparse.Namespace) -> int:
    baseline_payload = json.loads(Path(args.baseline_file).read_text(encoding="utf-8"))
    baseline_cases = list(baseline_payload.get("cases", []))
    selected = [
        c
        for c in baseline_cases
        if int(c["n"]) >= args.n_min and int(c["n"]) < args.n_max_exclusive
    ]
    selected.sort(key=_case_sort_key)
    if not selected:
        raise RuntimeError("No baseline cases selected by n-range")

    selected_ids = {str(c["id"]) for c in selected}
    existing_map: dict[str, dict[str, Any]] = {}
    if args.resume:
        existing_map = _load_existing_cases(Path(args.output_json))

    # Keep previously computed cases outside the current n-range so ranged runs
    # can accumulate into one final output file.
    output_cases_by_id: dict[str, dict[str, Any]] = {
        cid: case for cid, case in existing_map.items() if cid not in selected_ids
    }
    total = len(selected)
    started_all = time.time()
    workers = max(1, int(args.workers))
    completed_in_range = 0

    pending: list[tuple[int, dict[str, Any]]] = []
    for idx, case in enumerate(selected, start=1):
        cid = str(case["id"])
        if cid in existing_map:
            output_cases_by_id[cid] = existing_map[cid]
            completed_in_range += 1
            print(f"[{completed_in_range:03d}/{total}] {cid}  reused")
        else:
            pending.append((idx, case))

    def _save_checkpoint_snapshot() -> None:
        ordered_cases = sorted(output_cases_by_id.values(), key=_case_sort_key)
        checkpoint = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "config": {
                "n_min": int(args.n_min),
                "n_max_exclusive": int(args.n_max_exclusive),
                "timeout_sec": float(args.timeout_sec),
                "hard_timeout_sec": float(args.hard_timeout_sec),
                "num_attempts": int(args.num_attempts),
                "quality_tolerance_ratio": float(args.quality_tolerance_ratio),
                "judge_rule": "compliant iff runtime<=120s AND solver_blocks<=baseline*1.10 AND solver_verified",
                "ck_use_gpu": int(args.ck_use_gpu),
                "ck_skip_gpu_probe": bool(args.ck_skip_gpu_probe),
                "ck_n16_anchor_module": int(args.ck_n16_anchor_module),
                "ck_disable_cpsat": int(args.ck_disable_cpsat),
                "ck_solver_module": str(args.ck_solver_module),
                "ck_use_gpu_n16": int(args.ck_use_gpu_n16),
                "ck_skip_gpu_probe_n16": int(args.ck_skip_gpu_probe_n16),
                "ck_n16_anchor_module_n16": int(args.ck_n16_anchor_module_n16),
                "ck_disable_cpsat_n16": int(args.ck_disable_cpsat_n16),
                "ck_solver_module_n16": str(args.ck_solver_module_n16),
                "n16_owned_routing": True,
                "python_exe": args.python_exe,
                "workers": workers,
            },
            "baseline_file": str(args.baseline_file),
            "summary": _build_summary(ordered_cases),
            "cases": ordered_cases,
        }
        _save_json(Path(args.output_json), checkpoint)

    def _run_and_record(idx: int, case: dict[str, Any]) -> None:
        nonlocal completed_in_range
        cid = str(case["id"])
        n = int(case["n"])
        k = int(case["k"])
        j = int(case["j"])
        s = int(case["s"])
        seed = _case_seed(n, k, j, s)
        solver_config = _resolve_solver_dispatch_config(n=n, args=args)

        run_result = _run_one_case_subprocess(
            n=n,
            k=k,
            j=j,
            s=s,
            timeout_sec=float(args.timeout_sec),
            hard_timeout_sec=float(args.hard_timeout_sec),
            num_attempts=int(args.num_attempts),
            seed=seed,
            python_exe=args.python_exe,
            solver_config=solver_config,
        )
        evaluated = _evaluate_case(
            case=case,
            run_result=run_result,
            timeout_sec=float(args.timeout_sec),
            quality_tolerance_ratio=float(args.quality_tolerance_ratio),
        )
        output_cases_by_id[cid] = evaluated
        completed_in_range += 1
        print(
            (
                f"[{completed_in_range:03d}/{total}] {cid}  "
                f"status={evaluated['status']}  "
                f"profile={evaluated['solver_profile']}  "
                f"solver={evaluated['solver_blocks']}  "
                f"baseline={evaluated['baseline_blocks']}  "
                f"gap={evaluated['gap_ratio']}  "
                f"elapsed={evaluated['elapsed_sec']}s  "
                f"compliant={evaluated['compliant']}"
            )
        )
        _save_checkpoint_snapshot()

    if workers <= 1:
        for idx, case in pending:
            _run_and_record(idx, case)
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            future_to_meta = {}
            for idx, case in pending:
                n = int(case["n"])
                k = int(case["k"])
                j = int(case["j"])
                s = int(case["s"])
                solver_config = _resolve_solver_dispatch_config(n=n, args=args)
                future = pool.submit(
                    _run_one_case_subprocess,
                    n=n,
                    k=k,
                    j=j,
                    s=s,
                    timeout_sec=float(args.timeout_sec),
                    hard_timeout_sec=float(args.hard_timeout_sec),
                    num_attempts=int(args.num_attempts),
                    seed=_case_seed(n, k, j, s),
                    python_exe=args.python_exe,
                    solver_config=solver_config,
                )
                future_to_meta[future] = (idx, case, solver_config)
            for future in as_completed(future_to_meta):
                idx, case, solver_config = future_to_meta[future]
                cid = str(case["id"])
                try:
                    run_result = future.result()
                except Exception as exc:  # pragma: no cover - defensive path.
                    run_result = {
                        "status": "error",
                        "solver_blocks": None,
                        "elapsed_sec": float(args.hard_timeout_sec),
                        "first_legal_elapsed_sec": None,
                        "solver_verified": False,
                        "solver_module": solver_config.ck_solver_module,
                        "solver_profile": solver_config.profile_name,
                        "error": f"parallel-worker-exception: {exc}",
                    }
                evaluated = _evaluate_case(
                    case=case,
                    run_result=run_result,
                    timeout_sec=float(args.timeout_sec),
                    quality_tolerance_ratio=float(args.quality_tolerance_ratio),
                )
                output_cases_by_id[cid] = evaluated
                completed_in_range += 1
                print(
                    (
                        f"[{completed_in_range:03d}/{total}] {cid}  "
                        f"status={evaluated['status']}  "
                        f"profile={evaluated['solver_profile']}  "
                        f"solver={evaluated['solver_blocks']}  "
                        f"baseline={evaluated['baseline_blocks']}  "
                        f"gap={evaluated['gap_ratio']}  "
                        f"elapsed={evaluated['elapsed_sec']}s  "
                        f"compliant={evaluated['compliant']}"
                    )
                )
                _save_checkpoint_snapshot()

    output_cases = sorted(output_cases_by_id.values(), key=_case_sort_key)
    summary = _build_summary(output_cases)
    by_n = _by_n_summary(output_cases)
    reason_counter = Counter()
    for c in output_cases:
        reason_counter.update(c["non_compliant_reasons"])

    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "config": {
            "n_min": int(args.n_min),
            "n_max_exclusive": int(args.n_max_exclusive),
            "timeout_sec": float(args.timeout_sec),
            "hard_timeout_sec": float(args.hard_timeout_sec),
            "num_attempts": int(args.num_attempts),
            "quality_tolerance_ratio": float(args.quality_tolerance_ratio),
            "judge_rule": "compliant iff runtime<=120s AND solver_blocks<=baseline*1.10 AND solver_verified",
            "ck_use_gpu": int(args.ck_use_gpu),
            "ck_skip_gpu_probe": bool(args.ck_skip_gpu_probe),
            "ck_n16_anchor_module": int(args.ck_n16_anchor_module),
            "ck_disable_cpsat": int(args.ck_disable_cpsat),
            "ck_solver_module": str(args.ck_solver_module),
            "ck_use_gpu_n16": int(args.ck_use_gpu_n16),
            "ck_skip_gpu_probe_n16": int(args.ck_skip_gpu_probe_n16),
            "ck_n16_anchor_module_n16": int(args.ck_n16_anchor_module_n16),
            "ck_disable_cpsat_n16": int(args.ck_disable_cpsat_n16),
            "ck_solver_module_n16": str(args.ck_solver_module_n16),
            "n16_owned_routing": True,
            "python_exe": args.python_exe,
            "workers": workers,
        },
        "baseline_file": str(args.baseline_file),
        "summary": summary,
        "reason_counter": dict(reason_counter),
        "by_n": by_n,
        "elapsed_total_wall_sec": _fmt_float(time.time() - started_all),
        "cases": output_cases,
    }
    _save_json(Path(args.output_json), payload)

    md_text = _render_main_markdown(payload)
    Path(args.output_md).write_text(md_text, encoding="utf-8")

    split_a = [c for c in output_cases if int(c["n"]) < 16]
    split_b = [c for c in output_cases if 16 <= int(c["n"]) < 18]
    split_payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_json": str(args.output_json),
        "batch_n_lt_16": _batch_analysis(split_a, "n<16"),
        "batch_n_ge_16_lt_18": _batch_analysis(split_b, "16<=n<18"),
    }
    _save_json(Path(args.output_json).with_name(Path(args.output_json).stem + ".split.json"), split_payload)
    Path(args.split_md).write_text(_render_split_markdown(split_payload), encoding="utf-8")

    print("")
    print("Done.")
    print(f"JSON: {args.output_json}")
    print(f"Summary MD: {args.output_md}")
    print(f"Split MD: {args.split_md}")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rerun n<18 baseline compliance with timeout and quality thresholds."
    )
    parser.add_argument("--run-one", action="store_true", help="Internal mode: run one case and print JSON.")
    parser.add_argument("--n", type=int, default=None)
    parser.add_argument("--k", type=int, default=None)
    parser.add_argument("--j", type=int, default=None)
    parser.add_argument("--s", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--baseline-file", default=str(DEFAULT_BASELINE))
    parser.add_argument("--n-min", type=int, default=7)
    parser.add_argument("--n-max-exclusive", type=int, default=18)
    parser.add_argument("--timeout-sec", type=float, default=120.0)
    parser.add_argument("--hard-timeout-sec", type=float, default=125.0)
    parser.add_argument("--num-attempts", type=int, default=3)
    parser.add_argument("--quality-tolerance-ratio", type=float, default=0.1)
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--split-md", default=str(DEFAULT_SPLIT_MD))
    parser.add_argument("--resume", action="store_true", help="Reuse completed cases from output JSON if present.")
    parser.add_argument("--python-exe", default=_default_python_exe())
    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Number of cases to run in parallel (default: 2).",
    )
    parser.add_argument("--ck-use-gpu", type=int, default=1)
    parser.add_argument("--ck-n16-anchor-module", type=int, default=0)
    parser.add_argument("--ck-disable-cpsat", type=int, default=0)
    parser.add_argument(
        "--ck-solver-module",
        default="solver",
        help="Solver module name to import CoveringDesignSolver from (default: solver).",
    )
    parser.add_argument("--ck-use-gpu-n16", type=int, default=1)
    parser.add_argument("--ck-n16-anchor-module-n16", type=int, default=1)
    parser.add_argument("--ck-disable-cpsat-n16", type=int, default=1)
    parser.add_argument(
        "--ck-solver-module-n16",
        default="solver_n16_isolated",
        help="Dedicated solver module for n==16 routing (default: solver_n16_isolated).",
    )
    parser.add_argument(
        "--ck-skip-gpu-probe",
        action="store_true",
        help="Set CK_SKIP_GPU_PROBE=1 for child solver process.",
    )
    parser.add_argument(
        "--ck-skip-gpu-probe-n16",
        type=int,
        choices=[0, 1],
        default=0,
        help="Dedicated CK_SKIP_GPU_PROBE value for n==16 routing.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.run_one:
        required = [args.n, args.k, args.j, args.s]
        if any(v is None for v in required):
            raise SystemExit("--run-one requires --n --k --j --s")
        solver_config = _resolve_solver_dispatch_config(n=int(args.n), args=args)
        os.environ["CK_USE_GPU"] = str(int(bool(solver_config.ck_use_gpu)))
        if solver_config.ck_skip_gpu_probe:
            os.environ["CK_SKIP_GPU_PROBE"] = "1"
        else:
            os.environ.pop("CK_SKIP_GPU_PROBE", None)
        os.environ["CK_N16_ANCHOR_MODULE"] = str(int(bool(solver_config.ck_n16_anchor_module)))
        os.environ["CK_DISABLE_CPSAT"] = str(int(bool(solver_config.ck_disable_cpsat)))
        os.environ["CK_SOLVER_MODULE"] = str(solver_config.ck_solver_module)
        os.environ["CK_SOLVER_PROFILE"] = str(solver_config.profile_name)
        seed = args.seed if args.seed is not None else _case_seed(args.n, args.k, args.j, args.s)
        result = _run_one_case_locally(
            n=int(args.n),
            k=int(args.k),
            j=int(args.j),
            s=int(args.s),
            timeout_sec=float(args.timeout_sec),
            num_attempts=int(args.num_attempts),
            seed=int(seed),
        )
        print(json.dumps(result, ensure_ascii=False))
        return 0
    return _main_eval(args)


if __name__ == "__main__":
    raise SystemExit(main())
