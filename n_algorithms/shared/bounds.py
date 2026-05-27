from __future__ import annotations

import math
from typing import Any


def block_cover_count(n: int, k: int, j: int, s: int) -> int:
    total = 0
    for intersection_size in range(s, min(j, k) + 1):
        outside_size = j - intersection_size
        if 0 <= outside_size <= n - k:
            total += math.comb(k, intersection_size) * math.comb(n - k, outside_size)
    return total


def schonheim_bound(n: int, k: int, t: int) -> int:
    if t <= 0:
        return 1
    return math.ceil(n * schonheim_bound(n - 1, k - 1, t - 1) / k)


def get_bounds(n: int, k: int, j: int, s: int) -> dict[str, Any]:
    capacity = block_cover_count(n, k, j, s)
    if capacity <= 0:
        raise ValueError("no k-group can cover the requested j/s condition")
    counting_bound = math.ceil(math.comb(n, j) / capacity)
    schonheim = schonheim_bound(n, k, j) if s == j else None
    lower_bound = max(counting_bound, schonheim or 0)
    return {
        "lower_bound": lower_bound,
        "counting_bound": counting_bound,
        "schonheim_bound": schonheim,
        "ljcr_best": None,
    }