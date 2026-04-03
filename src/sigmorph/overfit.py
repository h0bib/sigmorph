from __future__ import annotations

from .models import OverfitReport, FieldCandidate


def build_overfit_report(selected: list[FieldCandidate]) -> OverfitReport:
    reasons: list[str] = []
    suggestions: list[str] = []

    for candidate in selected:
        if candidate.field_name in {"ComputerName", "User"}:
            reasons.append(f"Rule depends on environment-specific field: {candidate.field_name}")
            suggestions.append(f"Consider removing {candidate.field_name} from the main rule")

        if candidate.field_name == "CommandLine":
            long_values = [v for v in candidate.selected_values if len(v) > 40]
            if long_values:
                reasons.append("CommandLine condition may be too specific")
                suggestions.append("Prefer stable tokens over long exact command fragments")

    risk = "low"
    if len(reasons) >= 3:
        risk = "high"
    elif len(reasons) >= 1:
        risk = "medium"

    return OverfitReport(
        risk_level=risk,
        reasons=reasons,
        suggestions=suggestions,
    )