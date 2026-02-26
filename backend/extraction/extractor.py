from __future__ import annotations

from pathlib import Path

from extraction.ocr_engine import extract_text_with_ocr
from extraction.pdf_extractor import extract_pdf_text

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp"}


def extract_text(file_path: str, force_ocr_for_pdf: bool = False) -> tuple[str, str]:
    """
    Returns:
        (extracted_text, extraction_method)
    """
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        if force_ocr_for_pdf:
            return extract_text_with_ocr(file_path), "paddleocr_pdf"

        text = extract_pdf_text(file_path)
        if text:
            return text, "pymupdf_or_pdfplumber"

        return extract_text_with_ocr(file_path), "paddleocr_pdf_fallback"

    if suffix in IMAGE_EXTENSIONS:
        return extract_text_with_ocr(file_path), "paddleocr_image"

    if suffix in {".txt", ".md"}:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(), "raw_text"

    raise ValueError(f"Unsupported file extension: {suffix}")
