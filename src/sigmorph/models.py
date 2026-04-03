from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
import yaml


@dataclass
class FieldCandidate:
    field_name: str
    raw_values: list[str]
    presence_ratio: float
    uniqueness_ratio: float
    stability_score: float
    informativeness_score: float
    recommended_operator: str | None = None
    selected_values: list[str] = field(default_factory=list)


@dataclass
class RuleScore:
    coverage_score: float
    specificity_score: float
    stability_score: float
    false_positive_risk: float
    overall_score: float


@dataclass
class OverfitReport:
    risk_level: str
    reasons: list[str]
    suggestions: list[str]


@dataclass
class GeneratedRule:
    title: str
    logsource: dict[str, Any]
    detection: dict[str, Any]
    level: str
    metadata: dict[str, Any]
    explanation: dict[str, Any]
    score_data: RuleScore
    overfit_data: OverfitReport

    def dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "logsource": self.logsource,
            "detection": self.detection,
            "level": self.level,
            "metadata": self.metadata,
        }

    def yaml(self) -> str:
        return yaml.safe_dump(self.dict(), sort_keys=False, allow_unicode=True)

    def explain(self) -> dict[str, Any]:
        return self.explanation

    def score(self) -> dict[str, Any]:
        return asdict(self.score_data)

    def overfit_report(self) -> dict[str, Any]:
        return asdict(self.overfit_data)