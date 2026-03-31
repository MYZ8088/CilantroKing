"""LJCR (La Jolla Covering Repository) 综合测试数据集

来源: https://ljcr.dmgordon.org/cover/table.html  (2026-03-19)
分类依据: Schönheim 下界 与 LJCR 值比较
  - 绝对正确 (PROVEN): Schönheim 下界 == LJCR 值 → 已证明最优
  - 可能最优 (BEST_KNOWN): Schönheim 下界 < LJCR 值 → 目前最优但未证明

本数据集覆盖参数范围: n=7..25, k=4..7, t=3..7
共 186 个 C(n,k,t) 值, 其中 49 个已证明最优, 137 个为目前最优
"""

from __future__ import annotations

# 状态标记
PROVEN = "绝对正确"       # Schönheim bound == LJCR ⟹ 已证明最优
BEST_KNOWN = "可能最优"   # Schönheim bound < LJCR ⟹ 目前最优未证明


# ---- 数据格式: (n, k, t, ljcr_value, schoenheim_bound, status, gap) ----
# gap = ljcr_value - schoenheim_bound

LJCR_DATASET: list[tuple[int, int, int, int, int, str, int]] = [
    # ==========================================================
    # t=3, k=4:  C(n,4,3)  ─  大部分已证明最优
    # ==========================================================
    ( 7, 4, 3,    12,   11, BEST_KNOWN, 1),
    ( 8, 4, 3,    14,   14, PROVEN,     0),
    ( 9, 4, 3,    25,   25, PROVEN,     0),
    (10, 4, 3,    30,   30, PROVEN,     0),
    (11, 4, 3,    47,   47, PROVEN,     0),
    (12, 4, 3,    57,   57, PROVEN,     0),
    (13, 4, 3,    78,   78, PROVEN,     0),
    (14, 4, 3,    91,   91, PROVEN,     0),
    (15, 4, 3,   124,  124, PROVEN,     0),
    (16, 4, 3,   140,  140, PROVEN,     0),
    (17, 4, 3,   183,  183, PROVEN,     0),
    (18, 4, 3,   207,  207, PROVEN,     0),
    (19, 4, 3,   258,  257, BEST_KNOWN, 1),
    (20, 4, 3,   285,  285, PROVEN,     0),
    (21, 4, 3,   352,  352, PROVEN,     0),
    (22, 4, 3,   385,  385, PROVEN,     0),
    (23, 4, 3,   466,  466, PROVEN,     0),
    (24, 4, 3,   510,  510, PROVEN,     0),
    (25, 4, 3,   600,  600, PROVEN,     0),

    # ==========================================================
    # t=3, k=5:  C(n,5,3)
    # ==========================================================
    ( 7, 5, 3,     5,    5, PROVEN,     0),
    ( 8, 5, 3,     8,    7, BEST_KNOWN, 1),
    ( 9, 5, 3,    12,   11, BEST_KNOWN, 1),
    (10, 5, 3,    17,   14, BEST_KNOWN, 3),
    (11, 5, 3,    20,   18, BEST_KNOWN, 2),
    (12, 5, 3,    29,   27, BEST_KNOWN, 2),
    (13, 5, 3,    34,   32, BEST_KNOWN, 2),
    (14, 5, 3,    43,   37, BEST_KNOWN, 6),
    (15, 5, 3,    55,   54, BEST_KNOWN, 1),
    (16, 5, 3,    65,   61, BEST_KNOWN, 4),
    (17, 5, 3,    68,   68, PROVEN,     0),
    (18, 5, 3,    94,   94, PROVEN,     0),
    (19, 5, 3,   108,  103, BEST_KNOWN, 5),
    (20, 5, 3,   133,  116, BEST_KNOWN, 17),
    (21, 5, 3,   151,  147, BEST_KNOWN, 4),
    (22, 5, 3,   172,  163, BEST_KNOWN, 9),
    (23, 5, 3,   187,  180, BEST_KNOWN, 7),
    (24, 5, 3,   231,  221, BEST_KNOWN, 10),
    (25, 5, 3,   256,  240, BEST_KNOWN, 16),

    # ==========================================================
    # t=3, k=6:  C(n,6,3)
    # ==========================================================
    ( 7, 6, 3,     4,    4, PROVEN,     0),
    ( 8, 6, 3,     4,    4, PROVEN,     0),
    ( 9, 6, 3,     7,    6, BEST_KNOWN, 1),
    (10, 6, 3,    10,    7, BEST_KNOWN, 3),
    (11, 6, 3,    11,   11, PROVEN,     0),
    (12, 6, 3,    15,   14, BEST_KNOWN, 1),
    (13, 6, 3,    21,   18, BEST_KNOWN, 3),
    (14, 6, 3,    25,   19, BEST_KNOWN, 6),
    (15, 6, 3,    31,   30, BEST_KNOWN, 1),
    (16, 6, 3,    38,   32, BEST_KNOWN, 6),
    (17, 6, 3,    44,   37, BEST_KNOWN, 7),
    (18, 6, 3,    48,   42, BEST_KNOWN, 6),
    (19, 6, 3,    60,   57, BEST_KNOWN, 3),
    (20, 6, 3,    71,   64, BEST_KNOWN, 7),
    (21, 6, 3,    77,   70, BEST_KNOWN, 7),
    (22, 6, 3,    77,   77, PROVEN,     0),
    (23, 6, 3,   104,  104, PROVEN,     0),
    (24, 6, 3,   116,  112, BEST_KNOWN, 4),
    (25, 6, 3,   130,  121, BEST_KNOWN, 9),

    # ==========================================================
    # t=3, k=7:  C(n,7,3)
    # ==========================================================
    ( 8, 7, 3,     4,    4, PROVEN,     0),
    ( 9, 7, 3,     4,    4, PROVEN,     0),
    (10, 7, 3,     6,    5, BEST_KNOWN, 1),
    (11, 7, 3,     8,    7, BEST_KNOWN, 1),
    (12, 7, 3,    11,    7, BEST_KNOWN, 4),
    (13, 7, 3,    13,   12, BEST_KNOWN, 1),
    (14, 7, 3,    15,   14, BEST_KNOWN, 1),
    (15, 7, 3,    15,   15, PROVEN,     0),
    (16, 7, 3,    24,   19, BEST_KNOWN, 5),
    (17, 7, 3,    27,   20, BEST_KNOWN, 7),
    (18, 7, 3,    32,   31, BEST_KNOWN, 1),
    (19, 7, 3,    35,   33, BEST_KNOWN, 2),
    (20, 7, 3,    45,   38, BEST_KNOWN, 7),
    (21, 7, 3,    49,   42, BEST_KNOWN, 7),
    (22, 7, 3,    59,   44, BEST_KNOWN, 15),
    (23, 7, 3,    65,   63, BEST_KNOWN, 2),
    (24, 7, 3,    76,   69, BEST_KNOWN, 7),
    (25, 7, 3,    83,   72, BEST_KNOWN, 11),

    # ==========================================================
    # t=4, k=5:  C(n,5,4)
    # ==========================================================
    ( 7, 5, 4,     9,    9, PROVEN,     0),
    ( 8, 5, 4,    20,   18, BEST_KNOWN, 2),
    ( 9, 5, 4,    30,   26, BEST_KNOWN, 4),
    (10, 5, 4,    51,   50, BEST_KNOWN, 1),
    (11, 5, 4,    66,   66, PROVEN,     0),
    (12, 5, 4,   113,  113, PROVEN,     0),
    (13, 5, 4,   157,  149, BEST_KNOWN, 8),
    (14, 5, 4,   229,  219, BEST_KNOWN, 10),
    (15, 5, 4,   294,  273, BEST_KNOWN, 21),
    (16, 5, 4,   404,  397, BEST_KNOWN, 7),
    (17, 5, 4,   491,  476, BEST_KNOWN, 15),
    (18, 5, 4,   664,  659, BEST_KNOWN, 5),
    (19, 5, 4,   839,  787, BEST_KNOWN, 52),
    (20, 5, 4,  1063, 1028, BEST_KNOWN, 35),
    (21, 5, 4,  1246, 1197, BEST_KNOWN, 49),
    (22, 5, 4,  1573, 1549, BEST_KNOWN, 24),
    (23, 5, 4,  1771, 1771, PROVEN,     0),
    (24, 5, 4,  2237, 2237, PROVEN,     0),
    (25, 5, 4,  2614, 2550, BEST_KNOWN, 64),

    # ==========================================================
    # t=4, k=6:  C(n,6,4)
    # ==========================================================
    ( 7, 6, 4,     5,    5, PROVEN,     0),
    ( 8, 6, 4,     7,    7, PROVEN,     0),
    ( 9, 6, 4,    12,   11, BEST_KNOWN, 1),
    (10, 6, 4,    20,   19, BEST_KNOWN, 1),
    (11, 6, 4,    32,   26, BEST_KNOWN, 6),
    (12, 6, 4,    41,   36, BEST_KNOWN, 5),
    (13, 6, 4,    66,   59, BEST_KNOWN, 7),
    (14, 6, 4,    80,   75, BEST_KNOWN, 5),
    (15, 6, 4,   117,   93, BEST_KNOWN, 24),
    (16, 6, 4,   152,  144, BEST_KNOWN, 8),
    (17, 6, 4,   188,  173, BEST_KNOWN, 15),
    (18, 6, 4,   236,  204, BEST_KNOWN, 32),
    (19, 6, 4,   325,  298, BEST_KNOWN, 27),
    (20, 6, 4,   382,  344, BEST_KNOWN, 38),
    (21, 6, 4,   484,  406, BEST_KNOWN, 78),
    (22, 6, 4,   580,  539, BEST_KNOWN, 41),
    (23, 6, 4,   716,  625, BEST_KNOWN, 91),
    (24, 6, 4,   784,  720, BEST_KNOWN, 64),
    (25, 6, 4,   992,  921, BEST_KNOWN, 71),

    # ==========================================================
    # t=4, k=7:  C(n,7,4)
    # ==========================================================
    ( 8, 7, 4,     5,    5, PROVEN,     0),
    ( 9, 7, 4,     6,    6, PROVEN,     0),
    (10, 7, 4,    10,    9, BEST_KNOWN, 1),
    (11, 7, 4,    17,   11, BEST_KNOWN, 6),
    (12, 7, 4,    24,   19, BEST_KNOWN, 5),
    (13, 7, 4,    30,   26, BEST_KNOWN, 4),
    (14, 7, 4,    44,   36, BEST_KNOWN, 8),
    (15, 7, 4,    57,   41, BEST_KNOWN, 16),
    (16, 7, 4,    76,   69, BEST_KNOWN, 7),
    (17, 7, 4,    98,   78, BEST_KNOWN, 20),
    (18, 7, 4,   126,   96, BEST_KNOWN, 30),
    (19, 7, 4,   151,  114, BEST_KNOWN, 37),
    (20, 7, 4,   198,  163, BEST_KNOWN, 35),
    (21, 7, 4,   235,  192, BEST_KNOWN, 43),
    (22, 7, 4,   252,  220, BEST_KNOWN, 32),
    (23, 7, 4,   253,  253, PROVEN,     0),
    (24, 7, 4,   357,  357, PROVEN,     0),
    (25, 7, 4,   440,  400, BEST_KNOWN, 40),

    # ==========================================================
    # t=5, k=6:  C(n,6,5)
    # ==========================================================
    ( 7, 6, 5,     6,    6, PROVEN,     0),
    ( 8, 6, 5,    12,   12, PROVEN,     0),
    ( 9, 6, 5,    30,   27, BEST_KNOWN, 3),
    (10, 6, 5,    50,   44, BEST_KNOWN, 6),
    (11, 6, 5,   100,   92, BEST_KNOWN, 8),
    (12, 6, 5,   132,  132, PROVEN,     0),
    (13, 6, 5,   245,  245, PROVEN,     0),
    (14, 6, 5,   371,  348, BEST_KNOWN, 23),
    (15, 6, 5,   578,  548, BEST_KNOWN, 30),
    (16, 6, 5,   808,  728, BEST_KNOWN, 80),
    (17, 6, 5,  1202, 1125, BEST_KNOWN, 77),
    (18, 6, 5,  1530, 1428, BEST_KNOWN, 102),
    (19, 6, 5,  2167, 2087, BEST_KNOWN, 80),
    (20, 6, 5,  2800, 2624, BEST_KNOWN, 176),
    (21, 6, 5,  3863, 3598, BEST_KNOWN, 265),
    (22, 6, 5,  4659, 4389, BEST_KNOWN, 270),
    (23, 6, 5,  6156, 5938, BEST_KNOWN, 218),
    (24, 6, 5,  7084, 7084, PROVEN,     0),
    (25, 6, 5,  9321, 9321, PROVEN,     0),

    # ==========================================================
    # t=5, k=7:  C(n,7,5)
    # ==========================================================
    ( 8, 7, 5,     6,    6, PROVEN,     0),
    ( 9, 7, 5,     9,    9, PROVEN,     0),
    (10, 7, 5,    20,   16, BEST_KNOWN, 4),
    (11, 7, 5,    34,   30, BEST_KNOWN, 4),
    (12, 7, 5,    59,   45, BEST_KNOWN, 14),
    (13, 7, 5,    78,   67, BEST_KNOWN, 11),
    (14, 7, 5,   138,  118, BEST_KNOWN, 20),
    (15, 7, 5,   189,  161, BEST_KNOWN, 28),
    (16, 7, 5,   283,  213, BEST_KNOWN, 70),
    (17, 7, 5,   398,  350, BEST_KNOWN, 48),
    (18, 7, 5,   548,  445, BEST_KNOWN, 103),
    (19, 7, 5,   703,  554, BEST_KNOWN, 149),
    (20, 7, 5,   977,  852, BEST_KNOWN, 125),
    (21, 7, 5,  1279, 1032, BEST_KNOWN, 247),
    (22, 7, 5,  1584, 1276, BEST_KNOWN, 308),
    (23, 7, 5,  1948, 1771, BEST_KNOWN, 177),
    (24, 7, 5,  2576, 2143, BEST_KNOWN, 433),
    (25, 7, 5,  2952, 2572, BEST_KNOWN, 380),

    # ==========================================================
    # t=6, k=7:  C(n,7,6)
    # ==========================================================
    ( 8, 7, 6,     7,    7, PROVEN,     0),
    ( 9, 7, 6,    16,   16, PROVEN,     0),
    (10, 7, 6,    45,   39, BEST_KNOWN, 6),
    (11, 7, 6,    84,   70, BEST_KNOWN, 14),
    (12, 7, 6,   176,  158, BEST_KNOWN, 18),
    (13, 7, 6,   264,  246, BEST_KNOWN, 18),
    (14, 7, 6,   501,  490, BEST_KNOWN, 11),
    (15, 7, 6,   817,  746, BEST_KNOWN, 71),
    (16, 7, 6,  1326, 1253, BEST_KNOWN, 73),
    (17, 7, 6,  2048, 1768, BEST_KNOWN, 280),
    (18, 7, 6,  3246, 2893, BEST_KNOWN, 353),
    (19, 7, 6,  4411, 3876, BEST_KNOWN, 535),
    (20, 7, 6,  6537, 5963, BEST_KNOWN, 574),
    (21, 7, 6,  8704, 7872, BEST_KNOWN, 832),
    (22, 7, 6, 12553, 11308, BEST_KNOWN, 1245),
    (23, 7, 6, 15820, 14421, BEST_KNOWN, 1399),
    (24, 7, 6, 21881, 20359, BEST_KNOWN, 1522),
    (25, 7, 6, 28187, 25300, BEST_KNOWN, 2887),
]


# ---- 便捷过滤函数 ----

def get_proven_optimal() -> list[tuple[int, int, int, int]]:
    """返回所有已证明最优的 (n, k, t, value) 列表."""
    return [(n, k, t, val) for n, k, t, val, _, status, _ in LJCR_DATASET
            if status == PROVEN]


def get_best_known() -> list[tuple[int, int, int, int, int]]:
    """返回所有可能最优的 (n, k, t, value, gap) 列表."""
    return [(n, k, t, val, gap) for n, k, t, val, _, status, gap in LJCR_DATASET
            if status == BEST_KNOWN]


def get_by_params(t: int | None = None, k: int | None = None,
                  status: str | None = None) -> list[tuple]:
    """按参数过滤数据集."""
    result = LJCR_DATASET
    if t is not None:
        result = [r for r in result if r[2] == t]
    if k is not None:
        result = [r for r in result if r[1] == k]
    if status is not None:
        result = [r for r in result if r[5] == status]
    return result


def get_small_proven(max_n: int = 15) -> list[tuple[int, int, int, int]]:
    """返回小参数的已证明最优值 (适合快速测试)."""
    return [(n, k, t, val) for n, k, t, val, _, status, _ in LJCR_DATASET
            if status == PROVEN and n <= max_n]


def summary() -> dict:
    """数据集统计摘要."""
    total = len(LJCR_DATASET)
    proven = sum(1 for *_, status, _ in LJCR_DATASET if status == PROVEN)
    best_known = total - proven
    return {
        "total": total,
        "proven_optimal": proven,
        "best_known": best_known,
        "proven_ratio": f"{proven/total:.1%}",
        "t_range": "3..6",
        "k_range": "4..7",
        "n_range": "7..25",
    }


if __name__ == "__main__":
    stats = summary()
    print(f"LJCR 测试数据集统计:")
    print(f"  总数: {stats['total']}")
    print(f"  绝对正确 (proven): {stats['proven_optimal']}")
    print(f"  可能最优 (best known): {stats['best_known']}")
    print(f"  已证明比例: {stats['proven_ratio']}")
    print()

    print("=== 绝对正确 (已证明最优) ===")
    for n, k, t, val in get_proven_optimal():
        print(f"  C({n},{k},{t}) = {val}")

    print()
    print("=== 可能最优 (目前最佳, 未证明) ===")
    for n, k, t, val, gap in get_best_known():
        print(f"  C({n},{k},{t}) = {val}  (Schönheim gap={gap})")
