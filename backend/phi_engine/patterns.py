from __future__ import annotations

import re

CUSTOM_PATTERNS = {
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    # Phone patterns: (555) 123-4567 or 555-123-4567
    "PHONE_NUMBER": re.compile(
        r"(?:\(\d{3}\)\s*\d{3}[-.\s]?\d{4}|\b\d{3}[-.\s]\d{3}[-.\s]\d{4})\b"
    ),
    "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "MRN": re.compile(r"\b(?:MRN|Medical\s*Record\s*Number)[:\s-]*([A-Za-z0-9-]{5,20})\b", re.IGNORECASE),
    "DATE": re.compile(
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4})\b",
        re.IGNORECASE,
    ),
}


def detect_with_regex(text: str) -> list[dict]:
    entities: list[dict] = []
    for entity_type, pattern in CUSTOM_PATTERNS.items():
        for match in pattern.finditer(text):
            entities.append(
                {
                    "entity_type": entity_type,
                    "start": match.start(),
                    "end": match.end(),
                    "text": match.group(0),
                    "score": 0.95,
                    "source": "regex",
                }
            )
    return entities
