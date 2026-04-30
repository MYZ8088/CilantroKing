"""Covering design solver for the Optimal Samples Selection System.

Solves L(n, k, j, s): find minimum k-subsets of {0,...,n-1} such that
every j-subset shares at least s elements with at least one selected k-subset.

Optimisations:
  - Precomputed coverage table: for each candidate, which targets it covers
  - Incremental scoring: after choosing a group, only update affected candidates
  - Containment fast-path: O(C(k,j)) lookup table when s==j
  - Simulated annealing post-processing for medium-size solutions
  - Adaptive top-K heuristic for very large problems
  - Optional GPU batch scoring (CuPy) with automatic CPU fallback
"""

from __future__ import annotations

import json
import math
import os
import random
import site
import subprocess
import sys
import time
from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Callable

import numpy as np

from n_algorithms.shared.bounds import get_bounds
from n_algorithms.shared.identity_cover_module import build_identity_cover

# Import specialized modules for n17, n18
try:
    from n_algorithms.n17.specialized_module import (
        is_n17_special_case,
        run_n17_specialized_module,
        classify_n17_special_case,
        get_n17_case_spec,
        make_n17_case_key,
        should_short_circuit_n17_tiny_legal_solution,
    )
except ImportError:
    is_n17_special_case = None  # type: ignore
    run_n17_specialized_module = None  # type: ignore
    classify_n17_special_case = None  # type: ignore
    get_n17_case_spec = None  # type: ignore
    make_n17_case_key = None  # type: ignore
    should_short_circuit_n17_tiny_legal_solution = None  # type: ignore

try:
    from n_algorithms.n18.specialized_module import is_n18_special_case, run_n18_specialized_module
except ImportError:
    is_n18_special_case = None  # type: ignore
    run_n18_specialized_module = None  # type: ignore


@lru_cache(maxsize=1)
def _n_le_15_baseline_index() -> dict[tuple[int, int, int, int], int]:
    root = Path(__file__).resolve().parent
    candidates = [
        root / "coveringrepo_n_lt_26_baselines(1).json",
        root / "results" / "coveringrepo_n_lt_26_baselines.json",
        root / "results" / "n_le_15_all_legal_baselines_filled_v1.json",
    ]
    payload = None
    for path in candidates:
        if not path.exists():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            break
        except Exception:
            continue
    if payload is None:
        return {}
    cases = payload.get("cases")
    if not isinstance(cases, list):
        return {}
    index: dict[tuple[int, int, int, int], int] = {}
    for case in cases:
        if not isinstance(case, dict):
            continue
        try:
            key = (
                int(case["n"]),
                int(case["k"]),
                int(case["j"]),
                int(case["s"]),
            )
            index[key] = int(case["baseline_blocks"])
        except Exception:
            continue
    return index


def _add_windows_cuda_dll_dirs() -> None:
    """Make CuPy find CUDA DLLs from pip nvidia-* packages on Windows."""
    if os.name != "nt":
        return

    roots: list[Path] = []
    try:
        roots.extend(Path(p) for p in site.getsitepackages())
    except Exception:
        pass
    try:
        roots.append(Path(site.getusersitepackages()))
    except Exception:
        pass

    added: set[str] = set()
    for root in roots:
        nvidia_dir = root / "nvidia"
        if not nvidia_dir.exists():
            continue
        runtime_root = nvidia_dir / "cuda_runtime"
        if "CUDA_PATH" not in os.environ and runtime_root.exists():
            os.environ["CUDA_PATH"] = str(runtime_root)
        for pkg in ("cuda_nvrtc", "cuda_runtime", "nvjitlink"):
            bin_dir = nvidia_dir / pkg / "bin"
            if not bin_dir.exists():
                continue
            s = str(bin_dir)
            if s in added:
                continue
            try:
                os.add_dll_directory(s)  # type: ignore[attr-defined]
            except Exception:
                pass
            os.environ["PATH"] = s + os.pathsep + os.environ.get("PATH", "")
            added.add(s)


_add_windows_cuda_dll_dirs()

try:
    import cupy as cp  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cp = None

try:
    from ortools.sat.python import cp_model  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cp_model = None
if cp_model is not None and os.environ.get("CK_DISABLE_CPSAT") == "1":
    cp_model = None


_GPU_BATCH_PROBE_OK: bool | None = None
_GPU_BATCH_PROBE_AT: float | None = None
_GPU_BATCH_PROBE_RETRY_SEC = 30.0


# ---------------------------------------------------------------------------
# Bitmask utilities
# ---------------------------------------------------------------------------

def popcount_uint32(arr: np.ndarray) -> np.ndarray:
    """Vectorised Hamming-weight (popcount) for uint32 numpy arrays."""
    x = np.array(arr, dtype=np.uint32, copy=True)
    t = (x >> np.uint32(1)) & np.uint32(0x55555555)
    np.subtract(x, t, out=x)
    del t
    t = x & np.uint32(0x33333333)
    np.right_shift(x, np.uint32(2), out=x)
    x &= np.uint32(0x33333333)
    np.add(x, t, out=x)
    del t
    t = x >> np.uint32(4)
    np.add(x, t, out=x)
    del t
    x &= np.uint32(0x0F0F0F0F)
    np.multiply(x, np.uint32(0x01010101), out=x)
    np.right_shift(x, np.uint32(24), out=x)
    return x.astype(np.int32)


def _gpu_chunk_for_batch(num_cands: int, num_targets: int) -> int:
    assert cp is not None
    free_mem, _ = cp.cuda.Device().mem_info
    approx_bytes_per_target = max(4, num_cands * 12)
    chunk = int(max(
        2048,
        min(num_targets, (free_mem * 0.3) // approx_bytes_per_target),
    ))
    return max(1, chunk)


def _gpu_batch_scores_inline(
    cands: np.ndarray,
    targets: np.ndarray,
    *,
    containment: bool,
    s: int,
    cancel_fn: Callable[[], bool],
) -> np.ndarray:
    assert cp is not None
    cands_gpu = cp.asarray(cands, dtype=cp.uint32)
    targets_gpu = cp.asarray(targets, dtype=cp.uint32)
    scores_gpu = cp.zeros(len(cands), dtype=cp.int32)
    chunk = _gpu_chunk_for_batch(len(cands), len(targets))

    for start in range(0, len(targets), chunk):
        if cancel_fn():
            break
        t_chunk = targets_gpu[start : start + chunk]
        ints = cands_gpu[:, None] & t_chunk[None, :]
        if containment:
            hits = ints == t_chunk[None, :]
        else:
            x = cp.array(ints, dtype=cp.uint32, copy=True)
            t = (x >> cp.uint32(1)) & cp.uint32(0x55555555)
            x = x - t
            t = x & cp.uint32(0x33333333)
            x = (x >> cp.uint32(2)) & cp.uint32(0x33333333)
            x = x + t
            x = x + (x >> cp.uint32(4))
            x = x & cp.uint32(0x0F0F0F0F)
            x = x * cp.uint32(0x01010101)
            x = x >> cp.uint32(24)
            hits = x.astype(cp.int32) >= s
        scores_gpu += cp.sum(hits, axis=1, dtype=cp.int32)
    return cp.asnumpy(scores_gpu)


def _gpu_batch_best_inline(
    cands: np.ndarray,
    targets: np.ndarray,
    *,
    containment: bool,
    s: int,
    cancel_fn: Callable[[], bool],
) -> tuple[int, int]:
    assert cp is not None
    cands_gpu = cp.asarray(cands, dtype=cp.uint32)
    targets_gpu = cp.asarray(targets, dtype=cp.uint32)
    scores_gpu = cp.zeros(len(cands), dtype=cp.int32)
    chunk = _gpu_chunk_for_batch(len(cands), len(targets))

    for start in range(0, len(targets), chunk):
        if cancel_fn():
            break
        t_chunk = targets_gpu[start : start + chunk]
        ints = cands_gpu[:, None] & t_chunk[None, :]
        if containment:
            hits = ints == t_chunk[None, :]
        else:
            x = cp.array(ints, dtype=cp.uint32, copy=True)
            t = (x >> cp.uint32(1)) & cp.uint32(0x55555555)
            x = x - t
            t = x & cp.uint32(0x33333333)
            x = (x >> cp.uint32(2)) & cp.uint32(0x33333333)
            x = x + t
            x = x + (x >> cp.uint32(4))
            x = x & cp.uint32(0x0F0F0F0F)
            x = x * cp.uint32(0x01010101)
            x = x >> cp.uint32(24)
            hits = x.astype(cp.int32) >= s
        scores_gpu += cp.sum(hits, axis=1, dtype=cp.int32)

    best_local = int(cp.argmax(scores_gpu).get())
    best_count = int(scores_gpu[best_local].get())
    return best_local, best_count


def mask_to_elements(mask: int) -> list[int]:
    """Bitmask -> sorted list of 0-based element indices."""
    elems: list[int] = []
    i = 0
    while mask:
        if mask & 1:
            elems.append(i)
        mask >>= 1
        i += 1
    return elems


def elements_to_mask(elements) -> int:
    mask = 0
    for e in elements:
        mask |= 1 << e
    return mask


def _extract_bits(mask: int) -> list[int]:
    """Return individual bit-positions as power-of-2 values."""
    bits: list[int] = []
    while mask:
        b = mask & (-mask)
        bits.append(b)
        mask &= mask - 1
    return bits


def _probe_gpu_batch_path() -> bool:
    """Run a one-time subprocess probe before enabling the large-batch GPU path."""
    global _GPU_BATCH_PROBE_OK, _GPU_BATCH_PROBE_AT
    now = time.time()
    if _GPU_BATCH_PROBE_OK is True:
        return _GPU_BATCH_PROBE_OK
    if (
        _GPU_BATCH_PROBE_OK is False
        and _GPU_BATCH_PROBE_AT is not None
        and (now - _GPU_BATCH_PROBE_AT) < _GPU_BATCH_PROBE_RETRY_SEC
    ):
        return False
    if cp is None:
        _GPU_BATCH_PROBE_OK = False
        _GPU_BATCH_PROBE_AT = now
        return False
    if os.environ.get("CK_SKIP_GPU_PROBE") == "1":
        _GPU_BATCH_PROBE_OK = True
        _GPU_BATCH_PROBE_AT = now
        return True

    probe_script = r"""
import os
import numpy as np
from n_algorithms.shared.solver_core import _add_windows_cuda_dll_dirs
_add_windows_cuda_dll_dirs()
import cupy as cp

cands = np.arange(1024, dtype=np.uint32)
targets = np.arange(24576, dtype=np.uint32)
cands_gpu = cp.asarray(cands, dtype=cp.uint32)
targets_gpu = cp.asarray(targets, dtype=cp.uint32)
ints = cands_gpu[:, None] & targets_gpu[None, :]
x = cp.array(ints, dtype=cp.uint32, copy=True)
t = (x >> cp.uint32(1)) & cp.uint32(0x55555555)
x = x - t
t = x & cp.uint32(0x33333333)
x = (x >> cp.uint32(2)) & cp.uint32(0x33333333)
x = x + t
x = x + (x >> cp.uint32(4))
x = x & cp.uint32(0x0F0F0F0F)
x = x * cp.uint32(0x01010101)
x = x >> cp.uint32(24)
hits = x.astype(cp.int32) >= 1
scores = cp.sum(hits, axis=1, dtype=cp.int32)
cp.argmax(scores).get()
print("gpu-probe-ok")
"""
    env = os.environ.copy()
    env["CK_SKIP_GPU_PROBE"] = "1"
    try:
        completed = subprocess.run(
            [sys.executable, "-u", "-c", probe_script],
            capture_output=True,
            text=True,
            timeout=12,
            env=env,
        )
        _GPU_BATCH_PROBE_OK = (
            completed.returncode == 0
            and "gpu-probe-ok" in completed.stdout
        )
    except Exception:
        _GPU_BATCH_PROBE_OK = False
    _GPU_BATCH_PROBE_AT = now
    return _GPU_BATCH_PROBE_OK


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SolverProgress:
    phase: str = ""
    message: str = ""
    iteration: int = 0
    solution_size: int = 0
    remaining: int = 0
    total: int = 0
    elapsed: float = 0.0


@dataclass
class SolverResult:
    groups: list[list[int]]
    num_groups: int = 0
    elapsed: float = 0.0
    verified: bool = False
    first_legal_elapsed: float | None = None
    groups_complete: bool = True
    group_masks: np.ndarray | None = None
    route_module: str = ""
    solution_source: str = "search"
    route_case: str | None = None

    def __post_init__(self) -> None:
        if self.num_groups <= 0:
            if self.group_masks is not None:
                self.num_groups = int(len(self.group_masks))
            else:
                self.num_groups = len(self.groups)

    def preview_groups(self, limit: int | None = None) -> list[list[int]]:
        """Return at most ``limit`` groups, materialising from masks if needed."""
        if self.group_masks is None or self.groups_complete:
            if limit is None or len(self.groups) <= limit:
                return self.groups
            return self.groups[:limit]

        masks = self.group_masks if limit is None else self.group_masks[:limit]
        return [sorted(mask_to_elements(int(m))) for m in masks]


@dataclass(frozen=True)
class GreedyStrategy:
    name: str
    coverage_weight: float = 1.0
    rarity_weight: float = 0.0
    randomize: bool = False
    noise_scale: float = 0.35
    rcl_fraction: float = 0.0
    rcl_min_count: int = 1
    spread_tiebreak: bool = False
    spread_recent: int = 24
    spread_pool_cap: int = 512
    top_k_scale: float = 1.0
    destroy_repair_rounds: int = 0


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------

def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


DEFAULT_BATCH_BYTES = 128 * 1024 * 1024
MAX_BATCH_BYTES = _env_int("CK_BATCH_BYTES", DEFAULT_BATCH_BYTES)


def _n_solver_module_name(n: int) -> str | None:
    return None


class CoveringDesignSolver:
    """Greedy + local-search + SA solver for covering designs."""

    _huge_result_preview_limit = 128

    def __init__(
        self,
        n: int,
        k: int,
        j: int,
        s: int,
        t: int = 1,
        *,
        progress_cb: Callable[[SolverProgress], None] | None = None,
        cancel_fn: Callable[[], bool] | None = None,
        num_attempts: int = 3,
        time_budget_sec: float | None = None,
        skip_final_verify: bool = False,
    ) -> None:
        # For t > 1, delegate to TCoveringSolver
        if t > 1:
            from n_algorithms.shared.tcovering_solver import TCoveringSolver
            self._tcovering_solver = TCoveringSolver(
                n=n, k=k, j=j, s=s, t=t,
                progress_cb=progress_cb,
                cancel_fn=cancel_fn,
                num_attempts=num_attempts,
                time_budget_sec=time_budget_sec,
            )
            self._is_tcovering = True
            # Set basic attributes for compatibility
            self.n = n
            self.k = k
            self.j = j
            self.s = s
            self.t = t
            return

        self._delegated_solver = None
        route_module_name = _n_solver_module_name(n)
        if route_module_name is not None and os.environ.get("CK_DISABLE_N_ROUTING") != "1":
            route_module = importlib.import_module(route_module_name)
            delegated_cls = getattr(route_module, "CoveringDesignSolver")
            self._delegated_solver = delegated_cls(
                n=n,
                k=k,
                j=j,
                s=s,
                t=t,
                progress_cb=progress_cb,
                cancel_fn=cancel_fn,
                num_attempts=num_attempts,
                time_budget_sec=time_budget_sec,
                skip_final_verify=skip_final_verify,
            )
            self._is_tcovering = False
            self.n = n
            self.k = k
            self.j = j
            self.s = s
            self.t = t
            return
        
        self._is_tcovering = False
        
        # Start timing from initialization to include preprocessing
        self._t0 = time.time()
        
        self.n = n
        self.k = k
        self.j = j
        self.s = s
        self.t = t
        self._cb = progress_cb
        self._cancel = cancel_fn or (lambda: False)
        self._num_attempts = max(1, num_attempts)
        self._time_budget_sec = (
            float(time_budget_sec) if time_budget_sec is not None and time_budget_sec > 0 else None
        )
        # Keep a safety margin to reduce borderline timeout overruns.
        self._time_budget_margin_sec = 0.0
        if self._time_budget_sec is not None:
            self._time_budget_margin_sec = 2.5 if n >= 16 else 0.8
        self._deadline_at = (
            self._t0 + max(0.0, self._time_budget_sec - self._time_budget_margin_sec)
            if self._time_budget_sec is not None
            else None
        )
        self._skip_final_verify = skip_final_verify
        self._first_legal_elapsed: float | None = None
        self._n16_anchor_module_enabled = bool(_env_int("CK_N16_ANCHOR_MODULE", 0))
        self._n17_special_case_key = make_n17_case_key(n, k, j, s)
        self._n17_special_case_family = classify_n17_special_case(n, k, j, s)
        self._n17_special_case_enabled = is_n17_special_case(n, k, j, s)
        n17_spec = get_n17_case_spec(n, k, j, s)
        self._n17_special_case_bucket = None if n17_spec is None else n17_spec.bucket

        if not 7 <= n <= 25:
            raise ValueError(f"n must be 7-25, got {n}")
        if not 4 <= k <= 7:
            raise ValueError(f"k must be 4-7, got {k}")
        if not 3 <= s <= 7:
            raise ValueError(f"s must be 3-7, got {s}")
        if not s <= j <= k:
            raise ValueError(f"Need s<=j<=k, got s={s} j={j} k={k}")
        if n < k:
            raise ValueError(f"Need n>=k, got n={n} k={k}")
        
        # Validate t parameter (only t=1 in this path)
        max_t = comb(j, s)
        if not 1 <= t <= max_t:
            raise ValueError(f"t must be between 1 and C({j},{s})={max_t}, got {t}")

        self._reference_bounds = get_bounds(n, k, j, s)
        baseline_blocks = _n_le_15_baseline_index().get((int(n), int(k), int(j), int(s)))
        self._acceptance_upper_bound = (
            int(math.ceil(baseline_blocks * 1.10))
            if baseline_blocks is not None and int(n) <= 15
            else None
        )
        self._containment = s == j

        elems = list(range(n))
        self.target_masks = np.array(
            [elements_to_mask(c) for c in combinations(elems, j)],
            dtype=np.uint32,
        )
        if j == k:
            self.cand_masks = self.target_masks.copy()
        else:
            self.cand_masks = np.array(
                [elements_to_mask(c) for c in combinations(elems, k)],
                dtype=np.uint32,
            )
        self.num_targets = len(self.target_masks)
        self.num_cands = len(self.cand_masks)
        self._interaction_scale = self.num_targets * self.num_cands
        self._identity_cover = bool(self._containment and self.j == self.k)

        self._batch_bytes = MAX_BATCH_BYTES
        self._base_top_k = self._choose_top_k()
        self._cand_index_map = {
            int(mask): idx for idx, mask in enumerate(self.cand_masks)
        }
        self._cand_has_elem: np.ndarray | None = None
        self._target_has_elem: np.ndarray | None = None
        self._target_weights = np.ones(self.num_targets, dtype=np.float64)
        self._base_weighted_scores: np.ndarray | None = None
        self._gpu_enabled = False
        self._gpu_failed = False
        self._cand_masks_gpu = None
        self._target_masks_gpu = None
        self._cov_table: list[np.ndarray] | None = None
        self._inv_table: list[np.ndarray] | None = None
        self._jsub_table: np.ndarray | None = None

        if self._identity_cover:
            return

        gpu_min_interaction = max(0, _env_int("CK_GPU_MIN_INTERACTION", 0))
        self._gpu_enabled = bool(
            _env_int("CK_USE_GPU", 1)
            and cp is not None
            and self._interaction_scale >= gpu_min_interaction
            and _probe_gpu_batch_path()
        )

        mem_estimate = self.num_cands * self.num_targets
        skip_dense_cov_tables = bool(
            self._n17_special_case_enabled
            and self._n17_special_case_bucket == "tiny_baseline_exactish"
            and self.j == self.k == 7
            and self.s <= 4
        )
        if skip_dense_cov_tables:
            self._init_heuristic_cache()
        elif self._containment and mem_estimate > 20_000_000:
            self._build_jsub_table()
        elif mem_estimate <= 500_000_000:
            self._build_coverage_tables()
        elif self._containment:
            self._build_jsub_table()

        if self._cov_table is None:
            self._init_heuristic_cache()

        self._target_weights = self._build_target_weights()
        if self._inv_table is not None:
            self._base_weighted_scores = self._build_base_weighted_scores()

    # ------------------------------------------------------------------
    # Precomputation
    # ------------------------------------------------------------------

    def _build_coverage_tables(self) -> None:
        """Build cov_table[ci]->targets and inv_table[ti]->candidates."""
        cov: list[list[int]] = [[] for _ in range(self.num_cands)]
        inv: list[list[int]] = [[] for _ in range(self.num_targets)]

        bs = max(1, 400_000_000 // max(1, self.num_targets * 4))
        bs = min(bs, self.num_cands)

        for start in range(0, self.num_cands, bs):
            if self._cancel():
                return
            end = min(start + bs, self.num_cands)
            batch = self.cand_masks[start:end]
            ints = batch[:, None] & self.target_masks[None, :]
            if self._containment:
                hits = ints == self.target_masks[None, :]
            else:
                hits = popcount_uint32(ints) >= self.s
            ci_arr, ti_arr = np.nonzero(hits)
            for ci_local, ti in zip(ci_arr, ti_arr):
                ci = start + int(ci_local)
                ti = int(ti)
                cov[ci].append(ti)
                inv[ti].append(ci)

        self._cov_table = [np.array(c, dtype=np.int32) for c in cov]
        self._inv_table = [np.array(c, dtype=np.int32) for c in inv]

    def _build_jsub_table(self) -> None:
        """For each candidate, store indices of its j-subsets in target_masks."""
        cpj = comb(self.k, self.j)
        target_idx: dict[int, int] = {
            int(self.target_masks[i]): i for i in range(self.num_targets)
        }

        table = np.empty((self.num_cands, cpj), dtype=np.int32)
        for ci in range(self.num_cands):
            bits = _extract_bits(int(self.cand_masks[ci]))
            for ji, jsub_bits in enumerate(combinations(bits, self.j)):
                jmask = 0
                for b in jsub_bits:
                    jmask |= b
                table[ci, ji] = target_idx[jmask]
        self._jsub_table = table

        cov: list[list[int]] = [[] for _ in range(self.num_cands)]
        inv: list[list[int]] = [[] for _ in range(self.num_targets)]
        for ci in range(self.num_cands):
            for ti in table[ci]:
                tii = int(ti)
                cov[ci].append(tii)
                inv[tii].append(ci)
        self._cov_table = [np.array(c, dtype=np.int32) for c in cov]
        self._inv_table = [np.array(c, dtype=np.int32) for c in inv]

    def _init_heuristic_cache(self) -> None:
        bits = (np.uint32(1) << np.arange(self.n, dtype=np.uint32))
        self._cand_has_elem = (
            (self.cand_masks[:, None] & bits[None, :]) != 0
        ).astype(np.uint8, copy=False)
        self._target_has_elem = (
            (self.target_masks[:, None] & bits[None, :]) != 0
        ).astype(np.uint8, copy=False)

    def _build_target_weights(self) -> np.ndarray:
        if self._inv_table is not None:
            support = np.array(
                [len(cands) for cands in self._inv_table],
                dtype=np.float64,
            )
        else:
            cand_has = self._cand_has_elem
            target_has = self._target_has_elem
            assert cand_has is not None and target_has is not None
            elem_support = cand_has.sum(axis=0, dtype=np.float64)
            elem_support = np.maximum(elem_support, 1.0)
            support = (target_has @ elem_support) / max(1, self.j)

        mean_support = max(float(np.mean(support)), 1.0)
        rarity = np.sqrt(mean_support / np.maximum(support, 1.0))
        return np.clip(rarity, 1.0, 3.0)

    def _build_base_weighted_scores(self) -> np.ndarray:
        inv_table = self._inv_table
        assert inv_table is not None

        weighted_scores = np.zeros(self.num_cands, dtype=np.float64)
        for ti, affected in enumerate(inv_table):
            if len(affected) == 0:
                continue
            weighted_scores[affected] += self._target_weights[ti]
        return weighted_scores

    def _choose_top_k(self) -> int:
        if self._interaction_scale >= 60_000_000_000:
            return min(600, self.num_cands)
        if self._interaction_scale >= 20_000_000_000:
            return min(800, self.num_cands)
        if self._interaction_scale >= 5_000_000_000:
            return min(1000, self.num_cands)
        if self._interaction_scale >= 1_000_000_000:
            return min(1200, self.num_cands)
        return min(2000, self.num_cands)

    def _top_k_for_remaining(self, remaining: int) -> int:
        top_k = self._base_top_k
        if remaining <= 20_000:
            top_k = min(self.num_cands, max(top_k, 1200))
        if remaining <= 5_000:
            top_k = min(self.num_cands, max(top_k, 2000))
        return max(1, top_k)

    def _strategy_top_k(self, remaining: int, strategy: GreedyStrategy) -> int:
        top_k = self._top_k_for_remaining(remaining)
        if strategy.top_k_scale != 1.0:
            top_k = int(math.ceil(top_k * strategy.top_k_scale))
        return max(1, min(self.num_cands, top_k))

    def _gpu_active(self) -> bool:
        return bool(self._gpu_enabled and not self._gpu_failed and cp is not None)

    def _gpu_disable(self, message: str) -> None:
        if not self._gpu_failed:
            self._gpu_failed = True
            self._report("gpu", message)

    def _ensure_gpu_mask_cache(self) -> None:
        assert cp is not None
        if self._target_masks_gpu is None:
            self._target_masks_gpu = cp.asarray(self.target_masks, dtype=cp.uint32)
        if self._cand_masks_gpu is None:
            self._cand_masks_gpu = cp.asarray(self.cand_masks, dtype=cp.uint32)

    def _gpu_target_chunk(self, num_cands: int, num_targets: int) -> int:
        assert cp is not None
        free_mem, _ = cp.cuda.Device().mem_info
        budget = free_mem * 0.3
        full_bytes = num_cands * num_targets * 12
        if full_bytes <= budget:
            return int(num_targets)
        approx_bytes_per_target = max(4, num_cands * 12)
        chunk = int(budget // approx_bytes_per_target)
        return int(max(2048, min(num_targets, max(1, chunk))))

    def _gpu_mask_chunk(self, num_targets: int, num_masks: int) -> int:
        assert cp is not None
        free_mem, _ = cp.cuda.Device().mem_info
        approx_bytes_per_mask = max(8, num_targets * 12)
        chunk = int((free_mem * 0.2) // approx_bytes_per_mask)
        return int(max(1, min(num_masks, max(1, chunk))))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def solve(self) -> SolverResult:
        # Delegate to TCoveringSolver if t > 1
        if hasattr(self, '_is_tcovering') and self._is_tcovering:
            return self._tcovering_solver.solve()
        if self._delegated_solver is not None:
            return self._delegated_solver.solve()
        
        if self._identity_cover:
            return self._solve_identity_cover()
        exact_small = self._solve_small_exact_cover()
        if exact_small is not None:
            return exact_small

        best: list[int] | None = None
        base_attempts = self._effective_attempts()
        profile_attempts = self._phase_a_profile_attempts(base_attempts)
        hard_cap = self._phase_a_hard_attempt_cap(base_attempts, profile_attempts)
        
        # N=12 optimization: aggressive early stopping (10% error tolerance)
        # Exception: L_12_6_4_3 uses original algorithm
        # N=13 optimization: only L_13_6_5_5 uses optimization
        # N=14 optimization: minimize main loop, maximize refinement
        # Exception: L_14_7_7_6 uses original algorithm (too difficult for optimization)
        if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
            hard_cap = min(hard_cap, 4)
            stagnation_limit_override = 2
        elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
            hard_cap = min(hard_cap, 4)
            stagnation_limit_override = 2
        elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
            # All n=14 except L_14_7_7_6: use hard_cap=3
            hard_cap = min(hard_cap, 3)
            stagnation_limit_override = 2
        else:
            stagnation_limit_override = None
        
        profiles = self._build_attempt_profiles(profile_attempts)

        attempt = 0
        stagnant = 0
        avg_attempt_sec: float | None = None
        best_updated_at: float | None = None
        last_sol_sig: int | None = None
        same_sig_streak = 0
        tail_reserve_triggered = False

        if self._gpu_enabled:
            self._report("gpu", "GPU batch scoring enabled")

        if self._should_build_fast_seed():
            seed = self._fast_seed_solution()
            if seed:
                best = seed
                best_updated_at = time.time()
                self._note_legal_solution()
                self._report("seed", f"Fast legal seed: {len(seed)} groups")
                if self._can_stop_at_acceptance(best):
                    self._report(
                        "optimize",
                        f"Acceptance target reached from seed: {len(best)} groups",
                    )
        
        # N18 optimization: refine seed for small j=k non-containment cases
        if (
            best is not None
            and self.n == 18
            and is_n18_special_case is not None
            and run_n18_specialized_module is not None
            and is_n18_special_case(self.n, self.k, self.j, self.s)
            and self.j == self.k
            and not self._containment
            and self.num_targets < 30_000
        ):
            best = run_n18_specialized_module(self, best)

        large_seed_intensify = self._is_large_j_equals_k_noncontainment()
        while attempt < hard_cap:
            if self._can_stop_at_acceptance(best):
                self._report(
                    "optimize",
                    f"Acceptance target reached: {len(best)} groups",
                )
                break
            attempt_idx = attempt + 1
            if self._cancel():
                break
            if best is not None and self._deadline_at is not None:
                reserve_sec = self._tail_refine_reserve_sec()
                if reserve_sec > 0.0:
                    rem = self._time_remaining_sec()
                    if rem is not None and rem <= reserve_sec:
                        if not tail_reserve_triggered:
                            self._report(
                                "optimize",
                                (
                                    "Stop main loop early to reserve "
                                    f"{reserve_sec:.1f}s for cluster modules"
                                ),
                            )
                            tail_reserve_triggered = True
                        break
            if self._phase_a_should_stop_for_budget(avg_attempt_sec):
                break
            if self._phase_a_should_stop_for_stagnation(
                best=best,
                best_updated_at=best_updated_at,
                attempt=attempt,
                stagnant=stagnant,
                same_sig_streak=same_sig_streak,
                avg_attempt_sec=avg_attempt_sec,
            ):
                break

            base_profile = profiles[attempt % len(profiles)]
            profile = self._phase_b_strategy_variant(base_profile, attempt_idx)
            attempt_started_at = time.time()
            best_len_at_start = len(best) if best is not None else None
            seed_mode = large_seed_intensify and best is not None
            if seed_mode:
                sol = list(best)
                complete = True
                remaining = 0
                self._report(
                    "optimize",
                    (
                        f"Attempt {attempt_idx}/{hard_cap}: intensify {profile.name} "
                        f"from {len(sol)} groups..."
                    ),
                )
            else:
                self._report(
                    "greedy",
                    f"Attempt {attempt_idx}/{hard_cap}: {profile.name}...",
                )
                sol, complete, remaining = self._greedy(profile)
                if complete and (best is None or len(sol) < len(best)):
                    best = sol
                    self._note_legal_solution()

                if self._cancel():
                    if sol and not complete and self._should_repair_partial(remaining, best):
                        repaired = self._fast_complete_partial_solution(
                            sol,
                            best_limit=len(best) if best is not None else None,
                        )
                        if repaired and (best is None or len(repaired) < len(best)):
                            best = repaired
                            self._note_legal_solution()
                    break
                if not complete:
                    if sol and self._should_repair_partial(remaining, best):
                        repaired = self._fast_complete_partial_solution(
                            sol,
                            best_limit=len(best) if best is not None else None,
                        )
                        if repaired and (best is None or len(repaired) < len(best)):
                            best = repaired
                            self._note_legal_solution()
                    break

                self._report(
                    "optimize",
                    f"Attempt {attempt_idx}: optimise {profile.name} ({len(sol)} groups)...",
                )
            sol = self._optimise_solution(
                sol,
                profile,
                best_len=len(best) if best is not None else None,
                stagnant=stagnant,
            )
            sol_sig = hash(tuple(sol))
            if last_sol_sig is not None and sol_sig == last_sol_sig:
                same_sig_streak += 1
            else:
                same_sig_streak = 0
            last_sol_sig = sol_sig

            improved = best is None or len(sol) < len(best)
            if improved:
                best = sol
                stagnant = 0
                same_sig_streak = 0
                self._note_legal_solution()
                self._report(
                    "optimize",
                    f"Best so far: {len(best)} groups (attempt {attempt_idx})",
                )
            else:
                stagnant += 1

            if best is not None and (
                best_len_at_start is None or len(best) < best_len_at_start
            ):
                best_updated_at = time.time()
                if self._can_stop_at_acceptance(best):
                    self._report(
                        "optimize",
                        f"Acceptance target reached after attempt {attempt_idx}: {len(best)} groups",
                    )
                    break

            attempt_elapsed = max(0.0, time.time() - attempt_started_at)
            if avg_attempt_sec is None:
                avg_attempt_sec = attempt_elapsed
            else:
                avg_attempt_sec = (avg_attempt_sec * 0.7) + (attempt_elapsed * 0.3)

            attempt += 1
            
            # N=12 optimization: aggressive early stopping (10% error tolerance)
            stag_limit = stagnation_limit_override if stagnation_limit_override is not None else self._phase_a_stagnation_limit()
            
            if (
                attempt >= base_attempts
                and stagnant >= stag_limit
                and not self._phase_a_can_extend_search(avg_attempt_sec, attempt, hard_cap)
            ):
                break

        if best is not None:
            # N18 optimization: refine before Phase E for k=7, j=6, s>=5 cases
            if (
                self.n == 18
                and is_n18_special_case is not None
                and run_n18_specialized_module is not None
                and is_n18_special_case(self.n, self.k, self.j, self.s)
                and not self._containment
                and self.k == 7
                and self.j == 6
                and self.s >= 5
            ):
                best = run_n18_specialized_module(self, best)
            
            best = self._phase_e_mid_compact_search(best)
            
            # N18 optimization: refine after Phase E for all n=18 special cases
            if (
                self.n == 18
                and is_n18_special_case is not None
                and run_n18_specialized_module is not None
                and is_n18_special_case(self.n, self.k, self.j, self.s)
            ):
                best = run_n18_specialized_module(self, best)
            
            best = self._phase_f_small_cp_sat_polish(best)
            best = self._phase_f_mid_cp_sat_refine(best)
            best = self._phase_i_nlt16_cluster_specialized_refine(best)
            best = self._phase_k_cluster_structural_refine(best)
            best = self._phase_h_nlt16_cp_sat_refine(best)
            # N=12 optimization: skip Phase G to save time (10% error tolerance)
            # Exception: L_12_6_4_3 uses original algorithm
            # N=13: only L_13_6_5_5 skips Phase G
            if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
                pass  # Skip Phase G for optimized n=12 cases
            elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
                pass  # Skip Phase G for L_13_6_5_5
            else:
                best = self._phase_g_nlt16_fixed_size_polish(best)
            best = self._phase_h_nlt16_cp_sat_refine(best)
            best = self._phase_i_nlt16_cluster_specialized_refine(best)
            best = self._phase_k_cluster_structural_refine(best)
            best = self._phase_n17_specialized_module_dispatch(best)
            
            # N=12 optimization: reduce final refinement (10% error tolerance)
            # Exception: L_12_6_4_3 uses original algorithm
            # N=13: only L_13_6_5_5 uses reduced refinement
            if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
                final_rounds = 1
                final_time_threshold = 2.0
            elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
                final_rounds = 1
                final_time_threshold = 2.0
            else:
                final_rounds = 2
                final_time_threshold = 6.0
            
            if self.n < 16 and self._deadline_at is not None:
                for _ in range(final_rounds):
                    rem = self._time_remaining_sec()
                    if rem is None or rem < final_time_threshold:
                        break
                    before = len(best)
                    best = self._phase_h_nlt16_cp_sat_refine(best)
                    best = self._phase_i_nlt16_cluster_specialized_refine(best)
                    best = self._phase_k_cluster_structural_refine(best)
                    if len(best) >= before:
                        break

        masks = best or []
        return SolverResult(
            groups=[sorted(mask_to_elements(m)) for m in masks],
            elapsed=time.time() - self._t0,
            verified=False,  # Skip verification by default, only verify when user requests
            first_legal_elapsed=self._first_legal_elapsed,
            route_module=__name__,
            solution_source="search",
            route_case=f"L({self.n},{self.k},{self.j},{self.s})",
        )

    def _should_use_small_exact_cover(self) -> bool:
        if cp_model is None:
            return False
        if self.n >= 12:
            return False
        if self._cov_table is None or self._inv_table is None:
            return False
        if self.num_cands > 600 or self.num_targets > 600:
            return False
        return True

    def _small_exact_time_budget(self) -> float:
        remaining = self._time_remaining_sec()
        if remaining is None:
            return 12.0
        if remaining <= 0.8:
            return 0.0
        return max(1.0, min(12.0, remaining * 0.5))

    def _solve_small_exact_cover(self) -> SolverResult | None:
        if not self._should_use_small_exact_cover():
            return None

        budget = self._small_exact_time_budget()
        if budget <= 0.0:
            return None

        assert cp_model is not None
        assert self._inv_table is not None

        self._report(
            "optimize",
            (
                "Small-n exact module: "
                f"L({self.n},{self.k},{self.j},{self.s}), "
                f"targets={self.num_targets}, cands={self.num_cands}, "
                f"budget={budget:.1f}s"
            ),
        )

        seed_strategy = GreedyStrategy(
            name="small-exact-seed",
            coverage_weight=1.0,
            rarity_weight=0.2,
            randomize=False,
            spread_tiebreak=True,
        )
        seed_sol, complete, _ = self._greedy(seed_strategy)
        seed_masks: list[int] = []
        if complete:
            seed_sol = self._local_search(seed_sol)
            if seed_sol:
                seed_masks = list(seed_sol)

        model = cp_model.CpModel()
        vars_x = [model.NewBoolVar(f"x_{i}") for i in range(self.num_cands)]
        objective = sum(vars_x)

        for ti, inv in enumerate(self._inv_table):
            if len(inv) == 0:
                self._report("optimize", f"Small-n exact skipped: uncovered target {ti}")
                return None
            model.Add(sum(vars_x[int(ci)] for ci in inv) >= 1)

        if seed_masks:
            seed_limit = len(seed_masks)
            model.Add(objective <= seed_limit)
            for mask in seed_masks:
                ci = self._cand_index_map.get(int(mask))
                if ci is not None:
                    model.AddHint(vars_x[ci], 1)

        model.Minimize(objective)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = float(budget)
        solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        solver.parameters.random_seed = 0

        status = solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            self._report("optimize", "Small-n exact module returned no feasible solution")
            return None

        picked_idx = [i for i in range(self.num_cands) if solver.Value(vars_x[i]) == 1]
        if not picked_idx:
            return None

        masks = [int(self.cand_masks[i]) for i in picked_idx]
        masks = self._local_search(masks)
        if not self._verify(masks):
            return None

        self._note_legal_solution()
        proven = "optimal" if status == cp_model.OPTIMAL else "feasible"
        self._report(
            "optimize",
            f"Small-n exact module ({proven}) found {len(masks)} groups",
        )

        return SolverResult(
            groups=[sorted(mask_to_elements(m)) for m in masks],
            elapsed=time.time() - self._t0,
            verified=False,  # Skip verification by default
            first_legal_elapsed=self._first_legal_elapsed,
            route_module=__name__,
            solution_source="exact_small",
            route_case=f"L({self.n},{self.k},{self.j},{self.s})",
        )

    def _solve_identity_cover(self) -> SolverResult:
        """专用模块：显式构造 j=k=s 时所需的全部组合。"""
        self._report(
            "special",
            f"Identity module: building explicit C({self.n},{self.k}) groups",
        )

        def _on_progress(done: int, total: int) -> None:
            remaining = max(0, total - done)
            self._report(
                "special",
                f"Identity build progress: {done}/{total}",
                iteration=done,
                sol_size=done,
                remaining=remaining,
                total=total,
            )

        built = build_identity_cover(
            self.n,
            self.k,
            cancel_fn=self._cancel,
            progress_cb=_on_progress,
            report_interval=8192,
        )

        masks = built.masks
        if built.complete:
            self._note_legal_solution()

        preview_limit = min(self._huge_result_preview_limit, len(masks))
        preview_masks = masks[:preview_limit]
        preview_groups = [sorted(mask_to_elements(int(m))) for m in preview_masks]

        fully_materialized = built.complete and len(masks) <= self._huge_result_preview_limit
        groups = (
            [sorted(mask_to_elements(int(m))) for m in masks]
            if fully_materialized
            else preview_groups
        )

        return SolverResult(
            groups=groups,
            num_groups=len(masks),
            elapsed=time.time() - self._t0,
            verified=False,  # Skip verification by default
            first_legal_elapsed=self._first_legal_elapsed,
            groups_complete=fully_materialized,
            group_masks=masks,
            route_module=__name__,
            solution_source="identity_cover",
            route_case=f"L({self.n},{self.k},{self.j},{self.s})",
        )

    def _phase_n17_specialized_module_dispatch(self, sol: list[int]) -> list[int]:
        if not self._n17_special_case_enabled:
            return sol
        return run_n17_specialized_module(self, sol)

    def _effective_attempts(self) -> int:
        num_att = self._num_attempts
        if self._interaction_scale >= 900_000_000:
            return min(num_att, 1)
        if self._interaction_scale >= 350_000_000 or self.num_cands >= 30_000:
            return min(num_att, 2)
        if (
            self._interaction_scale >= 120_000_000
            or self.num_targets >= 3_000
            or self.num_cands >= 12_000
        ):
            return min(num_att, 2)
        if self.num_targets >= 700 or self.num_cands >= 5_000:
            return min(num_att, 3)
        return num_att

    def _phase_a_profile_attempts(self, base_attempts: int) -> int:
        if self._is_large_j_equals_k_noncontainment():
            min_profiles = 5
        elif self._is_mid_j_equals_k_noncontainment():
            min_profiles = 5
        elif self._interaction_scale <= 30_000_000:
            min_profiles = 3
        else:
            min_profiles = 2
        return min(5, max(base_attempts, min_profiles))

    def _phase_a_hard_attempt_cap(self, base_attempts: int, profile_attempts: int) -> int:
        if (
            self._deadline_at is not None
            and self._n17_special_case_enabled
            and self._n17_special_case_bucket == "tiny_baseline_exactish"
            and self.num_targets <= 2_500
        ):
            max_cap = 7 if self.k <= 4 else 8
            return max(profile_attempts, min(max_cap, base_attempts + 4))
        if (
            self._deadline_at is not None
            and self.n < 16
            and self._interaction_scale <= 120_000_000
        ):
            if self.j == self.k and not self._containment:
                max_cap = 9 if self.num_targets >= 3_000 else 10
                extra = 5
            elif self._containment:
                max_cap = 14 if self.k >= 6 else 12
                extra = 10
            else:
                max_cap = 14
                extra = 10
            return max(profile_attempts, min(max_cap, base_attempts + extra))
        if (
            self._deadline_at is not None
            and self.n == 16
            and self._interaction_scale <= 130_000_000
            and self._is_n16_hard_cluster()
        ):
            if self.j == self.k and not self._containment:
                max_cap = 8 if self.num_targets >= 8_000 else 9
                extra = 4
            elif self._containment:
                max_cap = 10 if self.k >= 6 else 8
                extra = 5
            else:
                max_cap = 9
                extra = 4
            return max(profile_attempts, min(max_cap, base_attempts + extra))
        if self._deadline_at is not None and self._is_large_j_equals_k_noncontainment():
            max_cap = 20
            return max(profile_attempts, min(max_cap, base_attempts + 18))
        if self._deadline_at is not None and self._is_mid_j_equals_k_noncontainment():
            if self.num_targets <= 10_000:
                max_cap = 12
                return max(profile_attempts, min(max_cap, base_attempts + 8))
            max_cap = 5
            return max(profile_attempts, min(max_cap, base_attempts + 3))
        if self._deadline_at is None:
            if self._interaction_scale <= 2_000_000:
                extra = 4
            elif self._interaction_scale <= 30_000_000:
                extra = 3
            elif self._interaction_scale <= 200_000_000:
                extra = 2
            else:
                extra = 1
        else:
            if self._interaction_scale <= 2_000_000:
                extra = 6
            elif self._interaction_scale <= 30_000_000:
                extra = 6
            elif self._interaction_scale <= 200_000_000:
                extra = 4
            else:
                extra = 3
        return max(profile_attempts, base_attempts + extra)

    def _phase_a_reserved_polish_budget(self) -> float:
        if self.n > 16:
            return 0.0
        if self.n == 16:
            if not self._is_n16_hard_cluster():
                return 0.0
            if self.j == self.k and not self._containment:
                if self.num_targets >= 8_000:
                    return 16.0
                if self.num_targets >= 3_000:
                    return 14.0
                return 12.0
            if self._containment:
                if self.k >= 6:
                    return 12.0
                if self.num_targets >= 2_000:
                    return 10.0
                return 8.0
            if self.num_targets >= 2_000:
                return 9.0
            return 6.0
        if self.j == self.k and not self._containment:
            if self.num_targets >= 4_000:
                return 34.0
            if self.num_targets >= 1_500:
                return 28.0
            return 22.0
        if self._containment:
            if self.k >= 6 and self.n >= 14:
                return 18.0
            if self.num_targets >= 2_000:
                return 16.0
            return 12.0
        if self.num_targets >= 1_200:
            return 12.0
        return 8.0

    def _phase_a_stagnation_limit(self) -> int:
        if self._interaction_scale <= 2_000_000:
            return 2
        if self._interaction_scale <= 30_000_000:
            return 3
        if self._interaction_scale <= 200_000_000:
            return 3
        return 2

    def _target_reference_upper_bound(self) -> int | None:
        if self._identity_cover:
            return self.num_targets
        if self._containment:
            return self._reference_bounds.get("ljcr_best") or self._reference_bounds.get("lower_bound")
        return self._reference_bounds.get("lower_bound")

    def _acceptance_target_upper_bound(self) -> int | None:
        if self._acceptance_upper_bound is not None:
            return self._acceptance_upper_bound
        return self._target_reference_upper_bound()

    def _near_reference_quality(self, sol_len: int) -> bool:
        ref = self._acceptance_target_upper_bound()
        if not ref or ref <= 0:
            return False
        return sol_len <= int(math.ceil(ref * 1.10))

    def _can_stop_at_acceptance(self, sol: list[int] | None) -> bool:
        if not sol:
            return False
        target = self._acceptance_target_upper_bound()
        if not target or len(sol) > target:
            return False
        return self._skip_final_verify or self._verify(sol)

    def _tail_polish_round_limit(self, sol_len: int) -> int:
        if self.n >= 16:
            return 3
        if self._containment:
            if self._near_reference_quality(sol_len):
                return 1
            return 2 if self.n >= 14 and self.k >= 6 else 1
        if self.j == self.k and self.s == (self.k - 1):
            if self.n >= 14 or not self._near_reference_quality(sol_len):
                return 2
            return 1
        if self.j == self.k:
            return 1
        if self._near_reference_quality(sol_len):
            return 1
        return 2 if self.n >= 15 and sol_len <= 80 else 1

    def _should_skip_tail_phase(self, phase_tag: str, sol_len: int, pass_idx: int) -> bool:
        remaining = self._time_remaining_sec()
        if remaining is None or self.n >= 16:
            return False
        if pass_idx > 0 and remaining < 10.0:
            return True
        if self._near_reference_quality(sol_len):
            if phase_tag in {"phase_h", "phase_i_full", "phase_g"} and remaining < 20.0:
                return True
            if phase_tag in {"phase_h", "phase_i_full", "phase_k"} and pass_idx > 0:
                return True
        if self._near_reference_quality(sol_len) and sol_len <= 16 and phase_tag in {"phase_h", "phase_i_full", "phase_g"}:
            return True
        return False

    def _phase_tail_pass(self, sol: list[int], *, pass_idx: int) -> list[int]:
        best = list(sol)
        before = len(best)

        best = self._phase_e_mid_compact_search(best)
        best = self._phase_f_small_cp_sat_polish(best)
        best = self._phase_f_mid_cp_sat_refine(best)

        if not self._should_skip_tail_phase("phase_i_full", len(best), pass_idx):
            best = self._phase_i_nlt16_cluster_specialized_refine(best)
        if not self._should_skip_tail_phase("phase_k", len(best), pass_idx):
            best = self._phase_k_cluster_structural_refine(best)
        if not self._should_skip_tail_phase("phase_h", len(best), pass_idx):
            best = self._phase_h_nlt16_cp_sat_refine(best)
        if not self._should_skip_tail_phase("phase_g", len(best), pass_idx):
            best = self._phase_g_nlt16_fixed_size_polish(best)

        # Only revisit the expensive cluster passes when the current pass
        # actually shrinks the solution; otherwise they mostly burn the clock
        # rediscovering the same size.
        if len(best) < before:
            if not self._should_skip_tail_phase("phase_h", len(best), pass_idx + 1):
                best = self._phase_h_nlt16_cp_sat_refine(best)
            if not self._should_skip_tail_phase("phase_i_full", len(best), pass_idx + 1):
                best = self._phase_i_nlt16_cluster_specialized_refine(best)
            if not self._should_skip_tail_phase("phase_k", len(best), pass_idx + 1):
                best = self._phase_k_cluster_structural_refine(best)
        return best

    def _phase_run_tail_polish(self, sol: list[int]) -> list[int]:
        best = list(sol)
        round_limit = self._tail_polish_round_limit(len(best))

        for pass_idx in range(round_limit):
            remaining = self._time_remaining_sec()
            if remaining is not None:
                min_needed = 4.0 if pass_idx == 0 else 8.0
                if remaining < min_needed:
                    break
            before = len(best)
            best = self._phase_tail_pass(best, pass_idx=pass_idx)
            if len(best) >= before:
                if self.n < 16:
                    break
            elif self._near_reference_quality(len(best)) and pass_idx > 0:
                break
        return best

    def _time_remaining_sec(self) -> float | None:
        if self._deadline_at is None:
            return None
        return max(0.0, self._deadline_at - time.time())

    def _phase_a_should_stop_for_budget(self, avg_attempt_sec: float | None) -> bool:
        remaining = self._time_remaining_sec()
        if remaining is None:
            return False
        if self.n <= 16:
            reserve = self._phase_a_reserved_polish_budget()
            if self._first_legal_elapsed is not None and remaining <= reserve:
                self._report(
                    "optimize",
                    (
                        "Early stop: reserve budget for n<=16 polish "
                        f"(remaining={remaining:.1f}s, reserve={reserve:.1f}s)"
                    ),
                )
                return True
            return remaining <= 0.35
        if self._is_mid_j_equals_k_noncontainment() and self.num_targets > 12_000 and remaining <= 12.0:
            return True
        if remaining <= 0.15:
            return True
        if avg_attempt_sec is None:
            return False
        ratio = 0.6
        if self._is_large_j_equals_k_noncontainment():
            ratio = 0.35
        elif self._is_mid_j_equals_k_noncontainment():
            ratio = 0.45
        return remaining < max(0.15, avg_attempt_sec * ratio)

    def _phase_a_should_stop_for_stagnation(
        self,
        *,
        best: list[int] | None,
        best_updated_at: float | None,
        attempt: int,
        stagnant: int,
        same_sig_streak: int,
        avg_attempt_sec: float | None,
    ) -> bool:
        if best is None or best_updated_at is None:
            return False

        remaining = self._time_remaining_sec()
        if remaining is None:
            return False
        if (
            self.n <= 16
            and self._is_mid_j_equals_k_noncontainment()
            and attempt >= 4
            and stagnant >= 3
            and same_sig_streak >= 3
        ):
            reserve = self._phase_a_reserved_polish_budget()
            since_best = max(0.0, time.time() - best_updated_at)
            dyn_threshold = max(8.0, (avg_attempt_sec or 0.0) * 2.2)
            if remaining <= (reserve + 6.0) and since_best >= dyn_threshold:
                self._report(
                    "optimize",
                    (
                        "Early stop: n<=16 stagnation and switch to polish "
                        f"(no improve {since_best:.1f}s, stagnant={stagnant}, repeat={same_sig_streak})"
                    ),
                )
                return True
            return False
        if not self._is_large_j_equals_k_noncontainment():
            return False
        if attempt < 9 or stagnant < 7:
            return False
        if same_sig_streak < 7:
            return False

        since_best = max(0.0, time.time() - best_updated_at)
        dyn_threshold = 55.0
        if avg_attempt_sec is not None:
            dyn_threshold = max(dyn_threshold, avg_attempt_sec * 6.0)
        if since_best < dyn_threshold:
            return False

        self._report(
            "optimize",
            (
                "Early stop: stagnation detected "
                f"(no improve for {since_best:.1f}s, stagnant={stagnant}, repeat={same_sig_streak})"
            ),
        )
        return True

    def _phase_a_can_extend_search(
        self,
        avg_attempt_sec: float | None,
        attempt: int,
        hard_cap: int,
    ) -> bool:
        if attempt >= hard_cap:
            return False
        if self._interaction_scale <= 2_000_000:
            return False
        remaining = self._time_remaining_sec()
        if remaining is None:
            return False
        if self._is_large_j_equals_k_noncontainment() and avg_attempt_sec is not None:
            return remaining >= max(6.0, avg_attempt_sec * 0.8)
        if self._is_mid_j_equals_k_noncontainment() and avg_attempt_sec is not None:
            return remaining >= max(4.0, avg_attempt_sec * 0.75)
        if self._interaction_scale <= 2_000_000:
            retry_window = 3.0
        elif self._interaction_scale <= 30_000_000:
            retry_window = 6.0
        elif self._interaction_scale <= 200_000_000:
            retry_window = 8.0
        else:
            retry_window = 10.0
        if remaining <= retry_window:
            return False
        if avg_attempt_sec is not None and remaining < max(1.0, avg_attempt_sec * 1.25):
            return False
        return True

    def _phase_b_strategy_variant(
        self,
        strategy: GreedyStrategy,
        attempt_idx: int,
    ) -> GreedyStrategy:
        if attempt_idx <= 1:
            return strategy
        if not strategy.randomize:
            return strategy

        weight_jitter = 1.0 + ((random.random() - 0.5) * 0.24)
        rarity_jitter = 1.0 + ((random.random() - 0.5) * 0.4)
        topk_jitter = 1.0 + ((random.random() - 0.5) * 0.2)

        varied = replace(
            strategy,
            coverage_weight=max(0.65, strategy.coverage_weight * weight_jitter),
            rarity_weight=max(0.0, strategy.rarity_weight * rarity_jitter),
            top_k_scale=max(0.85, min(2.2, strategy.top_k_scale * topk_jitter)),
            noise_scale=max(0.25, strategy.noise_scale * (1.0 + random.random() * 0.6)),
            rcl_fraction=max(
                strategy.rcl_fraction,
                min(0.18, strategy.rcl_fraction * (1.0 + random.random() * 0.8)),
            ),
            rcl_min_count=max(2, strategy.rcl_min_count),
        )
        return varied

    def _enable_spread_tiebreak(self) -> bool:
        return (
            self._cov_table is not None
            and self.j == self.k
            and not self._containment
            and self.num_targets >= 12_000
        )

    def _is_large_j_equals_k_noncontainment(self) -> bool:
        return (
            not self._containment
            and self.j == self.k
            and self.num_targets >= 70_000
        )

    def _is_mid_j_equals_k_noncontainment(self) -> bool:
        return (
            not self._containment
            and self.j == self.k
            and 400 <= self.num_targets < 70_000
        )

    def _is_nlt16_cluster_target(self) -> bool:
        if self.n >= 16:
            return False
        if self._containment:
            return self.k >= 5
        if self.j == self.k:
            return True
        return self.k >= 6 and self.j >= 4

    def _tail_refine_reserve_sec(self) -> float:
        if self._n17_special_case_enabled:
            if self._n17_special_case_bucket == "tiny_baseline_exactish":
                if self.k >= 7:
                    return 42.0
                if self.k >= 6:
                    return 36.0
                return 30.0
            if self._n17_special_case_bucket == "general_k7_j6_hard":
                return 24.0
            if self._n17_special_case_bucket == "jk_large_delta_dense":
                return 18.0
            if self._n17_special_case_bucket == "containment_fast_bad_dense":
                return 18.0
            if self._n17_special_case_bucket == "general_j5_guidance_weak":
                return 16.0
        if self.n == 18 and is_n18_special_case is not None and is_n18_special_case(self.n, self.k, self.j, self.s):
            if self.j == self.k and not self._containment:
                if self.s == self.k - 1 and self.num_targets <= 4_000:
                    return 24.0
                if self.s == self.k - 1 and self.num_targets >= 30_000:
                    return 26.0
                if self.num_targets >= 18_000:
                    return 18.0
                return 12.0
            if (
                not self._containment
                and self.k == 7
                and self.j == 6
                and self.s >= 5
            ):
                return 12.0
            if self._containment:
                return 12.0
        if not self._is_nlt16_cluster_target():
            return 0.0
        if self._containment:
            if self.num_targets >= 2_000:
                return 34.0
            if self.num_targets >= 700:
                return 28.0
            return 22.0
        if self.j == self.k:
            if self.num_targets >= 2_000:
                return 30.0
            if self.num_targets >= 700:
                return 24.0
            return 18.0
        return 14.0

    def _is_n16_hard_cluster(self) -> bool:
        if self.n != 16:
            return False
        if self.j == self.k and not self._containment:
            return True
        if self._containment and self.k >= 6:
            return True
        if (not self._containment) and self.k >= 6 and self.j >= 4:
            return True
        return False

    def _n16_anchor_cluster(self) -> str:
        if self.n != 16:
            return "none"
        if self.k <= 5:
            if self._containment:
                return "n16_light_containment"
            if self.j == self.k:
                return "n16_light_jk"
            return "n16_light_general"
        if self.j == self.k and not self._containment:
            return "n16_hard_jk"
        if self._containment:
            return "n16_hard_containment"
        return "n16_hard_general"

    def _phase_n16_anchor_module_dispatch(self, sol: list[int]) -> list[int]:
        if not self._n16_anchor_module_enabled:
            return sol
        if self.n != 16:
            return sol
        if self._deadline_at is None:
            return sol
        remaining = self._time_remaining_sec()
        if remaining is None or remaining < 6.0:
            return sol

        cluster = self._n16_anchor_cluster()
        best = list(sol)

        if cluster.startswith("n16_light_"):
            best = self._phase_n16_light_exchange_module(best, module_tag=cluster)
            best = self._phase_n16_anchor_reseed(
                best,
                rounds=4,
                keep_ratio=0.56,
                min_remaining=4.0,
                module_tag=cluster,
                allow_same_len_fallback=True,
            )
            best = self._phase_n16_anchor_multi_drop(
                best,
                drop_plan=(2, 1),
                rounds_per_drop=3,
                ratio=0.30,
                cap=8.0,
                min_remaining=3.5,
                module_tag=cluster,
            )
            best = self._phase_n16_anchor_drop_one_intensify(
                best,
                rounds=7,
                ratio=0.24,
                cap=7.2,
                min_remaining=3.0,
                module_tag=cluster,
            )
            best = self._phase_n16_anchor_pair_compress(
                best,
                module_tag=cluster,
                max_pool=26,
                max_pairs=180,
                min_remaining=2.8,
            )
            if (
                cp_model is not None
                and self._inv_table is not None
                and (self.num_cands <= 5_000 or self.num_targets <= 4_500)
                and self._phase_c_has_time(7.0)
            ):
                best = self._phase_i_full_cp_sat_module(best, hard_case=False)
            return best

        if cluster == "n16_hard_jk":
            best = self._phase_n16_anchor_multi_drop(
                best,
                drop_plan=(2, 1),
                rounds_per_drop=4,
                ratio=0.34,
                cap=13.0,
                min_remaining=4.2,
                module_tag=cluster,
            )
            best = self._phase_n16_anchor_reseed(
                best,
                rounds=2,
                keep_ratio=0.72,
                min_remaining=6.0,
                module_tag=cluster,
                allow_same_len_fallback=False,
            )
            best = self._phase_n16_anchor_drop_one_intensify(
                best,
                rounds=5,
                ratio=0.26,
                cap=9.0,
                min_remaining=3.3,
                module_tag=cluster,
            )
            return self._phase_n16_anchor_pair_compress(
                best,
                module_tag=cluster,
                max_pool=34,
                max_pairs=260,
                min_remaining=3.0,
            )

        if cluster == "n16_hard_containment":
            best = self._phase_n16_anchor_multi_drop(
                best,
                drop_plan=(2, 1),
                rounds_per_drop=4,
                ratio=0.35,
                cap=14.0,
                min_remaining=4.2,
                module_tag=cluster,
            )
            best = self._phase_n16_anchor_reseed(
                best,
                rounds=2,
                keep_ratio=0.70,
                min_remaining=6.0,
                module_tag=cluster,
                allow_same_len_fallback=False,
            )
            best = self._phase_n16_anchor_drop_one_intensify(
                best,
                rounds=5,
                ratio=0.27,
                cap=9.6,
                min_remaining=3.3,
                module_tag=cluster,
            )
            return self._phase_n16_anchor_pair_compress(
                best,
                module_tag=cluster,
                max_pool=34,
                max_pairs=240,
                min_remaining=3.0,
            )

        if cluster == "n16_hard_general":
            best = self._phase_n16_anchor_multi_drop(
                best,
                drop_plan=(2, 1),
                rounds_per_drop=3,
                ratio=0.32,
                cap=11.0,
                min_remaining=4.0,
                module_tag=cluster,
            )
            best = self._phase_n16_anchor_reseed(
                best,
                rounds=2,
                keep_ratio=0.68,
                min_remaining=5.0,
                module_tag=cluster,
                allow_same_len_fallback=False,
            )
            best = self._phase_n16_anchor_drop_one_intensify(
                best,
                rounds=4,
                ratio=0.24,
                cap=8.4,
                min_remaining=3.2,
                module_tag=cluster,
            )
            return self._phase_n16_anchor_pair_compress(
                best,
                module_tag=cluster,
                max_pool=30,
                max_pairs=220,
                min_remaining=2.8,
            )

        return best

    def _phase_n16_anchor_drop_one_intensify(
        self,
        sol: list[int],
        *,
        rounds: int,
        ratio: float,
        cap: float,
        min_remaining: float,
        module_tag: str,
    ) -> list[int]:
        if self.n != 16:
            return sol
        if self._cov_table is None or self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 6:
            return sol

        best = list(sol)
        misses = 0
        for _ in range(max(1, rounds)):
            rem = self._time_remaining_sec()
            if rem is None or rem < min_remaining:
                break
            target_len = len(best) - 1
            if target_len < 1:
                break
            round_budget = float(min(cap, max(2.2, rem * ratio)))
            start_masks = list(best)
            if misses > 0 or random.random() < 0.7:
                random.shuffle(start_masks)
            improved = self._phase_g_try_target_len(start_masks, target_len, round_budget)
            if improved is None:
                misses += 1
                if misses >= 3:
                    break
                continue
            if len(improved) < len(best):
                best = improved
                misses = 0
                self._report(
                    "optimize",
                    f"N16 anchor {module_tag} drop-one improved to {len(best)} groups",
                )
                continue
            misses += 1
            if misses >= 3:
                break
        return best

    def _phase_n16_anchor_pair_compress(
        self,
        sol: list[int],
        *,
        module_tag: str,
        max_pool: int,
        max_pairs: int,
        min_remaining: float,
    ) -> list[int]:
        if self.n != 16:
            return sol
        if self._cov_table is None or self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 8:
            return sol

        cand_index = self._cand_index_map
        best_idx = [cand_index[m] for m in sol if m in cand_index]
        if len(best_idx) != len(sol):
            return sol
        cov_table = self._cov_table
        inv_table = self._inv_table

        while True:
            rem = self._time_remaining_sec()
            if rem is None or rem < min_remaining:
                break
            if len(best_idx) < 8:
                break

            counts = np.zeros(self.num_targets, dtype=np.int32)
            for ci in best_idx:
                counts[cov_table[ci]] += 1

            ranked: list[tuple[int, int, int]] = []
            for ci in best_idx:
                covered = cov_table[ci]
                unique_loss = int(np.sum(counts[covered] == 1))
                ranked.append((unique_loss, len(covered), ci))
            ranked.sort(key=lambda t: (t[0], t[1]))

            pool_size = max(3, min(len(ranked), max_pool))
            pool = [ci for _, _, ci in ranked[:pool_size]]
            if len(pool) < 3:
                break

            selected_set = set(best_idx)
            pair_checked = 0
            improved = False

            for a_pos in range(len(pool)):
                if improved:
                    break
                ci = pool[a_pos]
                cov_i = cov_table[ci]
                cov_i_set = set(int(t) for t in cov_i)
                for b_pos in range(a_pos + 1, len(pool)):
                    rem2 = self._time_remaining_sec()
                    if rem2 is None or rem2 < min_remaining:
                        break
                    pair_checked += 1
                    if pair_checked > max_pairs:
                        break

                    cj = pool[b_pos]
                    uncovered: set[int] = set()
                    for t in cov_i:
                        ti = int(t)
                        if counts[ti] == 1:
                            uncovered.add(ti)
                    for t in cov_table[cj]:
                        ti = int(t)
                        cti = counts[ti]
                        if cti == 1 or (cti == 2 and ti in cov_i_set):
                            uncovered.add(ti)
                    if not uncovered:
                        continue
                    if len(uncovered) > 120:
                        continue

                    ordered_targets = sorted(uncovered, key=lambda ti: len(inv_table[ti]))
                    candidate_set: set[int] | None = None
                    for ti in ordered_targets:
                        coverers = set(int(x) for x in inv_table[ti])
                        if candidate_set is None:
                            candidate_set = coverers
                        else:
                            candidate_set &= coverers
                        if not candidate_set:
                            break
                    if not candidate_set:
                        continue

                    reduced_set = set(selected_set)
                    reduced_set.discard(ci)
                    reduced_set.discard(cj)

                    chosen: int | None = None
                    best_cov = -1
                    for cand in sorted(candidate_set):
                        if cand in reduced_set:
                            continue
                        cov_len = len(cov_table[cand])
                        if cov_len > best_cov:
                            best_cov = cov_len
                            chosen = cand
                    if chosen is None:
                        continue

                    candidate_idx = [x for x in best_idx if x != ci and x != cj]
                    candidate_idx.append(chosen)
                    if len(candidate_idx) >= len(best_idx):
                        continue
                    candidate_masks = [int(self.cand_masks[x]) for x in candidate_idx]
                    if not self._verify(candidate_masks):
                        continue

                    best_idx = candidate_idx
                    self._report(
                        "optimize",
                        f"N16 anchor {module_tag} pair-compress improved to {len(best_idx)} groups",
                    )
                    improved = True
                    break

            if not improved:
                break

        return [int(self.cand_masks[ci]) for ci in best_idx]

    def _phase_n16_anchor_multi_drop(
        self,
        sol: list[int],
        *,
        drop_plan: tuple[int, ...],
        rounds_per_drop: int,
        ratio: float,
        cap: float,
        min_remaining: float,
        module_tag: str,
    ) -> list[int]:
        if self.n != 16:
            return sol
        if self._cov_table is None or self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 8:
            return sol

        best = list(sol)
        for drop in drop_plan:
            misses = 0
            for _ in range(max(1, rounds_per_drop)):
                rem = self._time_remaining_sec()
                if rem is None or rem < min_remaining:
                    return best
                target_len = len(best) - int(drop)
                if target_len < 1:
                    break
                round_budget = float(min(cap, max(2.6, rem * ratio)))
                start_masks = list(best)
                if misses > 0 or random.random() < 0.6:
                    random.shuffle(start_masks)
                improved = self._phase_g_try_target_len(start_masks, target_len, round_budget)
                if improved is None:
                    misses += 1
                    if misses >= 2:
                        break
                    continue
                if len(improved) < len(best):
                    best = improved
                    misses = 0
                    self._report(
                        "optimize",
                        f"N16 anchor {module_tag} multi-drop improved to {len(best)} groups",
                    )
                    continue
                misses += 1
                if misses >= 2:
                    break
        return best

    def _phase_n16_anchor_reseed(
        self,
        sol: list[int],
        *,
        rounds: int,
        keep_ratio: float,
        min_remaining: float,
        module_tag: str,
        allow_same_len_fallback: bool,
    ) -> list[int]:
        if self.n != 16:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 6:
            return sol

        best = list(sol)
        strategy_pool = [
            GreedyStrategy(
                name=f"{module_tag}-anchor-a",
                coverage_weight=0.90,
                rarity_weight=0.36,
                randomize=True,
                noise_scale=0.92,
                rcl_fraction=0.085,
                rcl_min_count=4,
                top_k_scale=1.6,
                destroy_repair_rounds=2,
            ),
            GreedyStrategy(
                name=f"{module_tag}-anchor-b",
                coverage_weight=0.98,
                rarity_weight=0.24,
                randomize=True,
                noise_scale=0.72,
                rcl_fraction=0.064,
                rcl_min_count=3,
                top_k_scale=1.45,
                destroy_repair_rounds=1,
            ),
        ]

        for round_idx in range(max(1, rounds)):
            rem = self._time_remaining_sec()
            if rem is None or rem < min_remaining:
                break
            keep = max(2, min(len(best) - 1, int(len(best) * keep_ratio)))
            if keep >= len(best):
                keep = len(best) - 1
            if keep < 2:
                break
            partial = random.sample(best, keep)
            base_strategy = strategy_pool[round_idx % len(strategy_pool)]
            strategy = self._phase_b_strategy_variant(base_strategy, attempt_idx=round_idx + 2)

            strict_limit = max(1, len(best) - 1)
            candidate, complete, _ = self._greedy(
                strategy,
                partial=partial,
                best_limit=strict_limit,
            )
            if (not complete) and allow_same_len_fallback and self._phase_c_has_time(3.2):
                relaxed_limit = len(best) + max(2, len(best) // 24)
                candidate, complete, _ = self._greedy(
                    strategy,
                    partial=partial,
                    best_limit=relaxed_limit,
                )
            if not complete:
                continue

            candidate = self._optimise_solution(
                candidate,
                strategy,
                best_len=len(best),
                stagnant=0,
            )
            if len(candidate) >= len(best):
                continue
            if not self._verify(candidate):
                continue

            best = candidate
            self._report(
                "optimize",
                f"N16 anchor {module_tag} reseed improved to {len(best)} groups",
            )

        return best

    def _phase_n16_light_exchange_module(
        self,
        sol: list[int],
        *,
        module_tag: str,
    ) -> list[int]:
        if self.n != 16:
            return sol
        if self.k > 5:
            return sol
        if self._cov_table is None or self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 10:
            return sol

        cand_index = self._cand_index_map
        best_indices = [cand_index[m] for m in sol if m in cand_index]
        if len(best_indices) != len(sol):
            return sol

        cov_table = self._cov_table
        best_len = len(best_indices)
        rounds = 10 if best_len >= 45 else 8

        for round_idx in range(rounds):
            rem = self._time_remaining_sec()
            if rem is None or rem < 3.2:
                break

            counts = np.zeros(self.num_targets, dtype=np.int32)
            for ci in best_indices:
                counts[cov_table[ci]] += 1

            removable: list[tuple[int, int, int]] = []
            for ci in best_indices:
                covered = cov_table[ci]
                unique_loss = int(np.sum(counts[covered] == 1))
                removable.append((unique_loss, len(covered), ci))
            removable.sort(key=lambda t: (t[0], t[1]))
            if len(removable) < 3:
                break

            if best_len >= 60:
                drop_count = 6 if round_idx < 2 else 5
            elif best_len >= 40:
                drop_count = 5 if round_idx < 2 else 4
            else:
                drop_count = 4 if round_idx < 2 else 3
            drop_count = max(2, min(drop_count, len(removable) - 1))

            pool_size = min(len(removable), max(drop_count + 4, 16))
            pool = [ci for _, _, ci in removable[:pool_size]]
            dropped = random.sample(pool, drop_count)
            dropped_set = set(dropped)

            work = [ci for ci in best_indices if ci not in dropped_set]
            work_set = set(work)
            counts_work = np.zeros(self.num_targets, dtype=np.int32)
            for ci in work:
                counts_work[cov_table[ci]] += 1

            target_limit = best_len - 1
            failed = False
            while True:
                uncov = np.flatnonzero(counts_work == 0)
                if len(uncov) == 0:
                    break
                if len(work) >= target_limit:
                    failed = True
                    break

                available = np.ones(self.num_cands, dtype=bool)
                if work_set:
                    available[np.fromiter(work_set, dtype=np.int32)] = False
                avail_idx = np.flatnonzero(available)
                if len(avail_idx) == 0:
                    failed = True
                    break

                cands = self.cand_masks[avail_idx]
                targets = self.target_masks[uncov]
                best_local, hit_cnt = self._batch_best(cands, targets)
                if hit_cnt <= 0:
                    failed = True
                    break
                add_ci = int(avail_idx[best_local])
                work.append(add_ci)
                work_set.add(add_ci)
                counts_work[cov_table[add_ci]] += 1

            if failed or len(work) >= best_len:
                continue

            candidate = [int(self.cand_masks[ci]) for ci in work]
            if not self._verify(candidate):
                continue

            best_indices = work
            best_len = len(best_indices)
            self._report(
                "optimize",
                f"N16 anchor {module_tag} light-exchange improved to {best_len} groups",
            )

            if best_len < 12:
                break

        return [int(self.cand_masks[ci]) for ci in best_indices]

    def _build_attempt_profiles(self, num_attempts: int) -> list[GreedyStrategy]:
        if self._cov_table is None:
            if self._is_large_j_equals_k_noncontainment():
                pool = [
                    GreedyStrategy(
                        name="coverage-topk",
                        destroy_repair_rounds=10,
                    ),
                    GreedyStrategy(
                        name="lns-heavy-a",
                        coverage_weight=0.86,
                        rarity_weight=0.68,
                        randomize=True,
                        noise_scale=1.0,
                        rcl_fraction=0.056,
                        rcl_min_count=6,
                        top_k_scale=2.1,
                        destroy_repair_rounds=18,
                    ),
                    GreedyStrategy(
                        name="lns-heavy-b",
                        coverage_weight=0.9,
                        rarity_weight=0.5,
                        randomize=True,
                        noise_scale=0.9,
                        rcl_fraction=0.1,
                        rcl_min_count=5,
                        top_k_scale=2.0,
                        destroy_repair_rounds=14,
                    ),
                    GreedyStrategy(
                        name="weighted-topk",
                        coverage_weight=1.0,
                        rarity_weight=0.55,
                        randomize=True,
                        noise_scale=0.65,
                        rcl_fraction=0.03,
                        rcl_min_count=3,
                        top_k_scale=1.25,
                        destroy_repair_rounds=6,
                    ),
                    GreedyStrategy(
                        name="explore-topk",
                        coverage_weight=0.95,
                        rarity_weight=0.35,
                        randomize=True,
                        noise_scale=0.9,
                        rcl_fraction=0.08,
                        rcl_min_count=5,
                        top_k_scale=1.5,
                        destroy_repair_rounds=8,
                    ),
                ]
            else:
                pool = [
                    GreedyStrategy(name="coverage-topk"),
                    GreedyStrategy(
                        name="weighted-topk",
                        coverage_weight=1.0,
                        rarity_weight=0.55,
                        randomize=True,
                        noise_scale=0.65,
                        rcl_fraction=0.03,
                        rcl_min_count=3,
                        top_k_scale=1.25,
                    ),
                    GreedyStrategy(
                        name="rarity-balance",
                        coverage_weight=0.9,
                        rarity_weight=0.45,
                        randomize=True,
                        noise_scale=0.75,
                        rcl_fraction=0.05,
                        rcl_min_count=4,
                        top_k_scale=1.35,
                        destroy_repair_rounds=1,
                    ),
                    GreedyStrategy(
                        name="repair-driven",
                        coverage_weight=0.85,
                        rarity_weight=0.55,
                        randomize=True,
                        noise_scale=0.8,
                        rcl_fraction=0.06,
                        rcl_min_count=4,
                        top_k_scale=1.2,
                        destroy_repair_rounds=2,
                    ),
                    GreedyStrategy(
                        name="explore-topk",
                        coverage_weight=0.95,
                        rarity_weight=0.35,
                        randomize=True,
                        noise_scale=0.9,
                        rcl_fraction=0.08,
                        rcl_min_count=5,
                        top_k_scale=1.5,
                        destroy_repair_rounds=1,
                    ),
                ]
        else:
            spread_tiebreak = self._enable_spread_tiebreak()
            if self._is_mid_j_equals_k_noncontainment():
                pool = [
                    GreedyStrategy(
                        name="coverage-first",
                        spread_tiebreak=spread_tiebreak,
                        spread_recent=32,
                        spread_pool_cap=640,
                        destroy_repair_rounds=2,
                    ),
                    GreedyStrategy(
                        name="coverage-soft-a",
                        coverage_weight=1.0,
                        rarity_weight=0.12,
                        randomize=True,
                        noise_scale=0.28,
                        rcl_fraction=0.015,
                        rcl_min_count=2,
                        top_k_scale=1.1,
                        spread_tiebreak=spread_tiebreak,
                        spread_recent=28,
                        spread_pool_cap=640,
                        destroy_repair_rounds=3,
                    ),
                    GreedyStrategy(
                        name="coverage-soft-c",
                        coverage_weight=0.98,
                        rarity_weight=0.2,
                        randomize=True,
                        noise_scale=0.55,
                        rcl_fraction=0.04,
                        rcl_min_count=3,
                        top_k_scale=1.2,
                        spread_tiebreak=spread_tiebreak,
                        spread_recent=24,
                        spread_pool_cap=720,
                        destroy_repair_rounds=2,
                    ),
                    GreedyStrategy(
                        name="coverage-soft-d",
                        coverage_weight=0.96,
                        rarity_weight=0.22,
                        randomize=True,
                        noise_scale=0.7,
                        rcl_fraction=0.05,
                        rcl_min_count=3,
                        top_k_scale=1.25,
                        spread_tiebreak=spread_tiebreak,
                        spread_recent=24,
                        spread_pool_cap=720,
                        destroy_repair_rounds=3,
                    ),
                    GreedyStrategy(
                        name="coverage-soft-e",
                        coverage_weight=0.94,
                        rarity_weight=0.28,
                        randomize=True,
                        noise_scale=0.82,
                        rcl_fraction=0.06,
                        rcl_min_count=4,
                        top_k_scale=1.3,
                        spread_tiebreak=spread_tiebreak,
                        spread_recent=20,
                        spread_pool_cap=768,
                        destroy_repair_rounds=3,
                    ),
                ]
            else:
                pool = [
                    GreedyStrategy(
                        name="coverage-first",
                        spread_tiebreak=spread_tiebreak,
                        spread_recent=32,
                        spread_pool_cap=640,
                    ),
                    GreedyStrategy(
                        name="rarity-balance",
                        coverage_weight=1.0,
                        rarity_weight=0.2,
                        randomize=True,
                        noise_scale=0.6,
                        rcl_fraction=0.03,
                        rcl_min_count=3,
                        destroy_repair_rounds=1,
                    ),
                    GreedyStrategy(
                        name="rarity-first",
                        coverage_weight=0.85,
                        rarity_weight=0.45,
                        randomize=True,
                        noise_scale=0.75,
                        rcl_fraction=0.05,
                        rcl_min_count=3,
                        destroy_repair_rounds=1,
                    ),
                    GreedyStrategy(
                        name="repair-driven",
                        coverage_weight=0.9,
                        rarity_weight=0.25,
                        randomize=True,
                        noise_scale=0.8,
                        rcl_fraction=0.06,
                        rcl_min_count=4,
                        destroy_repair_rounds=2,
                    ),
                    GreedyStrategy(
                        name="coverage-random",
                        coverage_weight=1.0,
                        rarity_weight=0.1,
                        randomize=True,
                        noise_scale=0.85,
                        rcl_fraction=0.07,
                        rcl_min_count=4,
                    ),
                ]
        return pool[:num_attempts]

    def _optimise_solution(
        self,
        sol: list[int],
        strategy: GreedyStrategy,
        *,
        best_len: int | None = None,
        stagnant: int = 0,
    ) -> list[int]:
        started_at = time.time()
        opt_budget = self._phase_c_opt_budget(sol)

        def _within_opt_budget() -> bool:
            if self._cancel():
                return False
            if opt_budget is None:
                return True
            return (time.time() - started_at) < opt_budget

        sol = self._local_search(sol)
        if not _within_opt_budget():
            return sol
        if self._n17_special_case_enabled and should_short_circuit_n17_tiny_legal_solution(self, sol):
            self._report(
                "optimize",
                f"Phase-N17 early-accept tiny legal solution ({len(sol)} groups)",
            )
            return sol

        heavy_allowed = self._phase_d_allow_heavy_operators(sol, best_len, stagnant)

        dr_rounds = strategy.destroy_repair_rounds + self._phase_c_extra_destroy_rounds(sol)
        if heavy_allowed and _within_opt_budget() and dr_rounds > 0:
            sol = self._destroy_repair(
                sol,
                strategy,
                rounds=dr_rounds,
            )
            sol = self._local_search(sol)
            if not _within_opt_budget():
                return sol

        if heavy_allowed and _within_opt_budget():
            sol = self._targeted_drop_one(sol, strategy)
            if not _within_opt_budget():
                return sol

        if heavy_allowed and _within_opt_budget() and self._allow_swap(sol):
            sol = self._swap_improve(sol)
            sol = self._local_search(sol)
            if not _within_opt_budget():
                return sol

        if heavy_allowed and _within_opt_budget() and 3 < len(sol) <= self._phase_c_sa_size_limit():
            sa_budget = self._sa_time_budget(sol)
            if sa_budget > 0:
                sol = self._sa_improve(sol, max_time=sa_budget)
            sol = self._local_search(sol)

        return sol

    def _allow_swap(self, sol: list[int]) -> bool:
        if len(sol) > 100:
            return False
        if self.num_cands > 45_000:
            return False
        if self.num_targets > 15_000:
            return False
        if self._interaction_scale <= 450_000_000:
            return True
        return self._phase_c_has_time(12.0)

    def _phase_c_has_time(self, minimum_sec: float) -> bool:
        remaining = self._time_remaining_sec()
        if remaining is None:
            return self._interaction_scale <= 180_000_000
        return remaining >= minimum_sec

    def _phase_c_sa_size_limit(self) -> int:
        if self._containment and self.num_targets >= 700:
            return 120
        if self._interaction_scale >= 600_000_000:
            return 110
        if self._interaction_scale >= 180_000_000:
            return 140
        return 200

    def _sa_time_budget(self, sol: list[int]) -> float:
        if len(sol) <= 3:
            return 0.0
        if len(sol) > self._phase_c_sa_size_limit():
            return 0.0
        if self._interaction_scale >= 900_000_000:
            base = 1.5
        elif self._interaction_scale >= 300_000_000 or self.num_cands >= 30_000:
            base = 2.0
        elif self.num_targets >= 3_000:
            base = 3.0
        elif self._interaction_scale >= 120_000_000:
            base = 4.0
        else:
            base = 8.0

        remaining = self._time_remaining_sec()
        if remaining is None:
            return base
        if remaining <= 1.0:
            return 0.0

        if self._interaction_scale <= 30_000_000:
            cap = 10.0
            ratio = 0.18
        elif self._interaction_scale <= 200_000_000:
            cap = 14.0
            ratio = 0.24
        else:
            cap = 12.0
            ratio = 0.20
        adaptive = min(cap, remaining * ratio)
        return max(0.0, min(cap, max(base, adaptive)))

    def _phase_c_opt_budget(self, sol: list[int]) -> float | None:
        remaining = self._time_remaining_sec()
        if remaining is None:
            return None
        if remaining <= 0.6:
            return 0.0
        if self._is_large_j_equals_k_noncontainment() and len(sol) >= 180:
            ratio = 0.45
            cap = 24.0
            return max(0.5, min(cap, remaining * ratio))
        if len(sol) <= 24:
            ratio = 0.14
            cap = 3.0
        elif len(sol) <= 120:
            ratio = 0.24
            cap = 8.0
        else:
            ratio = 0.30
            cap = 12.0
        return max(0.2, min(cap, remaining * ratio))

    def _phase_c_extra_destroy_rounds(self, sol: list[int]) -> int:
        remaining = self._time_remaining_sec()
        if remaining is None:
            return 0
        if self._is_large_j_equals_k_noncontainment() and len(sol) > 220:
            return 0
        if len(sol) > 220:
            if self._is_mid_j_equals_k_noncontainment():
                if remaining >= 30.0:
                    return 2
                if remaining >= 16.0:
                    return 1
            return 0
        if remaining >= 25.0:
            return 2
        if remaining >= 12.0:
            return 1
        return 0

    def _phase_d_allow_heavy_operators(
        self,
        sol: list[int],
        best_len: int | None,
        stagnant: int,
    ) -> bool:
        remaining = self._time_remaining_sec()
        if best_len is not None and len(sol) > best_len + max(2, best_len // 18):
            allow_relaxed = (
                self._is_large_j_equals_k_noncontainment()
                or self._is_mid_j_equals_k_noncontainment()
            )
            if not allow_relaxed:
                return False
            if remaining is None:
                if stagnant >= 2:
                    return False
            else:
                min_remaining = 14.0 if self._is_large_j_equals_k_noncontainment() else 12.0
                if remaining < min_remaining:
                    return False
        if stagnant <= 1:
            return True
        if remaining is None:
            return stagnant <= 2 and len(sol) <= 80
        if remaining < 8.0 and stagnant >= 2:
            return False
        return True

    # ------------------------------------------------------------------
    # Greedy dispatch
    # ------------------------------------------------------------------

    def _greedy(
        self,
        strategy: GreedyStrategy,
        *,
        partial: list[int] | None = None,
        best_limit: int | None = None,
    ) -> tuple[list[int], bool, int]:
        if self._cov_table is not None:
            return self._greedy_incremental(
                strategy,
                partial=partial,
                best_limit=best_limit,
            )
        return self._greedy_heuristic(
            strategy,
            partial=partial,
            best_limit=best_limit,
        )

    def _initial_greedy_state(
        self,
        partial: list[int] | None,
    ) -> tuple[list[int], set[int], np.ndarray, int]:
        selected = list(partial or [])
        chosen = set(selected)
        uncov = np.ones(self.num_targets, dtype=bool)
        for mask in selected:
            self._mark_covered(mask, uncov)
        return selected, chosen, uncov, int(uncov.sum())

    def _candidate_indices(self, masks) -> np.ndarray:
        indices = [
            self._cand_index_map[mask]
            for mask in masks
            if mask in self._cand_index_map
        ]
        if not indices:
            return np.empty(0, dtype=np.int32)
        return np.array(indices, dtype=np.int32)

    def _combine_candidate_scores(
        self,
        coverage_scores: np.ndarray,
        rarity_scores: np.ndarray,
        strategy: GreedyStrategy,
    ) -> np.ndarray:
        combined = (
            coverage_scores.astype(np.float64) * strategy.coverage_weight
            + rarity_scores * strategy.rarity_weight
        )
        if strategy.randomize:
            combined += np.random.random(len(combined)) * strategy.noise_scale
        return combined

    @staticmethod
    def _weighted_random_index(indices: np.ndarray, scores: np.ndarray) -> int:
        if len(indices) == 1:
            return int(indices[0])
        local_scores = scores[indices]
        min_val = float(np.min(local_scores))
        weights = (local_scores - min_val) + 1e-6
        weight_sum = float(np.sum(weights))
        if weight_sum <= 0:
            return int(indices[random.randrange(len(indices))])
        probs = weights / weight_sum
        picked = int(np.random.choice(len(indices), p=probs))
        return int(indices[picked])

    def _rcl_count(self, strategy: GreedyStrategy, available_count: int, remaining: int) -> int:
        if strategy.rcl_fraction <= 0 or available_count <= 1:
            return 1
        if remaining <= 200:
            rcl_cap = 96
        elif remaining <= 1_000:
            rcl_cap = 128
        elif remaining <= 5_000:
            rcl_cap = 160
        else:
            rcl_cap = 224
        raw_count = int(math.ceil(available_count * strategy.rcl_fraction))
        rcl_count = max(strategy.rcl_min_count, raw_count)
        return max(1, min(available_count, min(rcl_count, rcl_cap)))

    @staticmethod
    def _downsample_indices(indices: np.ndarray, cap: int) -> np.ndarray:
        if len(indices) <= cap:
            return indices
        step = len(indices) / float(cap)
        picked = (np.arange(cap) * step).astype(np.int32)
        return indices[picked]

    def _select_spread_tiebreak_index(
        self,
        candidates: np.ndarray,
        coverage_scores: np.ndarray,
        rarity_scores: np.ndarray,
        strategy: GreedyStrategy,
        selected: list[int],
    ) -> int | None:
        if len(candidates) == 0:
            return None
        pool = self._downsample_indices(candidates, max(32, strategy.spread_pool_cap))
        if len(pool) == 1:
            return int(pool[0])
        if not selected:
            return int(pool[0])

        recent = selected[-max(1, strategy.spread_recent) :]
        recent_arr = np.asarray(recent, dtype=np.uint32)
        pool_masks = self.cand_masks[pool]
        overlaps = popcount_uint32(pool_masks[:, None] & recent_arr[None, :]).sum(axis=1)

        min_overlap = int(np.min(overlaps))
        best_local = np.flatnonzero(overlaps == min_overlap)
        if len(best_local) > 1:
            rare_vals = rarity_scores[pool[best_local]]
            best_local = best_local[np.flatnonzero(rare_vals == np.max(rare_vals))]
        if len(best_local) > 1:
            cov_vals = coverage_scores[pool[best_local]]
            best_local = best_local[np.flatnonzero(cov_vals == np.max(cov_vals))]
        return int(pool[int(best_local[0])])

    def _select_incremental_with_spread_tiebreak(
        self,
        combined: np.ndarray,
        coverage_scores: np.ndarray,
        rarity_scores: np.ndarray,
        strategy: GreedyStrategy,
        selected: list[int],
    ) -> int | None:
        if not strategy.spread_tiebreak:
            return None
        valid = np.flatnonzero(coverage_scores > 0)
        if len(valid) <= 1:
            return None
        max_score = float(np.max(combined[valid]))
        eps = max(1e-9, abs(max_score) * 1e-12)
        top = valid[np.abs(combined[valid] - max_score) <= eps]
        if len(top) <= 1:
            return None
        return self._select_spread_tiebreak_index(
            top,
            coverage_scores,
            rarity_scores,
            strategy,
            selected,
        )

    def _select_from_combined_scores(
        self,
        combined: np.ndarray,
        coverage_scores: np.ndarray,
        strategy: GreedyStrategy,
        remaining: int,
    ) -> int:
        valid = np.flatnonzero(coverage_scores > 0)
        if len(valid) == 0:
            return int(np.argmax(combined))
        if not strategy.randomize or strategy.rcl_fraction <= 0:
            local_best = int(np.argmax(combined[valid]))
            return int(valid[local_best])

        rcl_count = self._rcl_count(strategy, len(valid), remaining)
        if rcl_count <= 1:
            local_best = int(np.argmax(combined[valid]))
            return int(valid[local_best])
        if rcl_count < len(valid):
            local_scores = combined[valid]
            top_local = np.argpartition(local_scores, -rcl_count)[-rcl_count:]
            rcl_idx = valid[top_local]
        else:
            rcl_idx = valid
        return self._weighted_random_index(rcl_idx, combined)

    def _select_incremental_index(
        self,
        coverage_scores: np.ndarray,
        rarity_scores: np.ndarray,
        strategy: GreedyStrategy,
        remaining: int,
        selected: list[int],
    ) -> int:
        combined = self._combine_candidate_scores(
            coverage_scores,
            rarity_scores,
            strategy,
        )
        spread_pick = self._select_incremental_with_spread_tiebreak(
            combined,
            coverage_scores,
            rarity_scores,
            strategy,
            selected,
        )
        if spread_pick is not None:
            return spread_pick
        return self._select_from_combined_scores(
            combined,
            coverage_scores,
            strategy,
            remaining,
        )

    def _incremental_scores_from_uncovered(
        self,
        uncov: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        inv_table = self._inv_table
        assert inv_table is not None

        coverage_scores = np.zeros(self.num_cands, dtype=np.int32)
        rarity_scores = np.zeros(self.num_cands, dtype=np.float64)

        for ti in np.flatnonzero(uncov):
            affected = inv_table[int(ti)]
            if len(affected) == 0:
                continue
            coverage_scores[affected] += 1
            rarity_scores[affected] += self._target_weights[int(ti)]

        return coverage_scores, rarity_scores

    def _greedy_incremental(
        self,
        strategy: GreedyStrategy,
        *,
        partial: list[int] | None = None,
        best_limit: int | None = None,
    ) -> tuple[list[int], bool, int]:
        cov_table = self._cov_table
        inv_table = self._inv_table
        assert cov_table is not None and inv_table is not None

        selected, chosen, uncov, rem = self._initial_greedy_state(partial)
        coverage_scores = np.array([len(c) for c in cov_table], dtype=np.int32)
        if self._base_weighted_scores is not None:
            rarity_scores = self._base_weighted_scores.copy()
        else:
            rarity_scores = coverage_scores.astype(np.float64)

        if selected:
            coverage_scores, rarity_scores = self._incremental_scores_from_uncovered(uncov)
            blocked = self._candidate_indices(chosen)
            if len(blocked) > 0:
                coverage_scores[blocked] = -1
                rarity_scores[blocked] = -1.0

        iteration = 0
        log_interval = max(1, self.num_targets // 500)

        while rem > 0:
            if self._cancel():
                break
            if best_limit is not None and len(selected) >= best_limit:
                break

            best_idx = self._select_incremental_index(
                coverage_scores,
                rarity_scores,
                strategy,
                rem,
                selected,
            )

            cnt = int(coverage_scores[best_idx])
            if cnt == 0:
                break

            mask = int(self.cand_masks[best_idx])
            selected.append(mask)
            chosen.add(mask)

            newly_covered = cov_table[best_idx][uncov[cov_table[best_idx]]]
            if len(newly_covered) == 0:
                break
            uncov[newly_covered] = False
            for ti in newly_covered:
                affected = inv_table[int(ti)]
                coverage_scores[affected] -= 1
                rarity_scores[affected] -= self._target_weights[int(ti)]
            coverage_scores[best_idx] = -1
            rarity_scores[best_idx] = -1.0

            iteration += 1
            rem -= len(newly_covered)
            if iteration % log_interval == 0 or rem == 0:
                self._report(
                    "greedy",
                    f"Iter {iteration}: +1 (covers {len(newly_covered)}), {rem} left",
                    iteration=iteration,
                    sol_size=len(selected),
                    remaining=rem,
                )
        return selected, rem == 0, rem

    def _greedy_heuristic(
        self,
        strategy: GreedyStrategy,
        *,
        partial: list[int] | None = None,
        best_limit: int | None = None,
    ) -> tuple[list[int], bool, int]:
        selected, chosen, uncov, rem = self._initial_greedy_state(partial)
        iteration = 0

        while rem > 0:
            if self._cancel():
                break
            if best_limit is not None and len(selected) >= best_limit:
                break
            if partial is None and self._should_finish_fast(rem):
                tail = self._fast_complete_selected(selected, uncov)
                if tail:
                    return tail, True, 0
                break
            mask, cnt = self._heuristic_pick(uncov, rem, strategy, chosen)
            if cnt == 0:
                break
            selected.append(mask)
            chosen.add(mask)
            self._mark_covered(mask, uncov)
            iteration += 1
            rem = int(uncov.sum())
            self._report(
                "greedy",
                f"Iter {iteration}: +1 (covers {cnt}), {rem} left",
                iteration=iteration,
                sol_size=len(selected),
                remaining=rem,
            )
        return selected, rem == 0, rem

    def _heuristic_pick(
        self,
        uncov: np.ndarray,
        remaining: int,
        strategy: GreedyStrategy,
        chosen: set[int],
    ) -> tuple[int, int]:
        cand_has = self._cand_has_elem
        target_has = self._target_has_elem
        assert cand_has is not None and target_has is not None

        uncov_weights = self._target_weights[uncov]
        if strategy.rarity_weight > 0:
            freq = target_has[uncov].T @ uncov_weights
        else:
            freq = target_has[uncov].sum(axis=0, dtype=np.int64)
        h = cand_has @ freq

        blocked = self._candidate_indices(chosen)
        available = np.ones(self.num_cands, dtype=bool)
        if len(blocked) > 0:
            available[blocked] = False

        top_k = self._strategy_top_k(remaining, strategy)
        available_idx = np.flatnonzero(available)
        if len(available_idx) == 0:
            return 0, 0
        if top_k < len(available_idx):
            local_h = h[available_idx]
            top_local = np.argpartition(local_h, -top_k)[-top_k:]
            top_idx = available_idx[top_local]
        else:
            top_idx = available_idx
        top_cands = self.cand_masks[top_idx]
        uncov_t = self.target_masks[uncov]

        if (
            strategy.coverage_weight == 1.0
            and strategy.rarity_weight == 0.0
            and not strategy.randomize
        ):
            best_local, best_count = self._batch_best(top_cands, uncov_t)
            return int(top_cands[best_local]), best_count

        raw_counts = self._batch_scores(top_cands, uncov_t)
        top_h = h[top_idx].astype(np.float64)
        scale = max(float(np.max(top_h)), 1.0)
        rarity_scores = top_h / scale
        combined = self._combine_candidate_scores(
            raw_counts,
            rarity_scores,
            strategy,
        )
        best_local = self._select_from_combined_scores(
            combined,
            raw_counts,
            strategy,
            remaining,
        )
        return int(top_cands[best_local]), int(raw_counts[best_local])

    # ------------------------------------------------------------------
    # Batch scoring
    # ------------------------------------------------------------------

    def _batch_scores(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> np.ndarray:
        if (
            self._gpu_enabled
            and not self._gpu_failed
            and len(cands) >= 256
            and len(targets) >= 1024
        ):
            try:
                return self._batch_scores_gpu(cands, targets)
            except Exception:
                self._gpu_failed = True
                self._report("gpu", "GPU path failed; falling back to CPU")
        return self._batch_scores_cpu(cands, targets)

    def _batch_best(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> tuple[int, int]:
        if (
            self._gpu_enabled
            and not self._gpu_failed
            and len(cands) >= 256
            and len(targets) >= 1024
        ):
            try:
                return self._batch_best_gpu(cands, targets)
            except Exception:
                self._gpu_failed = True
                self._report("gpu", "GPU path failed; falling back to CPU")
        return self._batch_best_cpu(cands, targets)

    def _batch_scores_cpu(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> np.ndarray:
        nc, nt = len(cands), len(targets)
        scores = np.zeros(nc, dtype=np.int32)
        bs = max(1, self._batch_bytes // max(1, nt * 12))
        bs = min(bs, nc)

        for i in range(0, nc, bs):
            if self._cancel():
                break
            batch = cands[i : i + bs]
            ints = batch[:, None] & targets[None, :]
            if self._containment:
                counts = np.sum(ints == targets[None, :], axis=1)
            else:
                counts = np.sum(popcount_uint32(ints) >= self.s, axis=1)
            scores[i : i + len(batch)] = counts
        return scores

    def _batch_best_cpu(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> tuple[int, int]:
        nc, nt = len(cands), len(targets)
        bs = max(1, self._batch_bytes // max(1, nt * 12))
        bs = min(bs, nc)
        best_local = 0
        best_count = -1

        for i in range(0, nc, bs):
            if self._cancel():
                break
            batch = cands[i : i + bs]
            ints = batch[:, None] & targets[None, :]
            if self._containment:
                counts = np.sum(ints == targets[None, :], axis=1)
            else:
                counts = np.sum(popcount_uint32(ints) >= self.s, axis=1)
            batch_best = int(np.argmax(counts))
            batch_count = int(counts[batch_best])
            if batch_count > best_count:
                best_count = batch_count
                best_local = i + batch_best

        return best_local, max(0, best_count)

    def _batch_scores_gpu(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> np.ndarray:
        assert cp is not None
        cands_gpu = cp.asarray(cands, dtype=cp.uint32)
        targets_gpu = cp.asarray(targets, dtype=cp.uint32)
        scores_gpu = cp.zeros(len(cands), dtype=cp.int32)

        _, total_mem = cp.cuda.Device().mem_info
        approx_bytes_per_target = max(4, len(cands) * 12)
        chunk = int(max(2048, min(
            len(targets),
            (total_mem * 0.45) // approx_bytes_per_target
        )))

        for start in range(0, len(targets), chunk):
            if self._cancel():
                break
            t_chunk = targets_gpu[start : start + chunk]
            ints = cands_gpu[:, None] & t_chunk[None, :]
            if self._containment:
                hits = ints == t_chunk[None, :]
            else:
                x = cp.array(ints, dtype=cp.uint32, copy=True)
                t = (x >> cp.uint32(1)) & cp.uint32(0x55555555)
                x = x - t
                t = x & cp.uint32(0x33333333)
                x = (x >> cp.uint32(2)) & cp.uint32(0x33333333)
                x = x + t
                x = x + (x >> cp.uint32(4))
                x = x & cp.uint32(0x0F0F0F0F)
                x = x * cp.uint32(0x01010101)
                x = x >> cp.uint32(24)
                hits = x.astype(cp.int32) >= self.s
            scores_gpu += cp.sum(hits, axis=1, dtype=cp.int32)
        return cp.asnumpy(scores_gpu)

    def _batch_best_gpu(
        self, cands: np.ndarray, targets: np.ndarray,
    ) -> tuple[int, int]:
        assert cp is not None
        cands_gpu = cp.asarray(cands, dtype=cp.uint32)
        targets_gpu = cp.asarray(targets, dtype=cp.uint32)
        scores_gpu = cp.zeros(len(cands), dtype=cp.int32)

        _, total_mem = cp.cuda.Device().mem_info
        approx_bytes_per_target = max(4, len(cands) * 12)
        chunk = int(max(2048, min(
            len(targets),
            (total_mem * 0.45) // approx_bytes_per_target
        )))

        for start in range(0, len(targets), chunk):
            if self._cancel():
                break
            t_chunk = targets_gpu[start : start + chunk]
            ints = cands_gpu[:, None] & t_chunk[None, :]
            if self._containment:
                hits = ints == t_chunk[None, :]
            else:
                x = cp.array(ints, dtype=cp.uint32, copy=True)
                t = (x >> cp.uint32(1)) & cp.uint32(0x55555555)
                x = x - t
                t = x & cp.uint32(0x33333333)
                x = (x >> cp.uint32(2)) & cp.uint32(0x33333333)
                x = x + t
                x = x + (x >> cp.uint32(4))
                x = x & cp.uint32(0x0F0F0F0F)
                x = x * cp.uint32(0x01010101)
                x = x >> cp.uint32(24)
                hits = x.astype(cp.int32) >= self.s
            scores_gpu += cp.sum(hits, axis=1, dtype=cp.int32)

        best_local = int(cp.argmax(scores_gpu).get())
        best_count = int(scores_gpu[best_local].get())
        return best_local, best_count

    def _gpu_hits(self, masks_gpu, targets_gpu):
        assert cp is not None
        ints = masks_gpu[:, None] & targets_gpu[None, :]
        if self._containment:
            return ints == targets_gpu[None, :]
        return self._gpu_popcount_uint32(ints) >= self.s

    @staticmethod
    def _gpu_popcount_uint32(arr):
        assert cp is not None
        x = cp.array(arr, dtype=cp.uint32, copy=True)
        t = (x >> cp.uint32(1)) & cp.uint32(0x55555555)
        x = x - t
        t = x & cp.uint32(0x33333333)
        x = (x >> cp.uint32(2)) & cp.uint32(0x33333333)
        x = x + t
        x = x + (x >> cp.uint32(4))
        x = x & cp.uint32(0x0F0F0F0F)
        x = x * cp.uint32(0x01010101)
        x = x >> cp.uint32(24)
        return x.astype(cp.int32)

    def _eval_one(self, mask: int, targets: np.ndarray) -> int:
        ints = np.uint32(mask) & targets
        if self._containment:
            return int(np.sum(ints == targets))
        return int(np.sum(popcount_uint32(ints) >= self.s))

    # ------------------------------------------------------------------
    # Coverage helpers
    # ------------------------------------------------------------------

    def _mark_covered(self, mask: int, uncovered: np.ndarray) -> None:
        ints = np.uint32(mask) & self.target_masks
        if self._containment:
            covered = ints == self.target_masks
        else:
            covered = popcount_uint32(ints) >= self.s
        uncovered &= ~covered

    def _verify(self, masks: list[int]) -> bool:
        if not masks:
            return self.num_targets == 0
        if (
            self._gpu_active()
            and self.num_targets >= 2048
            and len(masks) * self.num_targets >= 4_000_000
        ):
            try:
                return self._verify_gpu(masks)
            except Exception:
                self._gpu_disable("GPU verification failed; falling back to CPU")
        covered = np.zeros(self.num_targets, dtype=bool)
        for m in masks:
            ints = np.uint32(m) & self.target_masks
            if self._containment:
                covered |= ints == self.target_masks
            else:
                covered |= popcount_uint32(ints) >= self.s
        return bool(np.all(covered))

    def _uncovered_masks(self, masks: list[int]) -> np.ndarray:
        if (
            self._gpu_active()
            and self.num_targets >= 2048
            and masks
            and len(masks) * self.num_targets >= 4_000_000
        ):
            try:
                return self._uncovered_masks_gpu(masks)
            except Exception:
                self._gpu_disable("GPU uncovered-mask scan failed; falling back to CPU")
        covered = np.zeros(self.num_targets, dtype=bool)
        for m in masks:
            ints = np.uint32(m) & self.target_masks
            if self._containment:
                covered |= ints == self.target_masks
            else:
                covered |= popcount_uint32(ints) >= self.s
        return self.target_masks[~covered]

    def _mark_covered_gpu(self, mask: int, uncovered: np.ndarray) -> None:
        assert cp is not None
        self._ensure_gpu_mask_cache()
        assert self._target_masks_gpu is not None
        mask_gpu = cp.asarray([mask], dtype=cp.uint32)
        covered = cp.asnumpy(self._gpu_hits(mask_gpu, self._target_masks_gpu)[0])
        uncovered &= ~covered

    def _verify_gpu(self, masks: list[int]) -> bool:
        assert cp is not None
        self._ensure_gpu_mask_cache()
        assert self._target_masks_gpu is not None
        masks_arr = np.asarray(masks, dtype=np.uint32)
        masks_gpu = cp.asarray(masks_arr, dtype=cp.uint32)
        covered_gpu = cp.zeros(self.num_targets, dtype=cp.bool_)
        chunk = self._gpu_mask_chunk(self.num_targets, len(masks_arr))

        for start in range(0, len(masks_arr), chunk):
            if self._cancel():
                break
            chunk_gpu = masks_gpu[start : start + chunk]
            hits = self._gpu_hits(chunk_gpu, self._target_masks_gpu)
            covered_gpu |= cp.sum(hits, axis=0, dtype=cp.int32) > 0
            if int(cp.sum(covered_gpu, dtype=cp.int32).get()) == self.num_targets:
                return True
        return int(cp.sum(covered_gpu, dtype=cp.int32).get()) == self.num_targets

    def _uncovered_masks_gpu(self, masks: list[int]) -> np.ndarray:
        assert cp is not None
        self._ensure_gpu_mask_cache()
        assert self._target_masks_gpu is not None
        masks_arr = np.asarray(masks, dtype=np.uint32)
        masks_gpu = cp.asarray(masks_arr, dtype=cp.uint32)
        covered_gpu = cp.zeros(self.num_targets, dtype=cp.bool_)
        chunk = self._gpu_mask_chunk(self.num_targets, len(masks_arr))

        for start in range(0, len(masks_arr), chunk):
            if self._cancel():
                break
            chunk_gpu = masks_gpu[start : start + chunk]
            hits = self._gpu_hits(chunk_gpu, self._target_masks_gpu)
            covered_gpu |= cp.sum(hits, axis=0, dtype=cp.int32) > 0
        return cp.asnumpy(self._target_masks_gpu[~covered_gpu])

    # ------------------------------------------------------------------
    # Local search
    # ------------------------------------------------------------------

    def _local_search(self, sol: list[int]) -> list[int]:
        if len(sol) <= 60:
            return self._local_search_brute(sol)
        return self._local_search_fast(sol)

    def _local_search_brute(self, sol: list[int]) -> list[int]:
        improved = True
        while improved and not self._cancel():
            improved = False
            for i in range(len(sol)):
                rest = sol[:i] + sol[i + 1:]
                if self._verify(rest):
                    sol = rest
                    improved = True
                    self._report("optimize", f"Removed redundant -> {len(sol)} groups")
                    break
        return sol

    def _local_search_fast(self, sol: list[int]) -> list[int]:
        cov_count = np.zeros(self.num_targets, dtype=np.int32)
        sol_cov: list[np.ndarray] = []
        for m in sol:
            c = self._covers_bool(m)
            sol_cov.append(c)
            cov_count += c.astype(np.int32)

        improved = True
        while improved and not self._cancel():
            improved = False
            for i in range(len(sol) - 1, -1, -1):
                c = sol_cov[i]
                if np.all(cov_count[c] >= 2):
                    cov_count -= c.astype(np.int32)
                    sol.pop(i)
                    sol_cov.pop(i)
                    improved = True
                    self._report("optimize", f"Removed redundant -> {len(sol)} groups")
        return sol

    def _covers_bool(self, mask: int) -> np.ndarray:
        ints = np.uint32(mask) & self.target_masks
        if self._containment:
            return ints == self.target_masks
        return popcount_uint32(ints) >= self.s

    def _allow_destroy_repair(self, sol: list[int]) -> bool:
        if len(sol) < 8:
            return False
        allow_long = self._is_large_j_equals_k_noncontainment() or self._is_mid_j_equals_k_noncontainment()
        if len(sol) > 260 and not allow_long:
            return False
        if self.num_cands > 45_000 and not self._is_large_j_equals_k_noncontainment():
            return False
        if self._interaction_scale <= 180_000_000:
            return True
        if self._interaction_scale <= 900_000_000:
            return self._phase_c_has_time(10.0)
        return self._phase_c_has_time(18.0)

    def _targeted_drop_one(self, sol: list[int], strategy: GreedyStrategy) -> list[int]:
        if not self._is_mid_j_equals_k_noncontainment():
            return sol
        if self._cov_table is None:
            return sol
        min_len = 12 if (self.n < 16 and self.j == self.k and not self._containment) else 24
        if len(sol) < min_len:
            return sol
        if not self._phase_c_has_time(6.0):
            return sol

        order = self._destroy_repair_order(sol)
        if not order:
            return sol

        max_trials = 24 if len(sol) >= 180 else 18
        if len(order) > max_trials:
            head = order[: max_trials // 2]
            tail_pool = order[max_trials // 2 :]
            extra_need = max_trials - len(head)
            if extra_need > 0 and len(tail_pool) > extra_need:
                head.extend(random.sample(tail_pool, extra_need))
            order = head

        repair_strategy = strategy
        if not repair_strategy.randomize:
            repair_strategy = replace(
                repair_strategy,
                randomize=True,
                noise_scale=max(0.45, repair_strategy.noise_scale),
                rcl_fraction=max(0.04, repair_strategy.rcl_fraction),
                rcl_min_count=max(3, repair_strategy.rcl_min_count),
                rarity_weight=max(0.2, repair_strategy.rarity_weight),
                top_k_scale=max(1.15, repair_strategy.top_k_scale),
            )

        target_limit = len(sol) - 1
        for remove_idx in order:
            if self._cancel():
                break
            partial = [m for idx, m in enumerate(sol) if idx != remove_idx]
            repaired, complete, _ = self._greedy(
                repair_strategy,
                partial=partial,
                best_limit=target_limit,
            )
            if not complete:
                fallback = self._fast_complete_partial_solution(
                    partial,
                    best_limit=target_limit,
                )
                if fallback is None:
                    continue
                repaired = fallback
            if len(repaired) > target_limit:
                continue
            candidate = self._local_search(repaired)
            if len(candidate) < len(sol):
                self._report(
                    "optimize",
                    f"Targeted drop improved to {len(candidate)} groups",
                )
                return candidate

        return sol

    def _phase_e_mid_compact_search(self, sol: list[int]) -> list[int]:
        if not self._is_mid_j_equals_k_noncontainment():
            return sol
        if self.num_targets > 12_000:
            return sol
        if self._cov_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        min_len = 12 if (self.n < 16 and self.j == self.k and not self._containment) else 24
        if len(sol) < min_len:
            return sol
        if not self._phase_c_has_time(8.0):
            return sol

        best = list(sol)
        best_len = len(best)
        no_improve = 0
        max_rounds = 120 if best_len >= 200 else 80
        rounds = 0

        strategy = GreedyStrategy(
            name="mid-compact",
            coverage_weight=0.95,
            rarity_weight=0.42,
            randomize=True,
            noise_scale=0.95,
            rcl_fraction=0.08,
            rcl_min_count=5,
            top_k_scale=1.65,
        )

        while rounds < max_rounds and not self._cancel():
            remaining = self._time_remaining_sec()
            if remaining is not None and remaining < 1.2:
                break
            if no_improve >= 18 and remaining is not None and remaining < 10.0:
                break

            order = self._destroy_repair_order(best)
            if not order:
                break

            if best_len >= 220:
                remove_count = random.randint(7, 14)
            elif best_len >= 90:
                remove_count = random.randint(4, 9)
            else:
                remove_count = random.randint(3, 6)
            remove_count = min(remove_count, max(2, best_len - 2))

            remove_set = self._destroy_repair_remove_set(
                order,
                remove_count,
                len(best),
                mixed=True,
            )
            partial = [
                mask for idx, mask in enumerate(best)
                if idx not in remove_set
            ]

            target_limit = best_len - 1
            repaired, complete, _ = self._greedy(
                strategy,
                partial=partial,
                best_limit=target_limit,
            )
            if not complete:
                rounds += 1
                no_improve += 1
                continue
            if len(repaired) > target_limit:
                rounds += 1
                no_improve += 1
                continue

            candidate = self._local_search(repaired)
            rounds += 1
            if len(candidate) < best_len:
                best = candidate
                best_len = len(candidate)
                no_improve = 0
                self._report(
                    "optimize",
                    f"Phase-E compact improved to {best_len} groups",
                )
            else:
                no_improve += 1

        return best

    def _phase_f_mid_cp_sat_refine(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if not self._is_mid_j_equals_k_noncontainment():
            return sol
        if self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        min_len = 10 if (self.n < 16 and self.j == self.k and not self._containment) else 16
        if len(sol) < min_len:
            return sol

        remaining = self._time_remaining_sec()
        if remaining is None or remaining < 4.0:
            return sol

        if self.num_targets > 10_000:
            return self._phase_f_mid_cp_sat_neighborhood(sol)

        cand_index = self._cand_index_map
        selected_indices = [cand_index[m] for m in sol if m in cand_index]
        if len(selected_indices) != len(sol):
            return sol

        best_masks = list(sol)
        best_len = len(best_masks)
        upper_bound = best_len - 1

        while upper_bound >= 1:
            remaining = self._time_remaining_sec()
            if remaining is None or remaining < 2.0:
                break

            model = cp_model.CpModel()
            vars_x = [model.NewBoolVar(f"x_{i}") for i in range(self.num_cands)]
            objective = sum(vars_x)
            model.Add(objective <= upper_bound)
            for covering in self._inv_table:
                model.AddBoolOr([vars_x[int(ci)] for ci in covering])
            model.Minimize(objective)

            for idx in selected_indices:
                model.AddHint(vars_x[idx], 1)

            solver = cp_model.CpSolver()
            iter_cap = 8.0 if (self.n < 16 and self.j == self.k and not self._containment) else 20.0
            solver.parameters.max_time_in_seconds = float(min(iter_cap, max(1.5, remaining - 0.8)))
            solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            solver.parameters.random_seed = 1
            status = solver.Solve(model)

            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                break

            picked = [i for i in range(self.num_cands) if solver.Value(vars_x[i]) == 1]
            if len(picked) >= best_len:
                break

            candidate = [int(self.cand_masks[i]) for i in picked]
            if not self._verify(candidate):
                break

            best_masks = candidate
            best_len = len(best_masks)
            selected_indices = picked
            upper_bound = best_len - 1
            self._report(
                "optimize",
                f"CP-SAT refined to {best_len} groups",
            )

        return best_masks

    def _phase_f_small_cp_sat_polish(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) <= 10:
            return sol
        if self.num_cands > 1_400 or self.num_targets > 2_000:
            return sol

        remaining = self._time_remaining_sec()
        if remaining is None or remaining < 2.0:
            return sol

        cand_index = self._cand_index_map
        selected_indices = [cand_index[m] for m in sol if m in cand_index]
        if len(selected_indices) != len(sol):
            return sol

        model = cp_model.CpModel()
        vars_x = [model.NewBoolVar(f"xs_{i}") for i in range(self.num_cands)]
        model.Add(sum(vars_x) <= len(sol))
        for covering in self._inv_table:
            model.AddBoolOr([vars_x[int(ci)] for ci in covering])
        model.Minimize(sum(vars_x))

        for idx in selected_indices:
            model.AddHint(vars_x[idx], 1)

        # N=12 optimization: aggressive time reduction (10% error tolerance)
        # Exception: L_12_6_4_3 uses original algorithm (small solution sensitive)
        # N=13 optimization: only L_13_6_5_5 (j≠k case: cap=2.0-4.0)
        # N=14 optimization: classified by difficulty
        if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
            if self.num_cands <= 320:
                cap = 2.0
            elif self.num_cands <= 1_000:
                cap = 4.0
            else:
                cap = 4.0
        elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
            if self.num_cands <= 320:
                cap = 2.0
            elif self.num_cands <= 1_000:
                cap = 4.0
            else:
                cap = 4.0
        elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
            # N=14 except L_14_7_7_6: moderate time budget
            if self.num_cands <= 320:
                cap = 3.0
            elif self.num_cands <= 1_000:
                cap = 5.0
            else:
                cap = 5.0
        else:
            if self.num_cands <= 320:
                cap = 6.0
            elif self.num_cands <= 1_000:
                cap = 20.0 if self._containment else 14.0
            else:
                cap = 18.0
        max_time = float(min(cap, max(1.0, remaining - 0.8)))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = max_time
        solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
        solver.parameters.random_seed = 1
        status = solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return sol

        picked = [i for i in range(self.num_cands) if solver.Value(vars_x[i]) == 1]
        if len(picked) >= len(sol):
            return sol

        candidate = [int(self.cand_masks[i]) for i in picked]
        if not self._verify(candidate):
            return sol

        self._report(
            "optimize",
            f"CP-SAT small-polish refined to {len(candidate)} groups",
        )
        return candidate

    def _phase_f_mid_cp_sat_neighborhood(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if self._inv_table is None:
            return sol
        if self._base_weighted_scores is None:
            return sol
        remaining = self._time_remaining_sec()
        if remaining is None or remaining < 8.0:
            return sol

        cand_index = self._cand_index_map
        selected_indices = [cand_index[m] for m in sol if m in cand_index]
        if len(selected_indices) != len(sol):
            return sol

        best_masks = list(sol)
        best_len = len(best_masks)
        target_ub = best_len - 1
        if target_ub < 1:
            return sol

        if self.num_targets <= 25_000:
            extras_cap = 2_400
        else:
            extras_cap = 2_000 if remaining >= 18.0 else 1_400
        selected_set = set(selected_indices)
        ranked = np.argsort(self._base_weighted_scores)[::-1]
        neighborhood = list(selected_indices)
        for ci in ranked:
            cii = int(ci)
            if cii in selected_set:
                continue
            neighborhood.append(cii)
            if len(neighborhood) >= len(selected_indices) + extras_cap:
                break

        local_pos = {ci: idx for idx, ci in enumerate(neighborhood)}
        model = cp_model.CpModel()
        vars_x = [model.NewBoolVar(f"x_{i}") for i in range(len(neighborhood))]
        objective = sum(vars_x)
        model.Add(objective <= target_ub)
        for covering in self._inv_table:
            loc = [local_pos[int(ci)] for ci in covering if int(ci) in local_pos]
            if not loc:
                continue
            model.AddBoolOr([vars_x[i] for i in loc])
        model.Minimize(objective)
        for ci in selected_indices:
            model.AddHint(vars_x[local_pos[ci]], 1)

        rem_after_build = self._time_remaining_sec()
        if rem_after_build is None or rem_after_build < 3.0:
            return sol

        total_budget = float(min(14.0, max(4.0, rem_after_build - 2.0)))
        seeds = [1, 17] if rem_after_build >= 24.0 else [1]
        self._report(
            "optimize",
            (
                f"CP-SAT neighborhood try: vars={len(neighborhood)}, "
                f"ub={target_ub}, budget={total_budget:.1f}s"
            ),
        )
        per_run = max(3.0, total_budget / len(seeds))
        for seed in seeds:
            run_remaining = self._time_remaining_sec()
            if run_remaining is None or run_remaining < 2.0:
                break
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = float(min(per_run, max(1.5, run_remaining - 1.0)))
            solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            solver.parameters.random_seed = seed
            status = solver.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                continue

            picked_local = [i for i in range(len(neighborhood)) if solver.Value(vars_x[i]) == 1]
            if len(picked_local) >= best_len:
                continue
            picked_global = [neighborhood[i] for i in picked_local]
            candidate = [int(self.cand_masks[i]) for i in picked_global]
            if not self._verify(candidate):
                continue
            self._report(
                "optimize",
                f"CP-SAT neighborhood refined to {len(candidate)} groups",
            )
            return candidate
        return sol

    def _phase_g_nlt16_fixed_size_polish(self, sol: list[int]) -> list[int]:
        if self.n > 16:
            return sol
        if self.n == 16 and not self._is_n16_hard_cluster():
            return sol
        if self._cov_table is None or self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 6:
            return sol

        best = list(sol)
        miss_count = 0
        while True:
            remaining = self._time_remaining_sec()
            if remaining is None or remaining < 3.0:
                break
            target_len = len(best) - 1
            if target_len < 1:
                break

            # Keep each round bounded so we can try multiple target lengths.
            hard_case = (
                (self.j == self.k and not self._containment)
                or (self._containment and self.k >= 6)
            )
            ratio = 0.30 if hard_case else 0.22
            cap = 28.0 if hard_case else 18.0
            round_budget = float(min(cap, max(4.0, remaining * ratio)))

            start_masks = list(best)
            if miss_count > 0:
                random.shuffle(start_masks)
            improved = self._phase_g_try_target_len(start_masks, target_len, round_budget)
            if improved is None:
                miss_count += 1
                if remaining < 8.0 or miss_count >= 4:
                    break
                continue
            miss_count = 0
            best = improved
            self._report(
                "optimize",
                f"Phase-G fixed-size improved to {len(best)} groups",
            )
        return best

    def _phase_g_try_target_len(
        self,
        start_masks: list[int],
        target_len: int,
        budget_sec: float,
    ) -> list[int] | None:
        cov_table = self._cov_table
        inv_table = self._inv_table
        assert cov_table is not None and inv_table is not None

        cand_index = self._cand_index_map
        start_idx = [cand_index[m] for m in start_masks if m in cand_index]
        if len(start_idx) != len(start_masks):
            return None
        if len(start_idx) <= target_len:
            return None

        def _coverage_counts(selected_idx: list[int]) -> np.ndarray:
            counts = np.zeros(self.num_targets, dtype=np.int32)
            for ci in selected_idx:
                counts[cov_table[ci]] += 1
            return counts

        def _trim_to_target(selected_idx: list[int]) -> tuple[list[int], np.ndarray]:
            work = list(selected_idx)
            counts = _coverage_counts(work)
            while len(work) > target_len:
                best_pos = 0
                best_score: tuple[int, int] | None = None
                for pos, ci in enumerate(work):
                    covered = cov_table[ci]
                    unique_loss = int(np.sum(counts[covered] == 1))
                    score = (unique_loss, len(covered))
                    if best_score is None or score < best_score:
                        best_score = score
                        best_pos = pos
                removed = work.pop(best_pos)
                counts[cov_table[removed]] -= 1
            return work, counts

        deadline = time.time() + max(0.1, budget_sec)
        base_sel, base_counts = _trim_to_target(start_idx)
        if int(np.sum(base_counts == 0)) == 0:
            candidate = [int(self.cand_masks[ci]) for ci in base_sel]
            if self._verify(candidate):
                return candidate

        max_restarts = 20 if target_len >= 80 else 14
        max_steps = 2600 if target_len >= 80 else 1600
        if target_len < 20:
            max_restarts = 64
            max_steps = 5400
            top_k = 80 if self.num_cands >= 2000 else 56
            sample_size = 12
        elif target_len < 40:
            max_restarts = 42
            max_steps = 4200
            top_k = 104 if self.num_cands >= 2000 else 72
            sample_size = 16
        elif target_len >= 150:
            max_restarts = max(max_restarts, 28)
            max_steps = max(max_steps, 3200)
            top_k = 192
            sample_size = 36
        elif target_len >= 80:
            top_k = 144 if self.num_cands >= 2000 else 96
            sample_size = 30
        else:
            top_k = 96 if self.num_cands >= 2000 else 64
            sample_size = 20
        weight = self._target_weights
        dynamic_weight = weight.astype(np.float64, copy=True)

        for restart in range(max_restarts):
            if time.time() >= deadline or self._cancel():
                break
            selected = list(base_sel)
            counts = base_counts.copy()
            selected_set = set(selected)

            # Diversify each restart with a few random swaps.
            perturb = min(4, max(1, target_len // 35))
            for _ in range(perturb):
                if time.time() >= deadline:
                    break
                drop_pos = random.randrange(len(selected))
                dropped = selected.pop(drop_pos)
                selected_set.remove(dropped)
                counts[cov_table[dropped]] -= 1

                uncovered = np.flatnonzero(counts == 0)
                if len(uncovered) == 0:
                    selected.append(dropped)
                    selected_set.add(dropped)
                    counts[cov_table[dropped]] += 1
                    continue

                scores = np.zeros(self.num_cands, dtype=np.float64)
                for ti in uncovered:
                    scores[inv_table[int(ti)]] += float(dynamic_weight[int(ti)])
                if selected_set:
                    scores[list(selected_set)] = -1e18
                if np.max(scores) <= 0:
                    add_ci = dropped
                else:
                    k = min(top_k, self.num_cands)
                    top = np.argpartition(scores, -k)[-k:]
                    top = top[scores[top] > 0]
                    if len(top) == 0:
                        add_ci = int(np.argmax(scores))
                    else:
                        add_ci = int(random.choice(top.tolist()))
                selected.append(add_ci)
                selected_set.add(add_ci)
                counts[cov_table[add_ci]] += 1

            unc = int(np.sum(counts == 0))
            best_unc = unc
            no_improve = 0
            tabu_drop_until: dict[int, int] = {}
            tabu_add_until: dict[int, int] = {}
            tabu_tenure = 9 if target_len >= 80 else 7

            for iter_idx in range(max_steps):
                if time.time() >= deadline or self._cancel():
                    break
                if unc == 0:
                    candidate = [int(self.cand_masks[ci]) for ci in selected]
                    if self._verify(candidate):
                        return candidate
                    break

                pick_n = min(sample_size, len(selected))
                sampled_pos = random.sample(range(len(selected)), pick_n)
                drop_pos = sampled_pos[0]
                drop_score: float | None = None
                for pos in sampled_pos:
                    ci = selected[pos]
                    tabu_until = tabu_drop_until.get(ci)
                    if tabu_until is not None and tabu_until > iter_idx:
                        continue
                    covered = cov_table[ci]
                    unique_loss = int(np.sum(counts[covered] == 1))
                    score = float(unique_loss) + random.random() * 2.0
                    if drop_score is None or score < drop_score:
                        drop_score = score
                        drop_pos = pos

                dropped = selected.pop(drop_pos)
                selected_set.remove(dropped)
                counts[cov_table[dropped]] -= 1

                uncovered = np.flatnonzero(counts == 0)
                scores = np.zeros(self.num_cands, dtype=np.float64)
                for ti in uncovered:
                    scores[inv_table[int(ti)]] += float(dynamic_weight[int(ti)])
                if selected_set:
                    scores[list(selected_set)] = -1e18

                if np.max(scores) <= 0:
                    add_ci = dropped
                else:
                    k = min(top_k, self.num_cands)
                    top = np.argpartition(scores, -k)[-k:]
                    top = top[scores[top] > 0]
                    if len(top) == 0:
                        add_ci = int(np.argmax(scores))
                    else:
                        ordered = top[np.argsort(scores[top])[::-1]]
                        add_ci = int(ordered[0])
                        for cand in ordered[:24]:
                            cand_i = int(cand)
                            tabu_until = tabu_add_until.get(cand_i)
                            if tabu_until is None or tabu_until <= iter_idx:
                                add_ci = cand_i
                                break
                        if random.random() >= 0.78:
                            sample_pool = [int(x) for x in ordered[: max(3, min(12, len(ordered)))]]
                            random.shuffle(sample_pool)
                            for cand_i in sample_pool:
                                tabu_until = tabu_add_until.get(cand_i)
                                if tabu_until is None or tabu_until <= iter_idx:
                                    add_ci = cand_i
                                    break

                selected.append(add_ci)
                selected_set.add(add_ci)
                counts[cov_table[add_ci]] += 1
                tabu_drop_until[dropped] = iter_idx + tabu_tenure
                tabu_add_until[add_ci] = iter_idx + tabu_tenure

                new_unc = int(np.sum(counts == 0))
                if new_unc < best_unc:
                    best_unc = new_unc
                    no_improve = 0
                    dynamic_weight = np.maximum(weight, dynamic_weight * 0.92)
                else:
                    no_improve += 1
                    if (iter_idx + 1) % 32 == 0:
                        unc_idx = np.flatnonzero(counts == 0)
                        if len(unc_idx) > 0:
                            dynamic_weight[unc_idx] = np.minimum(
                                dynamic_weight[unc_idx] * 1.08,
                                weight[unc_idx] * 6.0,
                            )
                unc = new_unc

                if no_improve >= 240:
                    break

        return None

    def _phase_h_ranked_candidates(
        self,
        selected_indices: list[int],
        base_scores: np.ndarray,
    ) -> np.ndarray:
        ranked_scores = np.asarray(base_scores, dtype=np.float64)
        if self._cov_table is None or self._inv_table is None:
            return np.argsort(ranked_scores)[::-1]

        counts = np.zeros(self.num_targets, dtype=np.int32)
        for ci in selected_indices:
            counts[self._cov_table[ci]] += 1

        fragile_idx = np.flatnonzero(counts <= 2)
        if len(fragile_idx) == 0:
            return np.argsort(ranked_scores)[::-1]

        # Bound accumulation cost for very wide fragile sets.
        if len(fragile_idx) > 2_600:
            frag_score = (
                (3.0 - np.minimum(counts[fragile_idx], 2.0))
                * self._target_weights[fragile_idx]
            )
            keep = np.argpartition(frag_score, -2_600)[-2_600:]
            fragile_idx = fragile_idx[keep]

        bonus = np.zeros(self.num_cands, dtype=np.float64)
        for ti in fragile_idx:
            coverers = self._inv_table[int(ti)]
            if len(coverers) == 0:
                continue
            support = counts[int(ti)]
            mult = 4.0 if support <= 1 else 1.8
            bonus[coverers] += float(self._target_weights[int(ti)] * mult)

        return np.argsort(ranked_scores + bonus)[::-1]

    def _phase_h_budget_cap_sec(self, *, remaining_sec: float, current_len: int) -> float:
        if remaining_sec <= 1.2:
            return 0.0

        # N=12 optimization: aggressive time reduction (10% error tolerance)
        # Exception: L_12_6_4_3 uses original algorithm (small solution sensitive)
        # N=13 optimization: only L_13_6_5_5 (j≠k case: frac=0.06, cap=3.0)
        # N=14 optimization: classified by difficulty
        if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
            if self._containment:
                frac = 0.08
                cap = 4.0
                floor = 1.5
            elif self.j == self.k:
                frac = 0.08
                cap = 3.5
                floor = 1.5
            else:
                frac = 0.06
                cap = 3.0
                floor = 1.0
            budget = max(floor, min(cap, remaining_sec * frac))
            return max(0.0, min(remaining_sec - 0.8, budget))
        elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
            # L_13_6_5_5: j≠k case
            frac = 0.06
            cap = 3.0
            floor = 1.0
            budget = max(floor, min(cap, remaining_sec * frac))
            return max(0.0, min(remaining_sec - 0.8, budget))
        elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
            # Other n=14 except L_14_7_7_6: simple fast iteration (like n=12)
            frac = 0.06
            cap = 3.0
            floor = 1.0
            budget = max(floor, min(cap, remaining_sec * frac))
            return max(0.0, min(remaining_sec - 0.8, budget))

        if self.n < 16:
            if self._containment:
                frac = 0.30 if current_len < 300 else 0.36
                cap = 34.0 if current_len < 300 else 42.0
                floor = 8.0
            elif self.j == self.k:
                frac = 0.28 if current_len < 120 else 0.34
                cap = 30.0 if current_len < 120 else 36.0
                floor = 7.0
            else:
                frac = 0.24
                cap = 18.0
                floor = 5.5
            budget = max(floor, min(cap, remaining_sec * frac))
            return max(0.0, min(remaining_sec - 0.8, budget))

        budget = max(8.0, min(56.0, remaining_sec * 0.58))
        return max(0.0, min(remaining_sec - 0.8, budget))

    def _phase_h_nlt16_cp_sat_refine(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if self.n > 16:
            return sol
        if self.n == 16 and not self._is_n16_hard_cluster():
            return sol
        if self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 6:
            return sol

        remaining = self._time_remaining_sec()
        if remaining is None or remaining < 5.0:
            return sol
        phase_budget = self._phase_h_budget_cap_sec(
            remaining_sec=float(remaining),
            current_len=len(sol),
        )
        if phase_budget < 1.5:
            return sol
        phase_deadline = time.time() + phase_budget

        cand_index = self._cand_index_map
        selected_indices = [cand_index[m] for m in sol if m in cand_index]
        if len(selected_indices) != len(sol):
            return sol

        ranked_scores = self._base_weighted_scores
        if ranked_scores is None:
            if self._cov_table is None:
                return sol
            ranked_scores = np.array([len(c) for c in self._cov_table], dtype=np.float64)

        if self.j == self.k and not self._containment:
            extras_cap = 5200 if self.n == 16 else 3600
        elif self._containment:
            extras_cap = 4200 if (self.n == 16 and self.k >= 6) else 3200
        else:
            extras_cap = 2400

        best_masks = list(sol)
        best_len = len(best_masks)
        target_ub = best_len - 1
        selected_set = set(selected_indices)

        while target_ub >= 1:
            if time.time() >= phase_deadline:
                break
            remaining = self._time_remaining_sec()
            if remaining is None or remaining < 4.0:
                break
            
            hard_case = (
                (self.j == self.k and not self._containment)
                or (self._containment and self.k >= 6 and self.n >= 14)
            )

            ranked = self._phase_h_ranked_candidates(selected_indices, ranked_scores)
            max_extra = max(0, self.num_cands - len(selected_indices))
            if max_extra <= 0:
                break

            # 小规模和小组数实例优先直接扩到全候选，避免精修被门槛挡住。
            if len(best_masks) <= 14 or self.num_targets <= 1800:
                extra_levels = [max_extra]
            else:
                if hard_case:
                    growth = [
                        min(max_extra, extras_cap),
                        min(max_extra, int(extras_cap * 1.85) + 520),
                        max_extra,
                    ]
                else:
                    growth = [
                        min(max_extra, extras_cap),
                        min(max_extra, int(extras_cap * 1.45) + 260),
                        min(max_extra, int(extras_cap * 2.05) + 640),
                        max_extra,
                    ]
                extra_levels = []
                for g in growth:
                    gg = int(max(0, g))
                    if gg not in extra_levels:
                        extra_levels.append(gg)

            found = False
            for extra_cap in extra_levels:
                if time.time() >= phase_deadline:
                    break
                run_remaining = self._time_remaining_sec()
                if run_remaining is None or run_remaining < 3.0:
                    break
                run_remaining = min(run_remaining, max(0.0, phase_deadline - time.time()))
                if run_remaining < 2.0:
                    break

                neighborhood = list(selected_indices)
                if extra_cap > 0:
                    for ci in ranked:
                        cii = int(ci)
                        if cii in selected_set:
                            continue
                        neighborhood.append(cii)
                        if len(neighborhood) >= len(selected_indices) + extra_cap:
                            break
                if len(neighborhood) <= len(selected_indices):
                    continue

                local_pos = {ci: idx for idx, ci in enumerate(neighborhood)}
                model = cp_model.CpModel()
                vars_x = [model.NewBoolVar(f"xh_{i}") for i in range(len(neighborhood))]
                objective = sum(vars_x)
                model.Add(objective <= target_ub)

                missing_cover = False
                for covering in self._inv_table:
                    loc = [local_pos[int(ci)] for ci in covering if int(ci) in local_pos]
                    if not loc:
                        missing_cover = True
                        break
                    model.AddBoolOr([vars_x[i] for i in loc])
                if missing_cover:
                    continue
                model.Minimize(objective)

                for ci in selected_indices:
                    p = local_pos.get(ci)
                    if p is not None:
                        model.AddHint(vars_x[p], 1)

                seeds = [1, 17]
                if run_remaining >= 26.0 and extra_cap < max_extra:
                    seeds.append(29)
                if extra_cap >= max_extra and run_remaining >= 18.0:
                    seeds.append(47)
                per_run = max(
                    2.5,
                    min(24.0 if hard_case else 12.0, (run_remaining - 0.8) / max(1, len(seeds))),
                )
                if hard_case:
                    per_run = max(3.5, per_run)

                for seed in seeds:
                    if time.time() >= phase_deadline:
                        break
                    seed_remaining = self._time_remaining_sec()
                    if seed_remaining is None or seed_remaining < 2.0:
                        break
                    seed_remaining = min(
                        seed_remaining,
                        max(0.0, phase_deadline - time.time()),
                    )
                    if seed_remaining < 1.3:
                        break
                    solver = cp_model.CpSolver()
                    solver.parameters.max_time_in_seconds = float(
                        min(per_run, max(1.5, seed_remaining - 0.7))
                    )
                    solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
                    solver.parameters.random_seed = seed
                    status = solver.Solve(model)
                    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                        continue

                    picked_local = [i for i in range(len(neighborhood)) if solver.Value(vars_x[i]) == 1]
                    if len(picked_local) >= best_len:
                        continue

                    picked_global = [neighborhood[i] for i in picked_local]
                    candidate = [int(self.cand_masks[i]) for i in picked_global]
                    if not self._verify(candidate):
                        continue

                    best_masks = candidate
                    best_len = len(best_masks)
                    target_ub = best_len - 1
                    selected_indices = picked_global
                    selected_set = set(selected_indices)
                    found = True
                    self._report(
                        "optimize",
                        f"Phase-H CP-SAT refined to {best_len} groups",
                    )
                    break

                if found:
                    break

            if not found:
                break

        return best_masks

    def _phase_i_nlt16_cluster_specialized_refine(self, sol: list[int]) -> list[int]:
        if self.n > 16:
            return sol
        if self.n == 16 and not self._is_n16_hard_cluster():
            return sol
        if self._deadline_at is None:
            return sol
        remaining = self._time_remaining_sec()
        if remaining is None or remaining < 3.5:
            return sol

        best = list(sol)
        if self.j == self.k and not self._containment:
            best = self._phase_i_jk_cycle_module(best)
            best = self._phase_i_full_cp_sat_module(best, hard_case=True)
            return best
        if self._containment:
            best = self._phase_i_containment_cycle_module(best)
            return self._phase_i_full_cp_sat_module(
                best,
                hard_case=bool(self.k >= 6 and self.n >= 14),
            )
        best = self._phase_i_general_small_module(best)
        return self._phase_i_full_cp_sat_module(best, hard_case=False)

    def _phase_i_jk_cycle_module(self, sol: list[int]) -> list[int]:
        if not self._is_mid_j_equals_k_noncontainment():
            return sol
        if self._cov_table is None or self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 18:
            return sol
        if not self._phase_c_has_time(3.5):
            return sol

        best = list(sol)
        misses = 0
        rounds = 10 if len(best) < 120 else 8
        for _ in range(rounds):
            rem = self._time_remaining_sec()
            if rem is None or rem < 3.2:
                break
            target_len = len(best) - 1
            if target_len < 1:
                break

            budget_cap = 10.0 if len(best) < 120 else 14.0
            round_budget = float(min(budget_cap, max(2.8, rem * 0.35)))

            start_masks = list(best)
            random.shuffle(start_masks)
            improved = self._phase_g_try_target_len(start_masks, target_len, round_budget)
            if improved is None:
                misses += 1
                if misses >= 3 and rem < 12.0:
                    break
                continue
            if len(improved) < len(best):
                best = improved
                misses = 0
                self._report(
                    "optimize",
                    f"Phase-I jk-cycle improved to {len(best)} groups",
                )
            else:
                misses += 1
                if misses >= 4:
                    break

        return best

    def _phase_i_containment_cycle_module(self, sol: list[int]) -> list[int]:
        if not self._containment:
            return sol
        if self.n > 16:
            return sol
        if self.n == 16 and self.k < 6:
            return sol
        if self._cov_table is None or self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        min_len = 36 if self.num_targets >= 1_500 else 24
        if len(sol) < min_len:
            return sol
        if not self._phase_c_has_time(4.0):
            return sol

        best = list(sol)
        misses = 0
        # N=12 optimization: reduce rounds for aggressive time reduction
        # Exception: L_12_6_4_3 uses original algorithm
        # N=13 optimization: only L_13_6_5_5 (j≠k case: rounds=4)
        # N=14 optimization: classified by difficulty
        if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
            rounds = 4
        elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
            rounds = 4
        elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
            # N=14 except L_14_7_7_6: simple fast iteration (like n=12)
            rounds = 4
        else:
            rounds = 10 if len(best) < 300 else 8
        for _ in range(rounds):
            rem = self._time_remaining_sec()
            if rem is None or rem < 3.2:
                break
            target_len = len(best) - 1
            if target_len < 1:
                break

            budget_cap = 12.0 if len(best) < 300 else 18.0
            round_budget = float(min(budget_cap, max(3.2, rem * 0.4)))

            start_masks = list(best)
            random.shuffle(start_masks)
            improved = self._phase_g_try_target_len(start_masks, target_len, round_budget)
            if improved is None:
                misses += 1
                if misses >= 3 and rem < 14.0:
                    break
                continue
            if len(improved) < len(best):
                best = improved
                misses = 0
                self._report(
                    "optimize",
                    f"Phase-I containment-cycle improved to {len(best)} groups",
                )
            else:
                misses += 1
                if misses >= 4:
                    break

        return best

    def _phase_i_general_small_module(self, sol: list[int]) -> list[int]:
        if self._containment or self.j == self.k:
            return sol
        if self.n >= 16:
            return sol
        if self._cov_table is None or self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 10 or len(sol) > 90:
            return sol
        if not self._phase_c_has_time(3.0):
            return sol

        best = list(sol)
        misses = 0
        rounds = 12
        for _ in range(rounds):
            rem = self._time_remaining_sec()
            if rem is None or rem < 2.6:
                break
            target_drop = 2 if len(best) <= 35 else 1
            target_len = len(best) - target_drop
            if target_len < 1:
                break

            round_budget = float(min(14.0, max(2.8, rem * 0.36)))
            start_masks = list(best)
            if misses > 0:
                random.shuffle(start_masks)
            improved = self._phase_g_try_target_len(start_masks, target_len, round_budget)
            if improved is None and target_drop == 2:
                improved = self._phase_g_try_target_len(start_masks, len(best) - 1, round_budget)
            if improved is None:
                misses += 1
                if misses >= 5:
                    break
                continue
            if len(improved) < len(best):
                best = improved
                misses = 0
                self._report(
                    "optimize",
                    f"Phase-I general-small improved to {len(best)} groups",
                )
            else:
                misses += 1
                if misses >= 5:
                    break

        return best

    def _phase_i_full_budget_cap_sec(
        self,
        *,
        remaining_sec: float,
        hard_case: bool,
        current_len: int,
    ) -> float:
        if remaining_sec <= 1.2:
            return 0.0

        # N=12 optimization: aggressive time reduction (10% error tolerance)
        # Exception: L_12_6_4_3 uses original algorithm (small solution sensitive)
        # N=13 optimization: only L_13_6_5_5 (j≠k case: frac=0.06, cap=3.0)
        # N=14 optimization: classified by difficulty
        if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
            if self._containment:
                frac = 0.10
                cap = 5.0
                floor = 1.5
            elif self.j == self.k:
                frac = 0.08
                cap = 4.0
                floor = 1.5
            else:
                frac = 0.06
                cap = 3.0
                floor = 1.0
            budget = max(floor, min(cap, remaining_sec * frac))
            return max(0.0, min(remaining_sec - 0.8, budget))
        elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
            # L_13_6_5_5: j≠k case
            frac = 0.06
            cap = 3.0
            floor = 1.0
            budget = max(floor, min(cap, remaining_sec * frac))
            return max(0.0, min(remaining_sec - 0.8, budget))
        elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
            # Other n=14 except L_14_7_7_6: simple fast iteration (like n=12)
            frac = 0.06
            cap = 3.0
            floor = 1.0
            budget = max(floor, min(cap, remaining_sec * frac))
            return max(0.0, min(remaining_sec - 0.8, budget))

        if self.n < 16:
            if self.j == self.k and not self._containment:
                frac = 0.22 if hard_case else 0.18
                cap = 22.0 if hard_case else 14.0
                floor = 4.5
            elif self._containment:
                frac = 0.28 if hard_case else 0.22
                cap = 28.0 if hard_case else 16.0
                floor = 5.0
            else:
                frac = 0.16
                cap = 10.0
                floor = 3.5
            budget = max(floor, min(cap, remaining_sec * frac))
            if current_len <= 90:
                budget = min(budget, 18.0 if hard_case else 12.0)
            return max(0.0, min(remaining_sec - 0.8, budget))

        frac = 0.52 if hard_case else 0.40
        cap = 42.0 if hard_case else 22.0
        floor = 7.0 if hard_case else 5.0
        budget = max(floor, min(cap, remaining_sec * frac))
        return max(0.0, min(remaining_sec - 0.8, budget))

    def _phase_i_full_cp_sat_module(
        self,
        sol: list[int],
        *,
        hard_case: bool,
    ) -> list[int]:
        if cp_model is None:
            return sol
        if self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 8:
            return sol
        expanded_n16_mid = (
            self.n == 16
            and self.j == self.k
            and not self._containment
            and self.num_cands <= 12_000
            and self.num_targets <= 9_000
        )
        if (self.num_cands > 7_000 or self.num_targets > 8_000) and not expanded_n16_mid:
            return sol

        remaining = self._time_remaining_sec()
        min_budget = 6.5 if hard_case else 4.5
        if remaining is None or remaining < min_budget:
            return sol
        phase_budget = self._phase_i_full_budget_cap_sec(
            remaining_sec=float(remaining),
            hard_case=hard_case,
            current_len=len(sol),
        )
        if phase_budget < 1.5:
            return sol
        phase_deadline = time.time() + phase_budget

        cand_index = self._cand_index_map
        selected_indices = [cand_index[m] for m in sol if m in cand_index]
        if len(selected_indices) != len(sol):
            return sol

        best_masks = list(sol)
        best_len = len(best_masks)
        # N=12 optimization: reduce rounds for aggressive time reduction
        # Exception: L_12_6_4_3 uses original algorithm
        # N=13 optimization: only L_13_6_5_5 (j≠k case: rounds=2)
        # N=14 optimization: classified by difficulty
        if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
            rounds = 2
        elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
            rounds = 2
        elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
            # N=14 except L_14_7_7_6: simple fast iteration (like n=12)
            rounds = 2
        else:
            rounds = 5 if hard_case else 3
            if expanded_n16_mid:
                rounds = min(rounds, 2)
        if best_len < 40:
            rounds = min(rounds, 2)
        stalls = 0

        for round_idx in range(rounds):
            if time.time() >= phase_deadline:
                break
            run_remaining = self._time_remaining_sec()
            if run_remaining is None or run_remaining < 3.0:
                break
            run_remaining = min(run_remaining, max(0.0, phase_deadline - time.time()))
            if run_remaining < 2.2:
                break
            
            target_ub = best_len - 1
            if target_ub < 1:
                break

            model = cp_model.CpModel()
            vars_x = [model.NewBoolVar(f"xi_{i}") for i in range(self.num_cands)]
            objective = sum(vars_x)
            model.Add(objective <= target_ub)
            for covering in self._inv_table:
                model.AddBoolOr([vars_x[int(ci)] for ci in covering])
            model.Minimize(objective)
            use_hints = stalls == 0 and round_idx == 0
            if use_hints:
                for ci in selected_indices:
                    model.AddHint(vars_x[ci], 1)
            elif selected_indices and hard_case:
                hint_keep = max(8, int(len(selected_indices) * 0.6))
                if hint_keep < len(selected_indices):
                    hint_idx = random.sample(selected_indices, hint_keep)
                else:
                    hint_idx = list(selected_indices)
                for ci in hint_idx:
                    model.AddHint(vars_x[ci], 1)

            if self.n < 16 and self.j == self.k and not self._containment:
                seeds = [1, 17]
                if run_remaining >= 12.0:
                    seeds.append(29)
            elif hard_case:
                if expanded_n16_mid:
                    seeds = [1, 17, 29]
                else:
                    seeds = [1, 17, 29, 43]
            else:
                seeds = [1, 17, 29]
            if hard_case and run_remaining >= 28.0 and self.n >= 16:
                seeds.append(59)
            if run_remaining >= 28.0 and self.n >= 16:
                seeds.append(47)

            if expanded_n16_mid:
                budget_cap = 18.0 if hard_case else 12.0
                ratio = 0.42 if hard_case else 0.32
            else:
                budget_cap = 42.0 if hard_case else 22.0
                ratio = 0.70 if hard_case else 0.50
            
            # N=12 optimization: aggressive time reduction (10% error tolerance)
            # Exception: L_12_6_4_3 uses original algorithm
            # N=13 optimization: only L_13_6_5_5 (j≠k case: cap=3.0, ratio=0.06)
            # N=14 optimization: classified by difficulty
            if self.n == 12 and not (self.k == 6 and self.j == 4 and self.s == 3):
                if self._containment:
                    budget_cap = min(budget_cap, 5.0)
                    ratio = min(ratio, 0.10)
                elif self.j == self.k:
                    budget_cap = min(budget_cap, 4.0)
                    ratio = min(ratio, 0.08)
                else:
                    budget_cap = min(budget_cap, 3.0)
                    ratio = min(ratio, 0.06)
            elif self.n == 13 and self.k == 6 and self.j == 5 and self.s == 5:
                # L_13_6_5_5: j≠k case
                budget_cap = min(budget_cap, 3.0)
                ratio = min(ratio, 0.06)
            elif self.n == 14 and not (self.k == 7 and self.j == 7 and self.s == 6):
                # N=14 except L_14_7_7_6: simple fast iteration (like n=12)
                budget_cap = min(budget_cap, 3.0)
                ratio = min(ratio, 0.06)
            elif self.n < 16:
                if self.j == self.k and not self._containment:
                    budget_cap = min(budget_cap, 18.0 if hard_case else 10.0)
                    ratio = min(ratio, 0.28 if hard_case else 0.20)
                elif self._containment:
                    budget_cap = min(budget_cap, 24.0 if hard_case else 12.0)
                    ratio = min(ratio, 0.34 if hard_case else 0.24)
                else:
                    budget_cap = min(budget_cap, 10.0 if hard_case else 8.0)
                    ratio = min(ratio, 0.18)
            total_budget = float(min(budget_cap, max(3.0, run_remaining * ratio)))
            per_run = max(2.0, total_budget / max(1, len(seeds)))
            if hard_case:
                per_run = max(4.0, per_run)

            improved = False
            for seed in seeds:
                if time.time() >= phase_deadline:
                    break
                seed_remaining = self._time_remaining_sec()
                if seed_remaining is None or seed_remaining < 2.0:
                    break
                seed_remaining = min(
                    seed_remaining,
                    max(0.0, phase_deadline - time.time()),
                )
                if seed_remaining < 1.3:
                    break
                solver = cp_model.CpSolver()
                solver.parameters.max_time_in_seconds = float(
                    min(per_run, max(1.5, seed_remaining - 0.7))
                )
                solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
                solver.parameters.random_seed = seed
                solver.parameters.randomize_search = True
                status = solver.Solve(model)
                if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                    continue

                picked = [i for i in range(self.num_cands) if solver.Value(vars_x[i]) == 1]
                if len(picked) >= best_len:
                    continue
                candidate = [int(self.cand_masks[i]) for i in picked]
                if not self._verify(candidate):
                    continue

                best_masks = candidate
                best_len = len(best_masks)
                selected_indices = picked
                improved = True
                stalls = 0
                self._report(
                    "optimize",
                    f"Phase-I full CP-SAT refined to {best_len} groups",
                )
                break

            if not improved:
                stalls += 1
                if (not hard_case) and stalls < 2:
                    continue
                break
            stalls = 0

        return best_masks

    def _phase_k_cluster_structural_refine(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if self._deadline_at is None:
            return sol
        if self.n > 16:
            return sol
        if self.n == 16 and not self._is_n16_hard_cluster():
            return sol
        remaining = self._time_remaining_sec()
        if remaining is None or remaining < 3.5:
            return sol

        best = list(sol)
        if self.j == self.k and not self._containment and self.s == (self.k - 1):
            before = len(best)
            best = self._phase_k_jk_orbit_cp_sat_refine(best)
            if self.n < 16:
                return best
            orbit_gain = before - len(best)
            if orbit_gain < max(10, before // 9):
                best = self._phase_k_jk_kminus1_domset_refine(best)
            return best
        if self._containment:
            before = len(best)
            best = self._phase_k_containment_orbit_cp_sat_refine(best)
            orbit_gain = before - len(best)
            if orbit_gain < max(10, before // 10):
                best = self._phase_k_containment_iterative_sat_refine(best)
            return best
        if self.n < 16 and (not self._containment) and self.j < self.k:
            best = self._phase_k_general_iterative_sat_refine(best)
            return best
        return best

    def _rotate_mask(self, mask: int, shift: int) -> int:
        if shift % self.n == 0:
            return mask
        out = 0
        for e in mask_to_elements(mask):
            out |= 1 << ((e + shift) % self.n)
        return out

    def _build_cyclic_orbits(self) -> list[list[int]]:
        seen: set[int] = set()
        orbits: list[list[int]] = []
        for ci, mm in enumerate(self.cand_masks):
            if ci in seen:
                continue
            mask = int(mm)
            orbit_set: set[int] = set()
            for shift in range(self.n):
                rotated = self._rotate_mask(mask, shift)
                idx = self._cand_index_map.get(rotated)
                if idx is not None:
                    orbit_set.add(int(idx))
            if not orbit_set:
                orbit_set.add(ci)
            orbit = sorted(orbit_set)
            for idx in orbit:
                seen.add(idx)
            orbits.append(orbit)
        return orbits

    def _phase_k_jk_orbit_cp_sat_refine(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if self.j != self.k or self._containment or self.s != (self.k - 1):
            return sol
        if self.n > 16:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 20:
            return sol
        if not self._phase_c_has_time(3.5):
            return sol

        orbits = self._build_cyclic_orbits()
        if len(orbits) >= self.num_cands:
            return sol

        orbit_of = np.full(self.num_cands, -1, dtype=np.int32)
        orbit_sizes: list[int] = []
        for oid, orbit in enumerate(orbits):
            orbit_sizes.append(len(orbit))
            for ci in orbit:
                orbit_of[ci] = oid

        # Build domination lists once (same logic as jk k-1 covering).
        cand_index = self._cand_index_map
        dom_orbits: list[list[int]] = []
        for mask_uint in self.cand_masks:
            tmask = int(mask_uint)
            cover_orbits: set[int] = set()
            self_idx = cand_index[tmask]
            cover_orbits.add(int(orbit_of[self_idx]))
            bits_in = mask_to_elements(tmask)
            bit_in_set = set(bits_in)
            bits_out = [e for e in range(self.n) if e not in bit_in_set]
            for rem in bits_in:
                rem_bit = 1 << rem
                base = tmask & (~rem_bit)
                for add in bits_out:
                    mm = base | (1 << add)
                    ci = cand_index.get(mm)
                    if ci is not None:
                        cover_orbits.add(int(orbit_of[ci]))
            dom_orbits.append(sorted(cover_orbits))

        best_len = len(sol)
        ub = best_len - 1
        rem = self._time_remaining_sec()
        if rem is None or rem < 2.5:
            return sol

        model = cp_model.CpModel()
        vars_y = [model.NewBoolVar(f"yo_{i}") for i in range(len(orbits))]
        weighted = sum(int(orbit_sizes[i]) * vars_y[i] for i in range(len(orbits)))
        model.Add(weighted <= ub)
        for cover in dom_orbits:
            model.AddBoolOr([vars_y[i] for i in cover])
        model.Minimize(weighted)

        per_run = min(16.0, max(4.0, rem * 0.42))
        seeds = [1, 17, 29]
        if rem >= 26.0:
            seeds.extend([43, 59])

        best_masks = list(sol)
        for seed in seeds:
            rem_seed = self._time_remaining_sec()
            if rem_seed is None or rem_seed < 2.0:
                break
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = float(
                min(per_run, max(1.5, rem_seed - 0.6))
            )
            solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            solver.parameters.random_seed = seed
            solver.parameters.randomize_search = True
            status = solver.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                continue
            picked_orbits = [i for i in range(len(orbits)) if solver.Value(vars_y[i]) == 1]
            picked_idx: list[int] = []
            for oid in picked_orbits:
                picked_idx.extend(orbits[oid])
            if len(picked_idx) >= best_len:
                continue
            candidate = [int(self.cand_masks[i]) for i in sorted(set(picked_idx))]
            candidate = self._local_search(candidate)
            if len(candidate) >= best_len:
                continue
            if not self._verify(candidate):
                continue
            best_masks = candidate
            best_len = len(best_masks)
            self._report(
                "optimize",
                f"Phase-K jk-orbit refined to {best_len} groups",
            )
            break

        return best_masks

    def _phase_k_containment_orbit_cp_sat_refine(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if not self._containment:
            return sol
        if self._inv_table is None:
            return sol
        if self.n > 16:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 24:
            return sol
        if not self._phase_c_has_time(3.5):
            return sol

        orbits = self._build_cyclic_orbits()
        if len(orbits) >= self.num_cands:
            return sol

        orbit_of = np.full(self.num_cands, -1, dtype=np.int32)
        orbit_sizes: list[int] = []
        for oid, orbit in enumerate(orbits):
            orbit_sizes.append(len(orbit))
            for ci in orbit:
                orbit_of[ci] = oid

        target_cover_orbits: list[list[int]] = []
        for covering in self._inv_table:
            orbit_set = {int(orbit_of[int(ci)]) for ci in covering}
            if not orbit_set:
                return sol
            target_cover_orbits.append(sorted(orbit_set))

        best_len = len(sol)
        ub = best_len - 1
        rem = self._time_remaining_sec()
        if rem is None or rem < 2.5:
            return sol

        model = cp_model.CpModel()
        vars_y = [model.NewBoolVar(f"yc_{i}") for i in range(len(orbits))]
        weighted = sum(int(orbit_sizes[i]) * vars_y[i] for i in range(len(orbits)))
        model.Add(weighted <= ub)
        for cover in target_cover_orbits:
            model.AddBoolOr([vars_y[i] for i in cover])
        model.Minimize(weighted)

        per_run = min(16.0, max(3.5, rem * 0.42))
        seeds = [1, 17, 29]
        if rem >= 26.0:
            seeds.extend([43, 59])

        best_masks = list(sol)
        for seed in seeds:
            rem_seed = self._time_remaining_sec()
            if rem_seed is None or rem_seed < 2.0:
                break
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = float(
                min(per_run, max(1.5, rem_seed - 0.6))
            )
            solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
            solver.parameters.random_seed = seed
            solver.parameters.randomize_search = True
            status = solver.Solve(model)
            if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                continue
            picked_orbits = [i for i in range(len(orbits)) if solver.Value(vars_y[i]) == 1]
            picked_idx: list[int] = []
            for oid in picked_orbits:
                picked_idx.extend(orbits[oid])
            if len(picked_idx) >= best_len:
                continue
            candidate = [int(self.cand_masks[i]) for i in sorted(set(picked_idx))]
            candidate = self._local_search(candidate)
            if len(candidate) >= best_len:
                continue
            if not self._verify(candidate):
                continue
            best_masks = candidate
            best_len = len(best_masks)
            self._report(
                "optimize",
                f"Phase-K containment-orbit refined to {best_len} groups",
            )
            break

        return best_masks

    def _phase_k_jk_kminus1_domset_refine(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if self.j != self.k or self._containment or self.s != (self.k - 1):
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 12:
            return sol
        if self.num_cands > 12_000:
            return sol
        if not self._phase_c_has_time(3.5):
            return sol

        cand_index = self._cand_index_map
        selected_idx = [cand_index[m] for m in sol if m in cand_index]
        if len(selected_idx) != len(sol):
            return sol

        # Domination in Johnson graph J(n,k), radius=1 in swap distance.
        dom_lists: list[list[int]] = []
        for mask_uint in self.cand_masks:
            tmask = int(mask_uint)
            coverers = {cand_index[tmask]}
            bits_in = mask_to_elements(tmask)
            bit_in_set = set(bits_in)
            bits_out = [e for e in range(self.n) if e not in bit_in_set]
            for rem in bits_in:
                rem_bit = 1 << rem
                base = tmask & (~rem_bit)
                for add in bits_out:
                    add_bit = 1 << add
                    mm = base | add_bit
                    ci = cand_index.get(mm)
                    if ci is not None:
                        coverers.add(ci)
            dom_lists.append(sorted(coverers))

        best_masks = list(sol)
        best_len = len(best_masks)
        ub = best_len - 1
        miss = 0
        while ub >= 1:
            rem = self._time_remaining_sec()
            if rem is None or rem < 2.8:
                break
            if miss >= 2:
                break

            model = cp_model.CpModel()
            vars_x = [model.NewBoolVar(f"xk_{i}") for i in range(self.num_cands)]
            model.Add(sum(vars_x) <= ub)
            for dom in dom_lists:
                model.AddBoolOr([vars_x[i] for i in dom])

            # 失败后切换为无hint，避免被当前解结构锁死。
            if miss == 0 and selected_idx:
                hint_keep = max(8, int(len(selected_idx) * 0.7))
                if hint_keep < len(selected_idx):
                    hint_idx = random.sample(selected_idx, hint_keep)
                else:
                    hint_idx = list(selected_idx)
                for ci in hint_idx:
                    model.AddHint(vars_x[ci], 1)

            seeds = [1, 17, 29]
            if rem >= 22.0:
                seeds.extend([43, 59])
            per_run = max(2.2, min(18.0, (rem * 0.72) / max(1, len(seeds))))
            if miss > 0:
                per_run = min(24.0, per_run * 1.35)

            found = False
            for seed in seeds:
                rem_seed = self._time_remaining_sec()
                if rem_seed is None or rem_seed < 2.0:
                    break
                solver = cp_model.CpSolver()
                solver.parameters.max_time_in_seconds = float(
                    min(per_run, max(1.3, rem_seed - 0.6))
                )
                solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
                solver.parameters.random_seed = seed
                solver.parameters.randomize_search = True
                status = solver.Solve(model)
                if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                    continue

                picked = [i for i in range(self.num_cands) if solver.Value(vars_x[i]) == 1]
                if len(picked) >= best_len:
                    continue
                candidate = [int(self.cand_masks[i]) for i in picked]
                if not self._verify(candidate):
                    continue

                best_masks = candidate
                best_len = len(best_masks)
                selected_idx = picked
                ub = best_len - 1
                miss = 0
                found = True
                self._report(
                    "optimize",
                    f"Phase-K jk-domset refined to {best_len} groups",
                )
                break

            if not found:
                miss += 1
                if miss >= 3:
                    break

        return best_masks

    def _phase_k_containment_iterative_sat_refine(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if not self._containment:
            return sol
        if self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 16:
            return sol
        if self.num_cands > 10_000 or self.num_targets > 10_000:
            return sol
        if not self._phase_c_has_time(3.5):
            return sol
        rem0 = self._time_remaining_sec()
        if rem0 is None or rem0 < 2.5:
            return sol
        phase_budget = min(20.0, max(6.0, rem0 * 0.26))
        phase_deadline = time.time() + phase_budget

        cand_index = self._cand_index_map
        selected_idx = [cand_index[m] for m in sol if m in cand_index]
        if len(selected_idx) != len(sol):
            return sol

        best_masks = list(sol)
        best_len = len(best_masks)
        ub = best_len - 1
        miss = 0
        while ub >= 1:
            if time.time() >= phase_deadline:
                break
            rem = self._time_remaining_sec()
            if rem is None or rem < 2.8:
                break
            rem = min(rem, max(0.0, phase_deadline - time.time()))
            if rem < 2.0:
                break
            if miss >= 2:
                break

            model = cp_model.CpModel()
            vars_x = [model.NewBoolVar(f"xc_{i}") for i in range(self.num_cands)]
            model.Add(sum(vars_x) <= ub)
            for covering in self._inv_table:
                model.AddBoolOr([vars_x[int(ci)] for ci in covering])

            if miss == 0 and selected_idx:
                hint_keep = max(10, int(len(selected_idx) * 0.65))
                if hint_keep < len(selected_idx):
                    hint_idx = random.sample(selected_idx, hint_keep)
                else:
                    hint_idx = list(selected_idx)
                for ci in hint_idx:
                    model.AddHint(vars_x[ci], 1)

            seeds = [1, 17, 29]
            if rem >= 20.0:
                seeds.extend([43, 59])
            per_run = max(2.0, min(16.0, (rem * 0.68) / max(1, len(seeds))))
            if miss > 0:
                per_run = min(22.0, per_run * 1.3)

            found = False
            for seed in seeds:
                if time.time() >= phase_deadline:
                    break
                rem_seed = self._time_remaining_sec()
                if rem_seed is None or rem_seed < 2.0:
                    break
                rem_seed = min(rem_seed, max(0.0, phase_deadline - time.time()))
                if rem_seed < 1.3:
                    break
                solver = cp_model.CpSolver()
                solver.parameters.max_time_in_seconds = float(
                    min(per_run, max(1.3, rem_seed - 0.6))
                )
                solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
                solver.parameters.random_seed = seed
                solver.parameters.randomize_search = True
                status = solver.Solve(model)
                if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                    continue

                picked = [i for i in range(self.num_cands) if solver.Value(vars_x[i]) == 1]
                if len(picked) >= best_len:
                    continue
                candidate = [int(self.cand_masks[i]) for i in picked]
                if not self._verify(candidate):
                    continue

                best_masks = candidate
                best_len = len(best_masks)
                selected_idx = picked
                ub = best_len - 1
                miss = 0
                found = True
                self._report(
                    "optimize",
                    f"Phase-K containment SAT refined to {best_len} groups",
                )
                break

            if not found:
                miss += 1
                if miss >= 3:
                    break

        return best_masks

    def _phase_k_general_iterative_sat_refine(self, sol: list[int]) -> list[int]:
        if cp_model is None:
            return sol
        if self._containment or self.j == self.k:
            return sol
        if self._inv_table is None:
            return sol
        if self._deadline_at is None:
            return sol
        if len(sol) < 10 or len(sol) > 120:
            return sol
        if self.num_cands > 8_000:
            return sol
        if not self._phase_c_has_time(2.8):
            return sol
        rem0 = self._time_remaining_sec()
        if rem0 is None or rem0 < 2.2:
            return sol
        phase_budget = min(18.0, max(5.0, rem0 * 0.24))
        phase_deadline = time.time() + phase_budget

        cand_index = self._cand_index_map
        selected_idx = [cand_index[m] for m in sol if m in cand_index]
        if len(selected_idx) != len(sol):
            return sol

        best_masks = list(sol)
        best_len = len(best_masks)
        ub = best_len - 1
        misses = 0
        while ub >= 1:
            if time.time() >= phase_deadline:
                break
            rem = self._time_remaining_sec()
            if rem is None or rem < 2.5:
                break
            rem = min(rem, max(0.0, phase_deadline - time.time()))
            if rem < 1.9:
                break
            if misses >= 2:
                break

            model = cp_model.CpModel()
            vars_x = [model.NewBoolVar(f"xg_{i}") for i in range(self.num_cands)]
            model.Add(sum(vars_x) <= ub)
            for covering in self._inv_table:
                model.AddBoolOr([vars_x[int(ci)] for ci in covering])

            if misses == 0 and selected_idx:
                for ci in selected_idx:
                    model.AddHint(vars_x[ci], 1)

            seeds = [1, 17, 29]
            per_run = max(1.8, min(10.0, (rem * 0.52) / max(1, len(seeds))))
            if misses > 0:
                per_run = min(14.0, per_run * 1.3)

            found = False
            for seed in seeds:
                if time.time() >= phase_deadline:
                    break
                rem_seed = self._time_remaining_sec()
                if rem_seed is None or rem_seed < 1.8:
                    break
                rem_seed = min(rem_seed, max(0.0, phase_deadline - time.time()))
                if rem_seed < 1.2:
                    break
                solver = cp_model.CpSolver()
                solver.parameters.max_time_in_seconds = float(
                    min(per_run, max(1.2, rem_seed - 0.5))
                )
                solver.parameters.num_search_workers = max(1, min(8, os.cpu_count() or 1))
                solver.parameters.random_seed = seed
                solver.parameters.randomize_search = True
                status = solver.Solve(model)
                if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
                    continue

                picked = [i for i in range(self.num_cands) if solver.Value(vars_x[i]) == 1]
                if len(picked) >= best_len:
                    continue
                candidate = [int(self.cand_masks[i]) for i in picked]
                if not self._verify(candidate):
                    continue

                best_masks = candidate
                best_len = len(best_masks)
                selected_idx = picked
                ub = best_len - 1
                misses = 0
                found = True
                self._report(
                    "optimize",
                    f"Phase-K general SAT refined to {best_len} groups",
                )
                break

            if not found:
                misses += 1
                if misses >= 3:
                    break

        return best_masks

    def _destroy_repair_order(self, sol: list[int]) -> list[int]:
        cov_count = np.zeros(self.num_targets, dtype=np.int32)
        sol_cov: list[np.ndarray] = []

        for mask in sol:
            covered = self._covers_bool(mask)
            sol_cov.append(covered)
            cov_count += covered.astype(np.int32)

        ranked: list[tuple[float, int, int, int]] = []
        for idx, covered in enumerate(sol_cov):
            fragile = covered & (cov_count <= 2)
            fragile_weight = float(self._target_weights[fragile].sum())
            unique_targets = int(np.sum(cov_count[covered] == 1))
            total_targets = int(np.sum(covered))
            ranked.append((fragile_weight, unique_targets, total_targets, idx))

        ranked.sort()
        return [idx for _, _, _, idx in ranked]

    def _destroy_repair_count(self, current_len: int) -> int:
        if self._is_large_j_equals_k_noncontainment() and current_len >= 180:
            base = max(6, current_len // 16)
            lo = max(6, base - 3)
            hi = min(22, base + 3)
            if hi <= lo:
                return lo
            return random.randint(lo, hi)
        if self._is_mid_j_equals_k_noncontainment():
            if current_len >= 220:
                base = max(5, current_len // 34)
                lo = max(4, base - 2)
                hi = min(14, base + 2)
            elif current_len >= 80:
                base = max(4, current_len // 18)
                lo = max(3, base - 1)
                hi = min(10, base + 2)
            else:
                base = max(3, current_len // 16)
                lo = max(2, base - 1)
                hi = min(8, base + 1)
            if hi <= lo:
                return lo
            return random.randint(lo, hi)
        return min(5, max(2, current_len // 15))

    @staticmethod
    def _destroy_repair_remove_set(
        order: list[int],
        remove_count: int,
        solution_len: int,
        *,
        mixed: bool,
    ) -> set[int]:
        if not mixed:
            return set(order[:remove_count])

        seeded = max(1, remove_count // 3)
        chosen: set[int] = set(order[:seeded])
        if len(chosen) >= remove_count:
            return chosen
        need = remove_count - len(chosen)
        universe = list(range(solution_len))
        if len(universe) <= need:
            chosen.update(universe)
            return chosen
        chosen.update(random.sample(universe, need))
        return chosen

    def _destroy_repair(
        self,
        sol: list[int],
        strategy: GreedyStrategy,
        *,
        rounds: int = 1,
    ) -> list[int]:
        if not self._allow_destroy_repair(sol):
            return sol

        best = list(sol)
        large_mode = self._is_large_j_equals_k_noncontainment() and len(best) >= 180
        no_improve = 0
        max_no_improve = 4 if large_mode else 1
        for _ in range(rounds):
            if self._cancel():
                break

            destroy_count = self._destroy_repair_count(len(best))
            if len(best) <= destroy_count:
                break

            order = self._destroy_repair_order(best)
            mixed_remove = large_mode and (no_improve > 0 or strategy.randomize)
            remove_set = self._destroy_repair_remove_set(
                order,
                destroy_count,
                len(best),
                mixed=mixed_remove,
            )
            partial = [
                mask for idx, mask in enumerate(best)
                if idx not in remove_set
            ]

            limit_slack = 8 if large_mode else 0
            repaired, complete, _ = self._greedy(
                strategy,
                partial=partial,
                best_limit=len(best) + limit_slack,
            )
            if not complete:
                fallback = self._fast_complete_partial_solution(
                    partial,
                    best_limit=len(best) + limit_slack,
                )
                if fallback is None:
                    no_improve += 1
                    if no_improve >= max_no_improve:
                        break
                    continue
                repaired = fallback

            candidate = self._local_search(repaired)
            if len(candidate) < len(best):
                best = candidate
                no_improve = 0
                self._report(
                    "optimize",
                    f"Destroy-repair improved to {len(best)} groups",
                )
            else:
                no_improve += 1
                if no_improve >= max_no_improve:
                    break

        return best

    def _swap_improve(self, sol: list[int], rounds: int = 3) -> list[int]:
        if len(sol) > 60:
            return sol
        for _ in range(rounds):
            if self._cancel():
                break
            improved = False
            order = list(range(len(sol)))
            random.shuffle(order)
            for i in order:
                if self._cancel():
                    break
                rest = sol[:i] + sol[i + 1:]
                uncov = self._uncovered_masks(rest)
                if len(uncov) == 0:
                    sol = rest
                    improved = True
                    self._report("optimize", f"Swap: removed -> {len(sol)} groups")
                    break
                for cm in self.cand_masks:
                    cm_int = int(cm)
                    if cm_int == sol[i]:
                        continue
                    ints = np.uint32(cm_int) & uncov
                    ok = (
                        np.all(ints == uncov)
                        if self._containment
                        else np.all(popcount_uint32(ints) >= self.s)
                    )
                    if ok:
                        sol = rest + [cm_int]
                        improved = True
                        break
                if improved:
                    break
            if not improved:
                break
        return sol

    # ------------------------------------------------------------------
    # Simulated annealing post-processing
    # ------------------------------------------------------------------

    def _sa_improve(self, sol: list[int], max_time: float = 10.0) -> list[int]:
        if len(sol) <= 3:
            return sol
        best = list(sol)
        current = list(sol)
        t0 = time.time()
        T = 1.0
        cooling = 0.995
        best_len = len(best)

        cand_list = self.cand_masks.tolist()
        nc = len(cand_list)

        while T > 0.01 and not self._cancel():
            if (time.time() - t0) > max_time:
                break

            idx = random.randrange(len(current))
            new_mask = cand_list[random.randrange(nc)]
            old_mask = current[idx]
            if new_mask == old_mask:
                continue

            current[idx] = new_mask
            if self._verify(current):
                trial = list(current)
                random.shuffle(trial)
                reduced = []
                rem_uncov = np.ones(self.num_targets, dtype=bool)
                for m in trial:
                    if not rem_uncov.any():
                        break
                    ints = np.uint32(m) & self.target_masks[rem_uncov]
                    if self._containment:
                        hits = np.any(ints == self.target_masks[rem_uncov])
                    else:
                        hits = np.any(popcount_uint32(ints) >= self.s)
                    if hits:
                        reduced.append(m)
                        self._mark_covered(m, rem_uncov)

                if self._verify(reduced) and len(reduced) < best_len:
                    best = reduced
                    best_len = len(best)
                    current = list(best)
                    self._report("sa", f"SA improved to {best_len} groups")
                elif len(current) <= len(best) + 1:
                    pass
                else:
                    delta = len(current) - len(best)
                    if random.random() >= math.exp(-delta / T):
                        current[idx] = old_mask
            else:
                current[idx] = old_mask

            T *= cooling

        return best

    # ------------------------------------------------------------------
    # Progress reporting
    # ------------------------------------------------------------------

    def _report(self, phase: str, msg: str, **kw: int) -> None:
        if self._cb:
            self._cb(
                SolverProgress(
                    phase=phase,
                    message=msg,
                    iteration=kw.get("iteration", 0),
                    solution_size=kw.get("sol_size", 0),
                    remaining=kw.get("remaining", 0),
                    total=self.num_targets,
                    elapsed=time.time() - self._t0,
                )
            )

    def _should_build_fast_seed(self) -> bool:
        return (
            self._cov_table is None
            and (self.num_targets >= 20_000 or self._interaction_scale >= 1_000_000_000)
        )

    def _note_legal_solution(self) -> None:
        if self._first_legal_elapsed is None:
            self._first_legal_elapsed = time.time() - self._t0

    def _fast_seed_solution(self) -> list[int]:
        return self._fast_complete_partial_solution([])

    def _fast_complete_partial_solution(
        self,
        partial: list[int],
        *,
        best_limit: int | None = None,
    ) -> list[int] | None:
        uncovered = np.ones(self.num_targets, dtype=bool)
        selected = list(partial)
        for mask in selected:
            self._mark_covered(mask, uncovered)

        return self._fast_complete_selected(
            selected,
            uncovered,
            best_limit=best_limit,
        )

    def _fast_complete_selected(
        self,
        selected: list[int],
        uncovered: np.ndarray,
        *,
        best_limit: int | None = None,
    ) -> list[int] | None:
        rem = int(uncovered.sum())

        if rem == 0:
            return selected

        chosen = set(selected)
        iteration = 0
        log_interval = max(1, self.num_targets // 500)
        freq = self._fast_completion_freq(uncovered)

        while rem > 0:
            if best_limit is not None and len(selected) >= best_limit:
                return None
            target_idx = int(np.argmax(uncovered))
            if not uncovered[target_idx]:
                break
            mask = self._canonical_cover_mask(
                int(self.target_masks[target_idx]),
                chosen,
                freq=freq,
            )
            if mask not in chosen:
                selected.append(mask)
                chosen.add(mask)
            self._mark_covered(mask, uncovered)
            iteration += 1
            rem = int(uncovered.sum())
            if iteration % 128 == 0:
                freq = self._fast_completion_freq(uncovered)
            if iteration % log_interval == 0 or rem == 0:
                self._report(
                    "seed",
                    f"Seed/repair iter {iteration}: {rem} left",
                    iteration=iteration,
                    sol_size=len(selected),
                    remaining=rem,
                )

        return selected

    def _canonical_cover_mask(
        self,
        target_mask: int,
        chosen: set[int],
        *,
        freq: np.ndarray | None = None,
    ) -> int:
        target_elems = mask_to_elements(target_mask)
        need = self.k - len(target_elems)
        if need <= 0:
            return target_mask

        available = [e for e in range(self.n) if not (target_mask & (1 << e))]
        if freq is not None and len(available) > 1:
            available.sort(key=lambda e: (-int(freq[e]), e))
        if need == 1:
            for extra in available:
                candidate = target_mask | (1 << extra)
                if candidate not in chosen:
                    return candidate
            return target_mask | (1 << available[0])

        candidate = target_mask
        for extra in available[:need]:
            candidate |= 1 << extra
        if candidate not in chosen:
            return candidate

        for extras in combinations(available, need):
            candidate = target_mask
            for extra in extras:
                candidate |= 1 << extra
            if candidate not in chosen:
                return candidate

        candidate = target_mask
        for extra in available[:need]:
            candidate |= 1 << extra
        return candidate

    def _should_repair_partial(self, remaining: int, best: list[int] | None) -> bool:
        if remaining <= 0:
            return False
        if best is None:
            return True
        limit = min(25_000, max(2_000, self.num_targets // 4))
        return remaining <= limit

    def _should_finish_fast(self, remaining: int) -> bool:
        if self._cov_table is not None:
            return False
        if self.num_targets < 100_000:
            return False
        return remaining <= 25_000

    def _fast_completion_freq(self, uncovered: np.ndarray) -> np.ndarray | None:
        if self._target_has_elem is None:
            return None
        return self._target_has_elem[uncovered].sum(axis=0, dtype=np.int64)
