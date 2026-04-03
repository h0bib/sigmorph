from __future__ import annotations

from .models import FieldCandidate


def build_explanation(all_candidates: list[FieldCandidate], selected: list[FieldCandidate]) -> dict:
    selected_names = {c.field_name for c in selected}
    kept = []
    discarded = []

    for candidate in selected:
        kept.append(
            {
                "field": candidate.field_name,
                "operator": candidate.recommended_operator,
                "values": candidate.selected_values,
                "stability_score": candidate.stability_score,
                "informativeness_score": candidate.informativeness_score,
            }
        )

    for candidate in all_candidates:
        if candidate.field_name in selected_names:
            continue
        discarded.append(
            {
                "field": candidate.field_name,
                "reason": "insufficient stability, low informativeness, or noisy field",
                "stability_score": candidate.stability_score,
                "informativeness_score": candidate.informativeness_score,
            }
        )

    return {
        "kept_fields": kept,
        "discarded_fields": discarded,
    }