from __future__ import annotations

from .ingest import load_events_from_json
from .normalize import normalize_events
from .candidate import extract_field_values
from .stability import build_candidates
from .generalize import select_candidates
from .sigma.builder import build_detection
from .score import compute_score
from .explain import build_explanation
from .overfit import build_overfit_report
from .models import GeneratedRule


class SigmaSynth:
    def __init__(self) -> None:
        self._events: list[dict] = []
        self._logsource: dict = {"product": "windows", "category": "process_creation"}

    def from_json(self, path: str) -> "SigmaSynth":
        self._events = load_events_from_json(path)
        return self

    def from_events(self, events: list[dict]) -> "SigmaSynth":
        self._events = events
        return self

    def for_logsource(self, product: str, category: str) -> "SigmaSynth":
        self._logsource = {"product": product, "category": category}
        return self

    def generate(self, profile: str = "balanced") -> GeneratedRule:
        if not self._events:
            raise ValueError("Aucun événement chargé.")

        normalized = normalize_events(self._events)
        field_values = extract_field_values(normalized)
        all_candidates = build_candidates(normalized, field_values)
        selected = select_candidates(all_candidates, profile)

        detection = build_detection(selected)
        score = compute_score(selected, len(all_candidates))
        explanation = build_explanation(all_candidates, selected)
        overfit = build_overfit_report(selected)

        return GeneratedRule(
            title="Auto-generated suspicious process pattern",
            logsource=self._logsource,
            detection=detection,
            level="medium",
            metadata={
                "status": "experimental",
                "profile": profile,
                "selected_fields": [c.field_name for c in selected],
            },
            explanation=explanation,
            score_data=score,
            overfit_data=overfit,
        )