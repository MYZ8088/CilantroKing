"""j=k=s 时的专用构造模块：显式生成全部 k 组合掩码。"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import Callable

import numpy as np


@dataclass
class IdentityCoverBuildResult:
    """Identity 构造结果。"""

    masks: np.ndarray
    complete: bool
    total_expected: int


def _next_same_popcount(mask: int) -> int:
    """Gosper hack：返回下一个 1 位数量相同的整数。"""
    lowbit = mask & -mask
    ripple = mask + lowbit
    ones = ((ripple ^ mask) >> 2) // lowbit
    return ripple | ones


def build_identity_cover(
    n: int,
    k: int,
    *,
    cancel_fn: Callable[[], bool] | None = None,
    progress_cb: Callable[[int, int], None] | None = None,
    report_interval: int = 4096,
) -> IdentityCoverBuildResult:
    """显式构造 C(n,k) 个组合掩码；支持取消与进度回调。"""
    if not (0 <= k <= n <= 31):
        raise ValueError(f"Need 0<=k<=n<=31, got n={n}, k={k}")

    total = comb(n, k)
    out = np.empty(total, dtype=np.uint32)
    cancel = cancel_fn or (lambda: False)
    step = max(1, report_interval)

    if total == 0:
        return IdentityCoverBuildResult(masks=np.empty(0, dtype=np.uint32), complete=True, total_expected=0)

    if k == 0:
        out[0] = np.uint32(0)
        if progress_cb is not None:
            progress_cb(1, 1)
        return IdentityCoverBuildResult(masks=out, complete=True, total_expected=1)

    limit = 1 << n
    mask = (1 << k) - 1
    idx = 0

    while mask < limit and idx < total:
        if cancel():
            partial = out[:idx].copy()
            return IdentityCoverBuildResult(
                masks=partial,
                complete=False,
                total_expected=total,
            )

        out[idx] = np.uint32(mask)
        idx += 1

        if progress_cb is not None and (idx == total or idx % step == 0):
            progress_cb(idx, total)

        if idx >= total:
            break

        mask = _next_same_popcount(mask)

    complete = (idx == total)
    masks = out if complete else out[:idx].copy()
    return IdentityCoverBuildResult(
        masks=masks,
        complete=complete,
        total_expected=total,
    )
