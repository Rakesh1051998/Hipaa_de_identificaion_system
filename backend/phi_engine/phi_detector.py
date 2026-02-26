from __future__ import annotations

from typing import Any

from phi_engine.patterns import detect_with_regex


try:
    from presidio_analyzer import AnalyzerEngine
except Exception:
    AnalyzerEngine = None


_analyzer: Any = None

# Entity types to ignore (common false positives in medical text)
ENTITY_BLACKLIST = {
    "IN_PAN",  # Indian PAN numbers - not relevant for US medical docs
    "AU_ABN",  # Australian Business Number
    "AU_ACN",  # Australian Company Number
    "AU_TFN",  # Australian Tax File Number
    "AU_MEDICARE",  # Australian Medicare
    "SG_NRIC_FIN",  # Singapore NRIC
}

# Common medical credential suffixes to ignore when detected as locations
MEDICAL_CREDENTIALS = {"MD", "DO", "RN", "NP", "PA", "DDS", "PharmD", "PhD"}


def get_analyzer() -> Any:
    global _analyzer
    if AnalyzerEngine is None:
        return None

    if _analyzer is None:
        _analyzer = AnalyzerEngine()
    return _analyzer


def _dedupe_entities(entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entities = sorted(entities, key=lambda x: (x["start"], -(x["end"] - x["start"])))
    merged: list[dict[str, Any]] = []

    for item in entities:
        if not merged:
            merged.append(item)
            continue

        prev = merged[-1]
        overlap = item["start"] < prev["end"]
        if overlap:
            prev_len = prev["end"] - prev["start"]
            curr_len = item["end"] - item["start"]
            if curr_len > prev_len:
                merged[-1] = item
        else:
            merged.append(item)

    return merged


def detect_phi(text: str, min_confidence: float = 0.6) -> list[dict[str, Any]]:
    """
    Detect PHI entities in text.
    
    Args:
        text: Input text to analyze
        min_confidence: Minimum confidence score (0.0-1.0) to accept detections.
                       Default 0.6 filters out most false positives.
    """
    entities: list[dict[str, Any]] = []

    analyzer = get_analyzer()
    if analyzer is not None:
        presidio_results = analyzer.analyze(text=text, language="en")
        for result in presidio_results:
            # Filter out blacklisted entity types (common false positives)
            if result.entity_type in ENTITY_BLACKLIST:
                continue
            
            # Filter out low-confidence detections to reduce false positives
            if result.score >= min_confidence:
                detected_text = text[result.start : result.end]
                
                # If entity spans newlines, truncate at first newline
                if "\n" in detected_text:
                    newline_pos = detected_text.index("\n")
                    detected_text = detected_text[:newline_pos].strip()
                    # Skip if truncated text is too short or empty
                    if len(detected_text) < 2:
                        continue
                    # Update end position
                    result_end = result.start + newline_pos
                else:
                    result_end = result.end
                
                # Skip medical credentials detected as locations
                if result.entity_type == "LOCATION" and detected_text.strip() in MEDICAL_CREDENTIALS:
                    continue
                
                entities.append(
                    {
                        "entity_type": result.entity_type,
                        "start": result.start,
                        "end": result_end,
                        "text": detected_text,
                        "score": float(result.score),
                        "source": "presidio",
                    }
                )

    entities.extend(detect_with_regex(text))

    return _dedupe_entities(entities)
