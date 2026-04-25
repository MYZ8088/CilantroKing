import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import evaluate_n_lt_18_compliance as eval_script


def _build_args(**overrides):
    base = {
        "ck_use_gpu": 0,
        "ck_skip_gpu_probe": True,
        "ck_n16_anchor_module": 0,
        "ck_disable_cpsat": 0,
        "ck_solver_module": "solver",
        "ck_use_gpu_n16": 1,
        "ck_skip_gpu_probe_n16": 1,
        "ck_n16_anchor_module_n16": 1,
        "ck_disable_cpsat_n16": 1,
        "ck_solver_module_n16": "solver_n16_isolated",
    }
    base.update(overrides)
    return argparse.Namespace(**base)


def test_resolve_solver_dispatch_config_non_16_uses_default_profile():
    args = _build_args()
    cfg = eval_script._resolve_solver_dispatch_config(n=15, args=args)
    assert cfg.profile_name == "default"
    assert cfg.ck_use_gpu == 0
    assert cfg.ck_skip_gpu_probe is True
    assert cfg.ck_n16_anchor_module == 0
    assert cfg.ck_disable_cpsat == 0
    assert cfg.ck_solver_module == "solver"


def test_resolve_solver_dispatch_config_n16_uses_isolated_profile():
    args = _build_args(
        ck_use_gpu=0,
        ck_skip_gpu_probe=False,
        ck_n16_anchor_module=0,
        ck_disable_cpsat=0,
        ck_solver_module="solver",
        ck_use_gpu_n16=1,
        ck_skip_gpu_probe_n16=1,
        ck_n16_anchor_module_n16=1,
        ck_disable_cpsat_n16=1,
        ck_solver_module_n16="solver_n16_isolated",
    )
    cfg = eval_script._resolve_solver_dispatch_config(n=16, args=args)
    assert cfg.profile_name == "n16_isolated"
    assert cfg.ck_use_gpu == 1
    assert cfg.ck_skip_gpu_probe is True
    assert cfg.ck_n16_anchor_module == 1
    assert cfg.ck_disable_cpsat == 1
    assert cfg.ck_solver_module == "solver_n16_isolated"


def test_run_one_case_subprocess_injects_solver_profile(monkeypatch):
    captured = {}

    class _Completed:
        returncode = 0
        stdout = json.dumps(
            {
                "status": "ok",
                "solver_blocks": 3,
                "elapsed_sec": 0.12,
                "first_legal_elapsed_sec": 0.08,
                "solver_verified": True,
            }
        )
        stderr = ""

    def _fake_run(cmd, cwd, capture_output, text, timeout, env):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        captured["env"] = env
        return _Completed()

    monkeypatch.setattr(eval_script.subprocess, "run", _fake_run)

    cfg = eval_script.SolverDispatchConfig(
        profile_name="n16_isolated",
        ck_use_gpu=1,
        ck_skip_gpu_probe=True,
        ck_n16_anchor_module=1,
        ck_disable_cpsat=1,
        ck_solver_module="solver_n16_isolated",
    )
    result = eval_script._run_one_case_subprocess(
        n=16,
        k=6,
        j=5,
        s=5,
        timeout_sec=1.0,
        hard_timeout_sec=2.0,
        num_attempts=1,
        seed=42,
        python_exe=sys.executable,
        solver_config=cfg,
    )

    assert captured["cwd"] == eval_script.ROOT
    assert captured["env"]["CK_SOLVER_MODULE"] == "solver_n16_isolated"
    assert captured["env"]["CK_SOLVER_PROFILE"] == "n16_isolated"
    assert captured["env"]["CK_USE_GPU"] == "1"
    assert captured["env"]["CK_SKIP_GPU_PROBE"] == "1"
    assert captured["env"]["CK_N16_ANCHOR_MODULE"] == "1"
    assert captured["env"]["CK_DISABLE_CPSAT"] == "1"
    assert result["solver_module"] == "solver_n16_isolated"
    assert result["solver_profile"] == "n16_isolated"
