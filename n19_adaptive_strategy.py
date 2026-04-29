from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class N19InstanceFeatures:
    n: int
    k: int
    j: int
    s: int
    family: str
    cluster: str
    num_targets: int
    num_cands: int
    interaction_scale: int
    solution_len: int


def classify_n19_cluster(*, k: int, j: int, s: int) -> str:
    if s == j:
        if j <= 3:
            return "containment_low_j"
        if k >= 7 and j >= 5:
            return "containment_large_k"
        return "containment_balanced"
    if j == k:
        if s <= 4:
            return "jk_small_s"
        if s == k - 1:
            return "jk_near_dominating"
        return "jk_other"
    if s <= 3:
        return "general_sparse_overlap"
    if k >= 7 and j >= 5:
        return "general_large_overlap"
    return "general_balanced"


def classify_n19_family(*, j: int, k: int, s: int) -> str:
    if s == j:
        return "containment_s_eq_j"
    if j == k:
        return "j_eq_k_noncontain_medium_n"
    return "general_noncontain"


def build_n19_features(
    *,
    n: int,
    k: int,
    j: int,
    s: int,
    num_targets: int,
    num_cands: int,
    interaction_scale: int,
    solution_len: int,
) -> N19InstanceFeatures:
    return N19InstanceFeatures(
        n=int(n),
        k=int(k),
        j=int(j),
        s=int(s),
        family=classify_n19_family(j=j, k=k, s=s),
        cluster=classify_n19_cluster(k=k, j=j, s=s),
        num_targets=int(num_targets),
        num_cands=int(num_cands),
        interaction_scale=int(interaction_scale),
        solution_len=int(solution_len),
    )


def select_n19_strategy_steps(features: N19InstanceFeatures) -> list[str]:
    if features.family == "j_eq_k_noncontain_medium_n":
        return ["jk_bundle"]

    if features.family == "containment_s_eq_j":
        if features.cluster == "containment_low_j":
            return ["containment_target_drop", "containment_sat"]
        if features.cluster == "containment_large_k":
            return ["containment_orbit", "containment_sat"]
        return ["containment_target_drop", "containment_orbit", "containment_sat"]

    if features.cluster == "general_sparse_overlap":
        return ["general_target_drop", "general_sat"]
    if features.cluster == "general_large_overlap":
        return ["general_target_drop", "general_sat"]
    return ["general_target_drop", "general_sat"]
