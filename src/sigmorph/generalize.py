from __future__ import annotations

from .models import FieldCandidate


NOISY_FIELDS = {"ComputerName", "User", "EventID", "CurrentDirectory"}


def _common_contains(values: list[str]) -> list[str]:
    tokens = []
    interesting = [
        "-enc",
        "EncodedCommand",
        "powershell",
        "cmd.exe",
        "rundll32",
        "mshta",
        "wscript",
    ]
    joined = " || ".join(v.lower() for v in values)
    for token in interesting:
        if token.lower() in joined:
            tokens.append(token)
    return tokens


def _path_to_filename(value: str) -> str:
    value = value.replace("/", "\\")
    return value.split("\\")[-1]


def choose_operator(candidate: FieldCandidate, profile: str) -> FieldCandidate:
    values = candidate.raw_values
    unique_values = sorted(set(values))

    if candidate.field_name in {"Image", "ParentImage"}:
        lower = [v.lower() for v in unique_values]
        if len(lower) == 1:
            candidate.recommended_operator = "endswith"
            candidate.selected_values = [_path_to_filename(lower[0])]
            return candidate

    if candidate.field_name == "CommandLine":
        contains = _common_contains(values)
        if contains:
            candidate.recommended_operator = "contains"
            candidate.selected_values = contains
            return candidate

    if len(unique_values) == 1:
        candidate.recommended_operator = "exact"
        candidate.selected_values = unique_values
        return candidate

    if profile == "strict":
        candidate.recommended_operator = None
        candidate.selected_values = []
        return candidate

    candidate.recommended_operator = "exact"
    candidate.selected_values = unique_values[:2]
    return candidate


def select_candidates(candidates: list[FieldCandidate], profile: str) -> list[FieldCandidate]:
    thresholds = {
        "strict": 0.60,
        "balanced": 0.45,
        "broad": 0.30,
    }
    threshold = thresholds.get(profile, 0.45)

    selected: list[FieldCandidate] = []
    for candidate in candidates:
        if candidate.field_name in NOISY_FIELDS:
            continue

        score = (candidate.stability_score * 0.6) + (candidate.informativeness_score * 0.4)
        if score < threshold:
            continue

        chosen = choose_operator(candidate, profile)
        if chosen.recommended_operator and chosen.selected_values:
            selected.append(chosen)

    return selected