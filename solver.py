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

import math
import os
import random
import site
import subprocess
import sys
import time
from dataclasses import dataclass, replace
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Callable

import numpy as np

from identity_cover_module import build_identity_cover


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
from solver import _add_windows_cuda_dll_dirs
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
            from tcovering_solver import TCoveringSolver
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
        self._deadline_at = (
            self._t0 + self._time_budget_sec if self._time_budget_sec is not None else None
        )
        self._skip_final_verify = skip_final_verify
        self._first_legal_elapsed: float | None = None

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

        self._gpu_enabled = bool(
            _env_int("CK_USE_GPU", 1)
            and cp is not None
            and self._interaction_scale >= 500_000_000
            and _probe_gpu_batch_path()
        )

        mem_estimate = self.num_cands * self.num_targets
        if self._containment and mem_estimate > 20_000_000:
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
        
        if self._identity_cover:
            return self._solve_identity_cover()

        best: list[int] | None = None
        base_attempts = self._effective_attempts()
        profile_attempts = self._phase_a_profile_attempts(base_attempts)
        hard_cap = self._phase_a_hard_attempt_cap(base_attempts, profile_attempts)
        profiles = self._build_attempt_profiles(profile_attempts)

        attempt = 0
        stagnant = 0
        avg_attempt_sec: float | None = None
        best_updated_at: float | None = None
        last_sol_sig: int | None = None
        same_sig_streak = 0

        if self._gpu_enabled:
            self._report("gpu", "GPU batch scoring enabled")

        if self._should_build_fast_seed():
            seed = self._fast_seed_solution()
            if seed:
                best = seed
                best_updated_at = time.time()
                self._note_legal_solution()
                self._report("seed", f"Fast legal seed: {len(seed)} groups")

        large_seed_intensify = self._is_large_j_equals_k_noncontainment()
        while attempt < hard_cap:
            attempt_idx = attempt + 1
            if self._cancel():
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

            attempt_elapsed = max(0.0, time.time() - attempt_started_at)
            if avg_attempt_sec is None:
                avg_attempt_sec = attempt_elapsed
            else:
                avg_attempt_sec = (avg_attempt_sec * 0.7) + (attempt_elapsed * 0.3)

            attempt += 1
            if (
                attempt >= base_attempts
                and stagnant >= self._phase_a_stagnation_limit()
                and not self._phase_a_can_extend_search(avg_attempt_sec, attempt, hard_cap)
            ):
                break

        if best is not None:
            best = self._phase_e_mid_compact_search(best)
            best = self._phase_f_small_cp_sat_polish(best)
            best = self._phase_f_mid_cp_sat_refine(best)

        masks = best or []
        return SolverResult(
            groups=[sorted(mask_to_elements(m)) for m in masks],
            elapsed=time.time() - self._t0,
            verified=False if self._skip_final_verify else self._verify(masks),
            first_legal_elapsed=self._first_legal_elapsed,
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
            verified=bool(built.complete and not self._skip_final_verify),
            first_legal_elapsed=self._first_legal_elapsed,
            groups_complete=fully_materialized,
            group_masks=masks,
        )

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

    def _phase_a_stagnation_limit(self) -> int:
        if self._interaction_scale <= 2_000_000:
            return 2
        if self._interaction_scale <= 30_000_000:
            return 3
        if self._interaction_scale <= 200_000_000:
            return 3
        return 2

    def _time_remaining_sec(self) -> float | None:
        if self._deadline_at is None:
            return None
        return max(0.0, self._deadline_at - time.time())

    def _phase_a_should_stop_for_budget(self, avg_attempt_sec: float | None) -> bool:
        remaining = self._time_remaining_sec()
        if remaining is None:
            return False
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
        if not self._is_large_j_equals_k_noncontainment():
            return False

        remaining = self._time_remaining_sec()
        if remaining is None:
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
            and 8_000 <= self.num_targets < 70_000
        )

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
            and len(targets) >= 4096
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
            and len(targets) >= 4096
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
            and self.num_targets >= 4096
            and len(masks) * self.num_targets >= 20_000_000
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
            and self.num_targets >= 4096
            and masks
            and len(masks) * self.num_targets >= 20_000_000
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
        if len(sol) < 24:
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
        if len(sol) < 24:
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
        if len(sol) < 16:
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
            model.Add(sum(vars_x) <= upper_bound)
            for covering in self._inv_table:
                model.AddBoolOr([vars_x[int(ci)] for ci in covering])

            for idx in selected_indices:
                model.AddHint(vars_x[idx], 1)

            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = float(min(20.0, max(1.5, remaining - 0.8)))
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
        model.Add(sum(vars_x) <= target_ub)
        for covering in self._inv_table:
            loc = [local_pos[int(ci)] for ci in covering if int(ci) in local_pos]
            if not loc:
                continue
            model.AddBoolOr([vars_x[i] for i in loc])
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
