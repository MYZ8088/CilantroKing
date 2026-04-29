from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
KNOWN_DESIGNS_DIR = ROOT / "known_designs"


@dataclass(frozen=True)
class Special5CaseSpec:
    n: int
    k: int
    j: int
    s: int
    source_file: str
    baseline_blocks: int


_HARDCODED_GROUPS: dict[tuple[int, int, int, int], list[list[int]]] = {
    (13, 5, 5, 4): [
        [0, 3, 4, 7, 12], [0, 3, 6, 10, 11], [2, 4, 5, 7, 12], [1, 3, 4, 5, 12],
        [1, 7, 10, 11, 12], [1, 4, 6, 9, 10], [1, 2, 3, 7, 10], [1, 7, 8, 9, 12],
        [1, 2, 5, 6, 12], [1, 4, 7, 8, 11], [0, 3, 7, 8, 10], [0, 2, 7, 9, 11],
        [3, 5, 6, 7, 12], [4, 6, 8, 10, 12], [1, 3, 5, 8, 10], [0, 4, 5, 6, 11],
        [2, 4, 5, 8, 9], [0, 5, 9, 10, 12], [3, 4, 5, 10, 11], [0, 2, 6, 7, 12],
        [2, 5, 6, 10, 11], [3, 5, 7, 9, 11], [2, 3, 9, 10, 12], [0, 1, 3, 6, 12],
        [0, 1, 2, 8, 10], [2, 3, 8, 11, 12], [2, 3, 4, 6, 11], [0, 2, 4, 10, 11],
        [0, 5, 8, 11, 12], [2, 5, 7, 8, 10], [1, 2, 5, 9, 11], [1, 6, 7, 8, 11],
        [0, 1, 3, 9, 11], [4, 6, 7, 9, 10], [0, 1, 5, 7, 10], [4, 6, 9, 11, 12],
        [0, 3, 4, 8, 9], [0, 1, 2, 4, 12], [0, 2, 6, 8, 9], [1, 4, 6, 7, 9],
        [0, 2, 3, 5, 9], [7, 8, 9, 10, 11], [3, 5, 6, 8, 9], [1, 2, 3, 6, 8],
        [0, 4, 5, 6, 8], [2, 3, 4, 7, 8], [0, 2, 6, 7, 9], [1, 2, 3, 6, 11],
        [1, 2, 3, 4, 10], [0, 1, 5, 7, 9],
    ],
    (14, 6, 5, 4): [
        [2, 5, 6, 8, 10, 13], [0, 2, 6, 7, 12, 13], [3, 4, 5, 7, 12, 13], [2, 4, 5, 7, 9, 10],
        [0, 3, 6, 7, 8, 9], [0, 3, 4, 8, 10, 13], [1, 4, 7, 9, 11, 12], [2, 3, 6, 7, 10, 11],
        [0, 5, 7, 8, 10, 12], [0, 2, 8, 9, 10, 11], [0, 1, 5, 9, 12, 13], [0, 1, 4, 6, 10, 12],
        [1, 2, 4, 6, 8, 9], [1, 3, 6, 8, 11, 13], [1, 4, 5, 6, 7, 8], [2, 3, 4, 9, 11, 13],
        [1, 2, 3, 7, 8, 12], [4, 7, 8, 9, 12, 13], [0, 1, 2, 3, 4, 5], [0, 5, 6, 9, 11, 13],
        [0, 4, 5, 7, 8, 11], [0, 2, 3, 4, 11, 12], [3, 5, 6, 9, 10, 12], [4, 5, 6, 10, 11, 13],
        [1, 3, 5, 9, 10, 11], [2, 5, 6, 8, 11, 12], [1, 2, 4, 10, 12, 13], [1, 8, 10, 11, 12, 13],
        [0, 1, 2, 7, 11, 13], [3, 4, 5, 8, 9, 12], [1, 3, 7, 9, 10, 13],
    ],
    (14, 7, 6, 5): [
        [0, 1, 3, 7, 11, 12, 13], [0, 1, 5, 6, 7, 8, 11], [0, 1, 2, 7, 8, 9, 10], [0, 4, 5, 8, 9, 11, 12],
        [0, 1, 2, 3, 4, 5, 6], [0, 2, 3, 5, 7, 9, 12], [1, 4, 6, 8, 10, 11, 13], [1, 2, 3, 6, 7, 10, 13],
        [3, 5, 6, 7, 9, 10, 11], [2, 3, 4, 9, 10, 12, 13], [2, 5, 6, 7, 8, 12, 13], [0, 2, 6, 10, 11, 12, 13],
        [0, 1, 3, 4, 9, 10, 11], [7, 8, 9, 10, 11, 12, 13], [0, 3, 5, 8, 9, 10, 13], [2, 3, 4, 7, 8, 11, 13],
        [0, 2, 3, 6, 8, 9, 11], [2, 4, 5, 6, 8, 9, 10], [0, 1, 2, 4, 8, 12, 13], [1, 2, 4, 6, 7, 9, 11],
        [0, 3, 4, 6, 7, 8, 10], [1, 4, 5, 7, 10, 12, 13], [0, 2, 4, 5, 7, 10, 11], [3, 4, 5, 6, 11, 12, 13],
        [1, 3, 5, 6, 8, 9, 13], [0, 1, 5, 6, 9, 10, 12], [0, 4, 5, 6, 7, 9, 13], [0, 1, 3, 5, 8, 10, 12],
        [0, 1, 4, 6, 7, 9, 12], [2, 6, 7, 8, 10, 11, 12], [1, 3, 4, 7, 8, 9, 12], [1, 2, 5, 9, 11, 12, 13],
        [2, 3, 4, 6, 10, 11, 12], [1, 2, 3, 5, 8, 10, 11], [1, 3, 6, 8, 9, 12, 13], [0, 1, 2, 5, 9, 11, 13],
        [1, 3, 4, 5, 7, 8, 12], [2, 4, 5, 7, 9, 10, 11],
    ],
    (15, 6, 4, 3): [
        [0, 6, 7, 8, 9, 10], [2, 4, 9, 10, 13, 14], [0, 1, 3, 10, 12, 13], [3, 5, 7, 9, 11, 13],
        [3, 4, 6, 7, 10, 12], [1, 4, 6, 8, 11, 13], [2, 7, 8, 11, 12, 14], [1, 2, 5, 6, 9, 12],
        [0, 1, 4, 5, 7, 14], [0, 1, 2, 3, 6, 13], [1, 2, 5, 10, 11, 14], [0, 4, 8, 9, 11, 12],
        [0, 5, 6, 8, 13, 14], [2, 3, 8, 9, 11, 14], [1, 3, 4, 5, 8, 12],
    ],
    (15, 7, 5, 4): [
        [0, 1, 2, 3, 4, 6, 7], [3, 4, 6, 8, 10, 11, 14], [0, 2, 3, 9, 10, 11, 12], [0, 3, 4, 7, 9, 13, 14],
        [1, 2, 6, 9, 11, 13, 14], [0, 2, 5, 8, 10, 13, 14], [2, 4, 5, 6, 7, 8, 9], [0, 5, 6, 7, 8, 10, 11],
        [1, 2, 3, 5, 11, 12, 14], [1, 3, 5, 6, 7, 10, 13], [2, 4, 7, 10, 11, 12, 13], [2, 3, 7, 8, 12, 13, 14],
        [0, 4, 5, 7, 11, 12, 14], [1, 3, 7, 8, 9, 11, 12], [0, 1, 4, 8, 11, 12, 13], [0, 1, 5, 8, 9, 10, 14],
        [1, 2, 6, 8, 10, 12, 14], [0, 3, 5, 6, 9, 12, 13], [3, 4, 5, 8, 9, 10, 13], [1, 4, 7, 9, 10, 12, 14],
        [1, 4, 5, 6, 10, 12, 13], [0, 4, 5, 6, 7, 9, 11],
    ],
}

_FILE_BACKED_SPECS: dict[tuple[int, int, int, int], str] = {
    (12, 5, 4, 3): "n12/12,05,03,04 combs.txt",
    (12, 6, 4, 3): "n12/12,06,03,04 combs.txt",
    (12, 6, 5, 4): "n12/12,06,04,05 combs.txt",
    (12, 7, 4, 4): "n12/12,07,04,04 combs.txt",
    (12, 7, 5, 4): "n12/12,07,04,05 combs.txt",
    (13, 4, 3, 3): "n13/13,04,03,03 combs.txt",
    (13, 5, 4, 3): "n13/13,05,03,04 combs.txt",
    (13, 5, 5, 3): "n13/13,05,03,05 combs.txt",
    (13, 6, 3, 3): "n13/13,06,03,03 combs.txt",
    (13, 6, 4, 3): "n13/13,06,03,04 combs.txt",
    (13, 6, 4, 4): "n13/13,06,04,04 combs.txt",
    (13, 6, 5, 4): "n13/13,06,04,05 combs.txt",
    (13, 6, 6, 4): "n13/13,06,04,06 combs.txt",
    (13, 6, 6, 5): "n13/13,06,05,06 combs.txt",
    (13, 7, 7, 5): "n13/13,07,05,07 combs.txt",
    (13, 7, 7, 6): "n13/13,07,06,07 combs.txt",
    (14, 5, 5, 3): "n14/14,05,03,05 combs.txt",
    (14, 6, 4, 3): "n14/14,06,03,04 combs.txt",
    (14, 6, 4, 4): "n14/14,06,04,04 combs.txt",
    (14, 6, 6, 4): "n14/14,06,04,06 combs.txt",
    (14, 6, 6, 5): "n14/14,06,05,06 combs.txt",
    (14, 7, 4, 3): "n14/14,07,03,04 combs.txt",
    (14, 7, 5, 5): "n14/14,07,05,05 combs.txt",
    (14, 7, 6, 4): "n14/14,07,04,06 combs.txt",
    (14, 7, 6, 6): "n14/14,07,06,06 combs.txt",
    (14, 7, 7, 6): "n14/14,07,06,07 combs.txt",
    (15, 6, 6, 5): "n15/15,06,05,06 combs.txt",
    (15, 7, 6, 4): "n15/15,07,04,06 combs.txt",
}


@lru_cache(maxsize=1)
def _canonical_baselines() -> dict[tuple[int, int, int, int], int]:
    candidates = [
        ROOT / "coveringrepo_n_lt_26_baselines(1).json",
        ROOT / "results" / "coveringrepo_n_lt_26_baselines.json",
        ROOT / "results" / "n_le_15_all_legal_baselines_filled_v1.json",
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
    baseline_map: dict[tuple[int, int, int, int], int] = {}
    for case in cases:
        if not isinstance(case, dict):
            continue
        try:
            key = (int(case["n"]), int(case["k"]), int(case["j"]), int(case["s"]))
            baseline_map[key] = int(case["baseline_blocks"])
        except Exception:
            continue
    return baseline_map


def _baseline_blocks_for(key: tuple[int, int, int, int]) -> int:
    baseline = _canonical_baselines().get(key)
    if baseline is None:
        groups = _HARDCODED_GROUPS.get(key)
        if groups is not None:
            return len(groups)
        filename = _FILE_BACKED_SPECS.get(key)
        if filename is not None:
            loaded = _load_file_backed_groups(filename)
            if loaded is not None:
                return len(loaded)
        raise KeyError(f"Missing baseline for special case {key}")
    return baseline


def _load_file_backed_groups(filename: str) -> list[list[int]] | None:
    path = KNOWN_DESIGNS_DIR / filename
    if not path.exists():
        return None
    groups: list[list[int]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        groups.append([int(part) - 1 for part in line.split()])
    return groups or None


def list_special5_keys() -> list[tuple[int, int, int, int]]:
    return sorted(set(_HARDCODED_GROUPS) | set(_FILE_BACKED_SPECS))


def get_special5_case_spec(n: int, k: int, j: int, s: int) -> Special5CaseSpec | None:
    key = (int(n), int(k), int(j), int(s))
    if key in _HARDCODED_GROUPS:
        return Special5CaseSpec(
            n=key[0],
            k=key[1],
            j=key[2],
            s=key[3],
            source_file="embedded",
            baseline_blocks=_baseline_blocks_for(key),
        )
    filename = _FILE_BACKED_SPECS.get(key)
    if filename is None:
        return None
    return Special5CaseSpec(
        n=key[0],
        k=key[1],
        j=key[2],
        s=key[3],
        source_file=f"known_designs/{filename}",
        baseline_blocks=_baseline_blocks_for(key),
    )


def get_special5_groups(n: int, k: int, j: int, s: int) -> list[list[int]] | None:
    key = (int(n), int(k), int(j), int(s))
    groups = _HARDCODED_GROUPS.get(key)
    if groups is not None:
        return [list(group) for group in groups]
    filename = _FILE_BACKED_SPECS.get(key)
    if filename is None:
        return None
    return _load_file_backed_groups(filename)
