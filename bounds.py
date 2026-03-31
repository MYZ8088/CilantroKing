"""Lower bounds and known-best values for covering design validation.

Provides:
  - Schönheim recursive lower bound for C(n,k,t) where s==j (containment)
  - Volume (packing) lower bound for general L(n,k,j,s)
  - LJCR (La Jolla Covering Repository) known best upper bounds for C(n,k,t)
"""

from __future__ import annotations

import math
from math import comb, ceil


# ------------------------------------------------------------------
# Schönheim bound  (recursive lower bound for containment C(n,k,t))
# ------------------------------------------------------------------

def schoenheim_bound(n: int, k: int, t: int) -> int:
    """Recursive Schönheim lower bound for C(n,k,t).

    C(n,k,t) >= ceil(n/k * ceil((n-1)/(k-1) * ... ))
    Base case: C(n,k,0) = 1, C(n,k,1) = ceil(n/k)
    """
    if t <= 0:
        return 1
    if t == 1:
        return ceil(n / k)
    if n <= t:
        return 1
    if n <= k:
        return 1
    inner = schoenheim_bound(n - 1, k - 1, t - 1)
    return ceil(n * inner / k)


# ------------------------------------------------------------------
# Volume (packing) lower bound for general L(n, k, j, s)
# ------------------------------------------------------------------

def max_coverage_per_candidate(n: int, k: int, j: int, s: int) -> int:
    """Max number of j-subsets a single k-subset can cover (|intersection| >= s)."""
    total = 0
    for i in range(s, min(j, k) + 1):
        total += comb(k, i) * comb(n - k, j - i)
    return total


def volume_lower_bound(n: int, k: int, j: int, s: int) -> int:
    """Simple packing lower bound: ceil(C(n,j) / max_coverage)."""
    num_targets = comb(n, j)
    max_cov = max_coverage_per_candidate(n, k, j, s)
    if max_cov == 0:
        return num_targets  # impossible to cover
    return ceil(num_targets / max_cov)


def best_lower_bound(n: int, k: int, j: int, s: int) -> int:
    """Best available lower bound for L(n,k,j,s)."""
    vol = volume_lower_bound(n, k, j, s)
    if s == j:
        sch = schoenheim_bound(n, k, j)
        return max(vol, sch)
    return vol


# ------------------------------------------------------------------
# LJCR known-best upper bounds for C(n, k, t)   (containment: s==j==t)
# Source: https://ljcr.dmgordon.org/cover/table.html  (2026-03-19)
# ------------------------------------------------------------------

# Format: LJCR[(n, k, t)] = best known upper bound
# Only includes n=7..25, k=4..7, t=3..7 relevant to our problem
LJCR: dict[tuple[int, int, int], int] = {
    # ---- t=3, k=4 ----
    (7, 4, 3): 12, (8, 4, 3): 14, (9, 4, 3): 25, (10, 4, 3): 30,
    (11, 4, 3): 47, (12, 4, 3): 57, (13, 4, 3): 78, (14, 4, 3): 91,
    (15, 4, 3): 124, (16, 4, 3): 140, (17, 4, 3): 183, (18, 4, 3): 207,
    (19, 4, 3): 258, (20, 4, 3): 285, (21, 4, 3): 352, (22, 4, 3): 385,
    (23, 4, 3): 466, (24, 4, 3): 510, (25, 4, 3): 600,
    # ---- t=3, k=5 ----
    (7, 5, 3): 5, (8, 5, 3): 8, (9, 5, 3): 12, (10, 5, 3): 17,
    (11, 5, 3): 20, (12, 5, 3): 29, (13, 5, 3): 34, (14, 5, 3): 43,
    (15, 5, 3): 55, (16, 5, 3): 65, (17, 5, 3): 68, (18, 5, 3): 94,
    (19, 5, 3): 108, (20, 5, 3): 133, (21, 5, 3): 151, (22, 5, 3): 172,
    (23, 5, 3): 187, (24, 5, 3): 231, (25, 5, 3): 256,
    # ---- t=3, k=6 ----
    (7, 6, 3): 4, (8, 6, 3): 4, (9, 6, 3): 7, (10, 6, 3): 10,
    (11, 6, 3): 11, (12, 6, 3): 15, (13, 6, 3): 21, (14, 6, 3): 25,
    (15, 6, 3): 31, (16, 6, 3): 38, (17, 6, 3): 44, (18, 6, 3): 48,
    (19, 6, 3): 60, (20, 6, 3): 71, (21, 6, 3): 77, (22, 6, 3): 77,
    (23, 6, 3): 104, (24, 6, 3): 116, (25, 6, 3): 130,
    # ---- t=3, k=7 ----
    (8, 7, 3): 4, (9, 7, 3): 4, (10, 7, 3): 6, (11, 7, 3): 8,
    (12, 7, 3): 11, (13, 7, 3): 13, (14, 7, 3): 15, (15, 7, 3): 15,
    (16, 7, 3): 24, (17, 7, 3): 27, (18, 7, 3): 32, (19, 7, 3): 35,
    (20, 7, 3): 45, (21, 7, 3): 49, (22, 7, 3): 59, (23, 7, 3): 65,
    (24, 7, 3): 76, (25, 7, 3): 83,
    # ---- t=4, k=5 ----
    (7, 5, 4): 9, (8, 5, 4): 20, (9, 5, 4): 30, (10, 5, 4): 51,
    (11, 5, 4): 66, (12, 5, 4): 113, (13, 5, 4): 157, (14, 5, 4): 229,
    (15, 5, 4): 294, (16, 5, 4): 404, (17, 5, 4): 491, (18, 5, 4): 664,
    (19, 5, 4): 839, (20, 5, 4): 1063, (21, 5, 4): 1246, (22, 5, 4): 1573,
    (23, 5, 4): 1771, (24, 5, 4): 2237, (25, 5, 4): 2614,
    # ---- t=4, k=6 ----
    (7, 6, 4): 5, (8, 6, 4): 7, (9, 6, 4): 12, (10, 6, 4): 20,
    (11, 6, 4): 32, (12, 6, 4): 41, (13, 6, 4): 66, (14, 6, 4): 80,
    (15, 6, 4): 117, (16, 6, 4): 152, (17, 6, 4): 188, (18, 6, 4): 236,
    (19, 6, 4): 325, (20, 6, 4): 382, (21, 6, 4): 484, (22, 6, 4): 580,
    (23, 6, 4): 716, (24, 6, 4): 784, (25, 6, 4): 992,
    # ---- t=4, k=7 ----
    (8, 7, 4): 5, (9, 7, 4): 6, (10, 7, 4): 10, (11, 7, 4): 17,
    (12, 7, 4): 24, (13, 7, 4): 30, (14, 7, 4): 44, (15, 7, 4): 57,
    (16, 7, 4): 76, (17, 7, 4): 98, (18, 7, 4): 126, (19, 7, 4): 151,
    (20, 7, 4): 198, (21, 7, 4): 235, (22, 7, 4): 252, (23, 7, 4): 253,
    (24, 7, 4): 357, (25, 7, 4): 440,
    # ---- t=5, k=6 ----
    (7, 6, 5): 6, (8, 6, 5): 12, (9, 6, 5): 30, (10, 6, 5): 50,
    (11, 6, 5): 100, (12, 6, 5): 132, (13, 6, 5): 245, (14, 6, 5): 371,
    (15, 6, 5): 578, (16, 6, 5): 808, (17, 6, 5): 1202, (18, 6, 5): 1530,
    (19, 6, 5): 2167, (20, 6, 5): 2800, (21, 6, 5): 3863, (22, 6, 5): 4659,
    (23, 6, 5): 6156, (24, 6, 5): 7084, (25, 6, 5): 9321,
    # ---- t=5, k=7 ----
    (8, 7, 5): 6, (9, 7, 5): 9, (10, 7, 5): 20, (11, 7, 5): 34,
    (12, 7, 5): 59, (13, 7, 5): 78, (14, 7, 5): 138, (15, 7, 5): 189,
    (16, 7, 5): 283, (17, 7, 5): 398, (18, 7, 5): 548, (19, 7, 5): 703,
    (20, 7, 5): 977, (21, 7, 5): 1279, (22, 7, 5): 1584, (23, 7, 5): 1948,
    (24, 7, 5): 2576, (25, 7, 5): 2952,
    # ---- t=6, k=7 ----
    (8, 7, 6): 7, (9, 7, 6): 16, (10, 7, 6): 45, (11, 7, 6): 84,
    (12, 7, 6): 176, (13, 7, 6): 264, (14, 7, 6): 501, (15, 7, 6): 817,
    (16, 7, 6): 1326, (17, 7, 6): 2048, (18, 7, 6): 3246, (19, 7, 6): 4411,
    (20, 7, 6): 6537, (21, 7, 6): 8704, (22, 7, 6): 12553, (23, 7, 6): 15820,
    (24, 7, 6): 21881, (25, 7, 6): 28187,
}


def ljcr_known_best(n: int, k: int, t: int) -> int | None:
    """Look up known best upper bound from LJCR. Returns None if not available."""
    return LJCR.get((n, k, t))


# ------------------------------------------------------------------
# Convenience: get all bounds for a parameter set
# ------------------------------------------------------------------

def get_bounds(n: int, k: int, j: int, s: int) -> dict:
    """Return all available bounds for L(n,k,j,s)."""
    result = {
        "volume_lb": volume_lower_bound(n, k, j, s),
        "lower_bound": best_lower_bound(n, k, j, s),
    }
    if s == j:
        result["schoenheim_lb"] = schoenheim_bound(n, k, j)
        known = ljcr_known_best(n, k, j)
        if known is not None:
            result["ljcr_best"] = known
    return result
