from __future__ import annotations

from .models import FieldCandidate


HIGH_VALUE_FIELDS = {"Image", "CommandLine", "ParentImage", "OriginalFileName"}
LOW_VALUE_FIELDS = {"ComputerName", "User"}


def build_candidates(events: list[dict], field_values: dict[str, list[str]]) -> list[FieldCandidate]:
    total = max(len(events), 1)
    candidates: list[FieldCandidate] = []

    for field_name, values in field_values.items():
        unique_count = len(set(values))
        presence_ratio = len(values) / total
        uniqueness_ratio = unique_count / max(len(values), 1)
        stability_score = max(0.0, min(1.0, presence_ratio * (1.0 - (uniqueness_ratio * 0.7))))

        info = 0.5
        if field_name in HIGH_VALUE_FIELDS:
            info = 0.9
        elif field_name in LOW_VALUE_FIELDS:
            info = 0.3

        candidates.append(
            FieldCandidate(
                field_name=field_name,
                raw_values=values,
                presence_ratio=round(presence_ratio, 3),
                uniqueness_ratio=round(uniqueness_ratio, 3),
                stability_score=round(stability_score, 3),
                informativeness_score=info,
            )
        )

    return candidates