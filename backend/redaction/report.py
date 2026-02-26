from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_redaction_report(
    filename: str,
    extraction_method: str,
    mode: str,
    entities: list[dict[str, Any]],
    counts: dict[str, int],
) -> dict[str, Any]:
    return {
        "filename": filename,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "extraction_method": extraction_method,
        "operation_mode": mode,
        "total_entities_detected": len(entities),
        "entities_by_type": counts,
        "detected_entities_preview": [
            {
                "entity_type": e["entity_type"],
                "text": e["text"],
                "source": e.get("source", "unknown"),
                "score": e.get("score", None),
            }
            for e in entities[:50]
        ],
    }
