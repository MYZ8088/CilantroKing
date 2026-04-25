from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from pathlib import Path


CaseKey = tuple[int, int, int, int]
ROOT = Path(__file__).resolve().parent
SPECIAL5_CACHE_FILE = ROOT / "results" / "special5_cached_groups_v1.json"


@dataclass(frozen=True)
class SpecialCaseSpec:
    n: int
    k: int
    j: int
    s: int
    baseline_blocks: int
    source_page: str

    @property
    def key(self) -> CaseKey:
        return (self.n, self.k, self.j, self.s)


_SPECIAL5_SPECS: tuple[SpecialCaseSpec, ...] = (
    SpecialCaseSpec(
        n=13,
        k=5,
        j=5,
        s=4,
        baseline_blocks=48,
        source_page="https://www.coveringrepository.com/systems.aspx?k=05&m=05&t=04",
    ),
    SpecialCaseSpec(
        n=14,
        k=6,
        j=5,
        s=4,
        baseline_blocks=29,
        source_page="https://www.coveringrepository.com/systems.aspx?k=06&m=05&t=04",
    ),
    SpecialCaseSpec(
        n=14,
        k=7,
        j=6,
        s=5,
        baseline_blocks=36,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=06&t=05",
    ),
    SpecialCaseSpec(
        n=15,
        k=6,
        j=4,
        s=3,
        baseline_blocks=14,
        source_page="https://www.coveringrepository.com/systems.aspx?k=06&m=04&t=03",
    ),
    SpecialCaseSpec(
        n=15,
        k=7,
        j=5,
        s=4,
        baseline_blocks=20,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=05&t=04",
    ),
)

_SPECIAL5_BY_KEY: dict[CaseKey, SpecialCaseSpec] = {spec.key: spec for spec in _SPECIAL5_SPECS}


def _verify_groups(*, n: int, j: int, s: int, groups: list[list[int]]) -> bool:
    group_sets = [set(g) for g in groups]
    for tgt in combinations(range(n), j):
        tset = set(tgt)
        if not any(len(tset & gset) >= s for gset in group_sets):
            return False
    return True


def _normalize_groups(n: int, k: int, groups: list[list[int]]) -> list[list[int]]:
    out: list[list[int]] = []
    for grp in groups:
        vals = [int(x) for x in grp]
        if len(vals) != k:
            raise ValueError(f"group length mismatch for {(n, k)}: {vals}")
        if len(set(vals)) != k:
            raise ValueError(f"group has duplicate elements: {vals}")
        if any(x < 0 or x >= n for x in vals):
            raise ValueError(f"group out of range [0,{n-1}]: {vals}")
        out.append(sorted(vals))
    return out


@lru_cache(maxsize=1)
def _load_cached_groups() -> dict[CaseKey, list[list[int]]]:
    if not SPECIAL5_CACHE_FILE.exists():
        return {}

    payload = json.loads(SPECIAL5_CACHE_FILE.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    if not isinstance(cases, list):
        return {}

    out: dict[CaseKey, list[list[int]]] = {}
    for row in cases:
        if not isinstance(row, dict):
            continue
        key = (
            int(row.get("n", -1)),
            int(row.get("k", -1)),
            int(row.get("j", -1)),
            int(row.get("s", -1)),
        )
        spec = _SPECIAL5_BY_KEY.get(key)
        if spec is None:
            continue
        raw_groups = row.get("groups")
        if not isinstance(raw_groups, list):
            continue
        groups = _normalize_groups(spec.n, spec.k, raw_groups)
        if not _verify_groups(n=spec.n, j=spec.j, s=spec.s, groups=groups):
            raise ValueError(f"cached groups verify failed for {key}")
        out[key] = groups
    return out


def is_special5_case(n: int, k: int, j: int, s: int) -> bool:
    return (int(n), int(k), int(j), int(s)) in _SPECIAL5_BY_KEY


def get_special5_case_spec(n: int, k: int, j: int, s: int) -> SpecialCaseSpec | None:
    return _SPECIAL5_BY_KEY.get((int(n), int(k), int(j), int(s)))


def get_special5_groups(n: int, k: int, j: int, s: int) -> list[list[int]] | None:
    key = (int(n), int(k), int(j), int(s))
    if key not in _SPECIAL5_BY_KEY:
        return None
    cached = _load_cached_groups()
    groups = cached.get(key)
    if groups is None:
        return None
    return [list(g) for g in groups]


def list_special5_keys() -> list[CaseKey]:
    return sorted(_SPECIAL5_BY_KEY.keys())
