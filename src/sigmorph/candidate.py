from __future__ import annotations

from collections import defaultdict


def extract_field_values(events: list[dict]) -> dict[str, list[str]]:
    values: dict[str, list[str]] = defaultdict(list)
    for event in events:
        for key, value in event.items():
            values[key].append(str(value))
    return dict(values)