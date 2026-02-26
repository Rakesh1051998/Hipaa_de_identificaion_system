from __future__ import annotations

from typing import Any


def redact_text(text: str, entities: list[dict[str, Any]]) -> tuple[str, dict[str, int]]:
    # Replace from end to start to preserve offsets
    sorted_entities = sorted(entities, key=lambda x: x["start"], reverse=True)
    counts: dict[str, int] = {}

    redacted_text = text
    for entity in sorted_entities:
        entity_type = entity["entity_type"]
        placeholder = f"[{entity_type}]"
        start, end = entity["start"], entity["end"]

        redacted_text = redacted_text[:start] + placeholder + redacted_text[end:]
        counts[entity_type] = counts.get(entity_type, 0) + 1

    return redacted_text, counts
