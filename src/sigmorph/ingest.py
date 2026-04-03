from __future__ import annotations

import json
from pathlib import Path


def load_events_from_json(path: str) -> list[dict]:
    """
    Charge un fichier JSON contenant une liste d'événements.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {path}")

    data = json.loads(file_path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("Le JSON doit contenir une liste d'événements.")

    for i, event in enumerate(data):
        if not isinstance(event, dict):
            raise ValueError(f"L'événement #{i} n'est pas un objet JSON valide.")

    return data