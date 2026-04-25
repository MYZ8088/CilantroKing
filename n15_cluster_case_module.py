from __future__ import annotations

from dataclasses import dataclass


CaseKey = tuple[int, int, int, int]


@dataclass(frozen=True)
class N15CaseSpec:
    n: int
    k: int
    j: int
    s: int
    baseline_blocks: int
    source_page: str

    @property
    def key(self) -> CaseKey:
        return (self.n, self.k, self.j, self.s)

    @property
    def family(self) -> str:
        if self.s == self.j:
            return "containment_s_eq_j"
        if self.j == self.k:
            return "j_eq_k_noncontain_medium_n"
        return "general_noncontain"

    @property
    def quality_limit_110(self) -> int:
        return int(self.baseline_blocks * 1.10 + 1e-9)


_N15_CASES: tuple[N15CaseSpec, ...] = (
    N15CaseSpec(
        n=13,
        k=6,
        j=6,
        s=5,
        baseline_blocks=61,
        source_page="https://www.coveringrepository.com/systems.aspx?k=06&m=06&t=05",
    ),
    N15CaseSpec(
        n=13,
        k=7,
        j=7,
        s=6,
        baseline_blocks=61,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=07&t=06",
    ),
    N15CaseSpec(
        n=14,
        k=5,
        j=5,
        s=4,
        baseline_blocks=69,
        source_page="https://www.coveringrepository.com/systems.aspx?k=05&m=05&t=04",
    ),
    N15CaseSpec(
        n=14,
        k=6,
        j=4,
        s=4,
        baseline_blocks=80,
        source_page="https://www.coveringrepository.com/systems.aspx?k=06&m=04&t=04",
    ),
    N15CaseSpec(
        n=14,
        k=6,
        j=6,
        s=5,
        baseline_blocks=98,
        source_page="https://www.coveringrepository.com/systems.aspx?k=06&m=06&t=05",
    ),
    N15CaseSpec(
        n=14,
        k=7,
        j=5,
        s=5,
        baseline_blocks=138,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=05&t=05",
    ),
    N15CaseSpec(
        n=14,
        k=7,
        j=6,
        s=6,
        baseline_blocks=501,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=06&t=06",
    ),
    N15CaseSpec(
        n=14,
        k=7,
        j=7,
        s=6,
        baseline_blocks=100,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=07&t=06",
    ),
    N15CaseSpec(
        n=15,
        k=6,
        j=4,
        s=4,
        baseline_blocks=117,
        source_page="https://www.coveringrepository.com/systems.aspx?k=06&m=04&t=04",
    ),
    N15CaseSpec(
        n=15,
        k=6,
        j=5,
        s=4,
        baseline_blocks=40,
        source_page="https://www.coveringrepository.com/systems.aspx?k=06&m=05&t=04",
    ),
    N15CaseSpec(
        n=15,
        k=6,
        j=6,
        s=5,
        baseline_blocks=142,
        source_page="https://www.coveringrepository.com/systems.aspx?k=06&m=06&t=05",
    ),
    N15CaseSpec(
        n=15,
        k=7,
        j=5,
        s=5,
        baseline_blocks=189,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=05&t=05",
    ),
    N15CaseSpec(
        n=15,
        k=7,
        j=6,
        s=5,
        baseline_blocks=58,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=06&t=05",
    ),
    N15CaseSpec(
        n=15,
        k=7,
        j=6,
        s=6,
        baseline_blocks=817,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=06&t=06",
    ),
    N15CaseSpec(
        n=15,
        k=7,
        j=7,
        s=6,
        baseline_blocks=180,
        source_page="https://www.coveringrepository.com/systems.aspx?k=07&m=07&t=06",
    ),
)

_N15_CASE_BY_KEY: dict[CaseKey, N15CaseSpec] = {spec.key: spec for spec in _N15_CASES}


def is_n15_target_case(n: int, k: int, j: int, s: int) -> bool:
    return (int(n), int(k), int(j), int(s)) in _N15_CASE_BY_KEY


def get_n15_case_spec(n: int, k: int, j: int, s: int) -> N15CaseSpec | None:
    return _N15_CASE_BY_KEY.get((int(n), int(k), int(j), int(s)))


def list_n15_target_specs() -> list[N15CaseSpec]:
    return list(_N15_CASES)


def cluster_strategy_label(spec: N15CaseSpec, gap_ratio: float) -> str:
    if gap_ratio > 0.18:
        band = "severe"
    elif gap_ratio > 0.12:
        band = "medium"
    else:
        band = "edge"
    return f"{spec.family}__{band}"


def method_hint_from_coveringrepo(spec: N15CaseSpec) -> str:
    if spec.family == "j_eq_k_noncontain_medium_n":
        return "orbit+domset+deep-search（借鉴 history 中 local-search / dynamic-programming / iterative SAT 思路）"
    if spec.family == "containment_s_eq_j":
        return "shrink+block-weight+iterative SAT（借鉴 WSC 手册中的 shrinking / weight / deep search 线索）"
    return "two-stage local-search + SAT polish（借鉴局部搜索+后处理组合）"

