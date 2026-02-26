from __future__ import annotations

from typing import Any

from faker import Faker


fake = Faker()


def _fake_value(entity_type: str) -> str:
    mapping = {
        "PERSON": fake.name,
        "PATIENT": fake.name,
        "DOCTOR": fake.name,
        "DATE_TIME": lambda: fake.date(pattern="%Y-%m-%d"),
        "DATE": lambda: fake.date(pattern="%Y-%m-%d"),
        "PHONE_NUMBER": fake.phone_number,
        "EMAIL": fake.email,
        "SSN": fake.ssn,
        "MRN": lambda: f"MRN-{fake.random_number(digits=8, fix_len=True)}",
        "LOCATION": fake.address,
    }

    generator = mapping.get(entity_type, lambda: f"[{entity_type}_REPLACED]")
    value = generator()
    return str(value).replace("\n", ", ")


def synthesize_text(text: str, entities: list[dict[str, Any]]) -> tuple[str, dict[str, int]]:
    sorted_entities = sorted(entities, key=lambda x: x["start"], reverse=True)
    counts: dict[str, int] = {}

    transformed = text
    for entity in sorted_entities:
        entity_type = entity["entity_type"]
        replacement = _fake_value(entity_type)
        start, end = entity["start"], entity["end"]

        transformed = transformed[:start] + replacement + transformed[end:]
        counts[entity_type] = counts.get(entity_type, 0) + 1

    return transformed, counts
