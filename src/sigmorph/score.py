from __future__ import annotations

from .models import RuleScore, FieldCandidate


def compute_score(selected: list[FieldCandidate], total_candidates: int) -> RuleScore:
    if not selected:
        return RuleScore(0.0, 0.0, 0.0, 1.0, 0.0)

    avg_stability = sum(c.stability_score for c in selected) / len(selected)
    avg_info = sum(c.informativeness_score for c in selected) / len(selected)

    coverage = min(1.0, len(selected) / max(total_candidates, 1) + 0.2)
    specificity = min(1.0, avg_info)
    stability = min(1.0, avg_stability)
    false_positive_risk = max(0.0, 1.0 - ((specificity * 0.6) + (stability * 0.4)))
    overall = ((coverage * 0.25) + (specificity * 0.35) + (stability * 0.40))

    return RuleScore(
        coverage_score=round(coverage, 3),
        specificity_score=round(specificity, 3),
        stability_score=round(stability, 3),
        false_positive_risk=round(false_positive_risk, 3),
        overall_score=round(overall, 3),
    )