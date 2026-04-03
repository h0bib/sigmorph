from __future__ import annotations

from ..models import FieldCandidate


def build_detection(candidates: list[FieldCandidate]) -> dict:
    detection: dict = {}
    condition_parts: list[str] = []

    for idx, candidate in enumerate(candidates, start=1):
        name = f"selection_{idx}"
        field = candidate.field_name

        if candidate.recommended_operator == "exact":
            value = candidate.selected_values[0] if len(candidate.selected_values) == 1 else candidate.selected_values
            detection[name] = {field: value}

        elif candidate.recommended_operator == "contains":
            key = f"{field}|contains"
            value = candidate.selected_values[0] if len(candidate.selected_values) == 1 else candidate.selected_values
            detection[name] = {key: value}

        elif candidate.recommended_operator == "endswith":
            key = f"{field}|endswith"
            suffix = candidate.selected_values[0]
            if not suffix.startswith("\\"):
                suffix = "\\" + suffix
            detection[name] = {key: suffix}

        condition_parts.append(name)

    detection["condition"] = " and ".join(condition_parts) if condition_parts else "selection_1"
    return detection