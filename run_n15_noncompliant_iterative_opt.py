from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from n15_cluster_case_module import get_n15_case_spec, method_hint_from_coveringrepo


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def _band(gap_ratio: float | None) -> str:
    if gap_ratio is None:
        return "unknown"
    if gap_ratio > 0.18:
        return "severe"
    if gap_ratio > 0.12:
        return "medium"
    if gap_ratio > 0.10:
        return "edge"
    return "compliant"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _non_compliant_cases(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [c for c in payload.get("cases", []) if not bool(c.get("compliant", False))]


def _write_baseline_from_cases(cases: list[dict[str, Any]], out_path: Path, *, source: str) -> None:
    out_cases: list[dict[str, Any]] = []
    for case in cases:
        n = int(case["n"])
        k = int(case["k"])
        j = int(case["j"])
        s = int(case["s"])
        spec = get_n15_case_spec(n, k, j, s)
        source_page = case.get("source_page")
        if spec is not None:
            source_page = source_page or spec.source_page
        out_cases.append(
            {
                "id": str(case["id"]),
                "n": n,
                "k": k,
                "j": j,
                "s": s,
                "baseline_blocks": int(case["baseline_blocks"]),
                "source_page": source_page,
            }
        )
    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "case_count": len(out_cases),
        "cases": out_cases,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _cluster_summary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    cluster_count: dict[str, int] = defaultdict(int)
    family_count: dict[str, int] = defaultdict(int)
    method_hints: dict[str, set[str]] = defaultdict(set)
    for case in cases:
        family = str(case.get("family") or "unknown")
        gap = case.get("gap_ratio")
        gap_ratio = float(gap) if gap is not None else None
        band = _band(gap_ratio)
        cluster_key = f"{family}__{band}"
        cluster_count[cluster_key] += 1
        family_count[family] += 1
        spec = get_n15_case_spec(int(case["n"]), int(case["k"]), int(case["j"]), int(case["s"]))
        if spec is not None:
            method_hints[family].add(method_hint_from_coveringrepo(spec))
    return {
        "cluster_count": dict(sorted(cluster_count.items(), key=lambda kv: kv[0])),
        "family_count": dict(sorted(family_count.items(), key=lambda kv: kv[0])),
        "method_hints": {k: sorted(v) for k, v in sorted(method_hints.items(), key=lambda kv: kv[0])},
    }


def _render_cluster_md(*, title: str, cases: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"- 样本数: {len(cases)}")
    lines.append("")
    if not cases:
        lines.append("当前无不合规样本。")
        return "\n".join(lines) + "\n"

    cluster_info = _cluster_summary(cases)
    lines.append("## 聚类统计")
    lines.append("")
    lines.append("| cluster | count |")
    lines.append("| --- | ---: |")
    for k, v in cluster_info["cluster_count"].items():
        lines.append(f"| {k} | {v} |")

    lines.append("")
    lines.append("## 分族策略（借鉴 coveringrepository 公开方法）")
    lines.append("")
    for fam, cnt in cluster_info["family_count"].items():
        lines.append(f"- `{fam}`: {cnt} 例")
        for hint in cluster_info["method_hints"].get(fam, []):
            lines.append(f"  - 方法线索: {hint}")

    lines.append("")
    lines.append("## 样本明细")
    lines.append("")
    lines.append("| id | params | family | baseline | solver | gap | cluster |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: | --- |")
    for c in sorted(cases, key=lambda x: (int(x["n"]), int(x["k"]), int(x["j"]), int(x["s"]))):
        gap = float(c["gap_ratio"]) if c.get("gap_ratio") is not None else None
        lines.append(
            f"| {c['id']} | L({c['n']},{c['k']},{c['j']},{c['s']}) | "
            f"{c.get('family')} | {c['baseline_blocks']} | {c.get('solver_blocks')} | "
            f"{c.get('gap_ratio')} | {c.get('family')}__{_band(gap)} |"
        )
    return "\n".join(lines) + "\n"


def _run_eval(
    *,
    baseline_file: Path,
    output_json: Path,
    output_md: Path,
    output_split_md: Path,
    profile: str,
    timeout_sec: float,
    num_attempts: int,
    workers: int,
    ck_use_gpu: int,
) -> None:
    baseline_payload = _load_json(baseline_file)
    cases = baseline_payload.get("cases", [])
    if not cases:
        raise RuntimeError("baseline cases is empty")
    n_min = min(int(c["n"]) for c in cases)
    n_max_exclusive = max(int(c["n"]) for c in cases) + 1

    cmd = [
        sys.executable,
        str(ROOT / "evaluate_n_lt_18_compliance.py"),
        "--baseline-file",
        str(baseline_file),
        "--n-min",
        str(n_min),
        "--n-max-exclusive",
        str(n_max_exclusive),
        "--timeout-sec",
        str(float(timeout_sec)),
        "--hard-timeout-sec",
        str(float(timeout_sec) + 10.0),
        "--num-attempts",
        str(int(num_attempts)),
        "--workers",
        str(int(workers)),
        "--ck-use-gpu",
        str(int(ck_use_gpu)),
        "--ck-solver-module",
        "solver_n15_cluster_isolated",
        "--output-json",
        str(output_json),
        "--output-md",
        str(output_md),
        "--split-md",
        str(output_split_md),
        "--ck-skip-gpu-probe",
    ]
    env = os.environ.copy()
    env["CK_N15_CLUSTER_PROFILE"] = profile
    env["CK_N15_HARDCASE_MODULE"] = "0"
    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
        env=env,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "evaluate failed\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    print(completed.stdout)


def _pick_best_case_rows(iter_payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best_map: dict[str, dict[str, Any]] = {}
    for payload in iter_payloads:
        for c in payload.get("cases", []):
            cid = str(c["id"])
            if cid not in best_map:
                best_map[cid] = c
                continue
            cur_best = best_map[cid]
            cur_blocks = int(cur_best.get("solver_blocks") or 10**9)
            new_blocks = int(c.get("solver_blocks") or 10**9)
            if new_blocks < cur_blocks:
                best_map[cid] = c
    return [best_map[k] for k in sorted(best_map.keys())]


def _render_summary_md(
    *,
    source_json: Path,
    iteration_rows: list[dict[str, Any]],
    best_cases: list[dict[str, Any]],
) -> str:
    lines: list[str] = []
    lines.append("# n<=15 不合规簇自动迭代优化报告")
    lines.append("")
    lines.append(f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 输入结果: `{source_json}`")
    lines.append("")
    lines.append("## 迭代结果")
    lines.append("")
    lines.append("| iter | profile | total | compliant | non_compliant | avg_gap_non_compliant | output_json |")
    lines.append("| ---: | --- | ---: | ---: | ---: | ---: | --- |")
    for row in iteration_rows:
        lines.append(
            f"| {row['iter']} | {row['profile']} | {row['total']} | {row['compliant']} | "
            f"{row['non_compliant']} | {row['avg_gap_non_compliant']} | `{row['output_json']}` |"
        )

    lines.append("")
    lines.append("## 逐样本最佳（跨迭代取最优）")
    lines.append("")
    lines.append("| id | params | baseline | best_solver | gap | compliant | profile |")
    lines.append("| --- | --- | ---: | ---: | ---: | --- | --- |")
    for c in sorted(best_cases, key=lambda x: (int(x["n"]), int(x["k"]), int(x["j"]), int(x["s"]))):
        lines.append(
            f"| {c['id']} | L({c['n']},{c['k']},{c['j']},{c['s']}) | {c['baseline_blocks']} | "
            f"{c.get('solver_blocks')} | {c.get('gap_ratio')} | {c.get('compliant')} | {c.get('solver_profile')} |"
        )
    return "\n".join(lines) + "\n"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="n<=15 非合规样本聚类专题优化与自动迭代")
    parser.add_argument(
        "--source-json",
        default=str(RESULTS / "n_le_15_noncompliant15_after_special_v5_w1.json"),
        help="输入结果文件（从中提取当前不合规样本）",
    )
    parser.add_argument("--max-iters", type=int, default=2)
    parser.add_argument(
        "--profiles",
        default="balanced,exact_first",
        help="迭代 profile 列表，逗号分隔",
    )
    parser.add_argument("--timeout-sec", type=float, default=120.0)
    parser.add_argument("--num-attempts", type=int, default=3)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--ck-use-gpu", type=int, default=1)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    source_json = Path(args.source_json).resolve()
    source_payload = _load_json(source_json)
    current_non_compliant = _non_compliant_cases(source_payload)
    if not current_non_compliant:
        print("输入结果中没有不合规样本，无需迭代。")
        return 0

    profiles = [p.strip() for p in str(args.profiles).split(",") if p.strip()]
    if not profiles:
        profiles = ["balanced"]
    max_iters = max(1, int(args.max_iters))
    profiles = profiles[:max_iters]

    iter_rows: list[dict[str, Any]] = []
    iter_payloads: list[dict[str, Any]] = []

    initial_cluster_md = RESULTS / "n15_cluster_iter0_analysis.md"
    initial_cluster_md.write_text(
        _render_cluster_md(
            title="Iter0 输入不合规聚类分析",
            cases=current_non_compliant,
        ),
        encoding="utf-8",
    )

    for idx, profile in enumerate(profiles, start=1):
        baseline_file = RESULTS / f"n15_iter{idx}_baseline_from_remaining.json"
        _write_baseline_from_cases(
            current_non_compliant,
            baseline_file,
            source=f"iter{idx}-remaining-from-{source_json.name}",
        )
        out_json = RESULTS / f"n15_iter{idx}_cluster_solver_{profile}.json"
        out_md = RESULTS / f"n15_iter{idx}_cluster_solver_{profile}.md"
        out_split_md = RESULTS / f"n15_iter{idx}_cluster_solver_{profile}_split.md"

        print(
            f"[iter{idx}] profile={profile} "
            f"cases={len(current_non_compliant)} "
            f"baseline={baseline_file.name}"
        )
        _run_eval(
            baseline_file=baseline_file,
            output_json=out_json,
            output_md=out_md,
            output_split_md=out_split_md,
            profile=profile,
            timeout_sec=float(args.timeout_sec),
            num_attempts=int(args.num_attempts),
            workers=int(args.workers),
            ck_use_gpu=int(args.ck_use_gpu),
        )
        payload = _load_json(out_json)
        iter_payloads.append(payload)
        cases = list(payload.get("cases", []))
        remain = _non_compliant_cases(payload)
        non_gaps = [float(c["gap_ratio"]) for c in remain if c.get("gap_ratio") is not None]
        avg_gap_non = round(sum(non_gaps) / len(non_gaps), 6) if non_gaps else 0.0
        iter_rows.append(
            {
                "iter": idx,
                "profile": profile,
                "total": len(cases),
                "compliant": sum(1 for c in cases if bool(c.get("compliant", False))),
                "non_compliant": len(remain),
                "avg_gap_non_compliant": avg_gap_non,
                "output_json": out_json.name,
            }
        )

        cluster_md = RESULTS / f"n15_iter{idx}_cluster_analysis.md"
        cluster_md.write_text(
            _render_cluster_md(
                title=f"Iter{idx} 输出不合规聚类分析（profile={profile}）",
                cases=remain,
            ),
            encoding="utf-8",
        )

        current_non_compliant = remain
        if not current_non_compliant:
            break

    best_cases = _pick_best_case_rows(iter_payloads)
    summary_md = RESULTS / "n15_cluster_iterative_summary.md"
    summary_md.write_text(
        _render_summary_md(
            source_json=source_json,
            iteration_rows=iter_rows,
            best_cases=best_cases,
        ),
        encoding="utf-8",
    )

    best_json = RESULTS / "n15_cluster_best_of_iterations.json"
    best_json.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_json": str(source_json),
                "iterations": iter_rows,
                "best_cases": best_cases,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("")
    print(f"iter summary: {summary_md}")
    print(f"best cases : {best_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

