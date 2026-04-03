from __future__ import annotations

SUPPORTED_FIELDS = {
    "Image",
    "CommandLine",
    "ParentImage",
    "User",
    "ComputerName",
    "EventID",
    "OriginalFileName",
    "CurrentDirectory",
}


def _norm_string(value: object) -> str:
    text = str(value).strip()
    return " ".join(text.split())


def normalize_events(events: list[dict]) -> list[dict]:
    normalized: list[dict] = []

    for event in events:
        out: dict = {}
        for key, value in event.items():
            if key not in SUPPORTED_FIELDS:
                continue
            if value is None:
                continue
            if isinstance(value, (str, int, float)):
                out[key] = _norm_string(value)
        normalized.append(out)

    return normalized