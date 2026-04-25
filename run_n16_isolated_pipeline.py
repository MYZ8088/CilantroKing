from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EVAL_SCRIPT = ROOT / "evaluate_n_lt_18_compliance.py"
RESULTS_DIR = ROOT / "results"

DEFAULT_BASELINE = RESULTS_DIR / "coveringrepo_n_lt_26_baselines.json"
DEFAULT_OUTPUT_JSON = RESULTS_DIR / "n_eq_16_isolated_pipeline.json"
DEFAULT_OUTPUT_MD = RESULTS_DIR / "n_eq_16_isolated_pipeline.md"
DEFAULT_SPLIT_MD = RESULTS_DIR / "n_eq_16_isolated_pipeline_split.md"


def _default_python_exe() -> str:
    if os.name == "nt":
        venv_python = ROOT / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run n=16 isolated pipeline with dedicated solver module."
    )
    parser.add_argument("--baseline-file", default=str(DEFAULT_BASELINE))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--split-md", default=str(DEFAULT_SPLIT_MD))
    parser.add_argument("--n-min", type=int, default=16)
    parser.add_argument("--n-max-exclusive", type=int, default=17)
    parser.add_argument("--timeout-sec", type=float, default=120.0)
    parser.add_argument("--hard-timeout-sec", type=float, default=125.0)
    parser.add_argument("--num-attempts", type=int, default=3)
    parser.add_argument("--quality-tolerance-ratio", type=float, default=0.1)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--python-exe", default=_default_python_exe())
    parser.add_argument("--solver-module", default="solver_n16_isolated")
    parser.add_argument("--ck-use-gpu", type=int, default=1)
    parser.add_argument("--ck-n16-anchor-module", type=int, default=1)
    parser.add_argument("--ck-disable-cpsat", type=int, default=1)
    parser.add_argument("--ck-skip-gpu-probe", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def _build_cmd(args: argparse.Namespace) -> list[str]:
    cmd = [
        args.python_exe,
        str(EVAL_SCRIPT),
        "--baseline-file",
        str(args.baseline_file),
        "--n-min",
        str(args.n_min),
        "--n-max-exclusive",
        str(args.n_max_exclusive),
        "--timeout-sec",
        str(args.timeout_sec),
        "--hard-timeout-sec",
        str(args.hard_timeout_sec),
        "--num-attempts",
        str(args.num_attempts),
        "--quality-tolerance-ratio",
        str(args.quality_tolerance_ratio),
        "--workers",
        str(args.workers),
        "--python-exe",
        str(args.python_exe),
        "--ck-use-gpu-n16",
        str(args.ck_use_gpu),
        "--ck-n16-anchor-module-n16",
        str(args.ck_n16_anchor_module),
        "--ck-disable-cpsat-n16",
        str(args.ck_disable_cpsat),
        "--ck-solver-module-n16",
        str(args.solver_module),
        "--output-json",
        str(args.output_json),
        "--output-md",
        str(args.output_md),
        "--split-md",
        str(args.split_md),
    ]
    if args.ck_skip_gpu_probe:
        cmd.extend(["--ck-skip-gpu-probe-n16", "1"])
    if args.resume:
        cmd.append("--resume")
    return cmd


def main() -> int:
    args = _parse_args()
    cmd = _build_cmd(args)
    print("Running n=16 isolated pipeline:")
    print(" ".join(cmd))
    if args.dry_run:
        return 0
    completed = subprocess.run(cmd, cwd=ROOT)
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
