from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
import pdfplumber


def extract_text_pymupdf(file_path: str) -> str:
    text_chunks: list[str] = []
    with fitz.open(file_path) as doc:
        for page in doc:
            page_text = page.get_text("text") or ""
            if page_text.strip():
                text_chunks.append(page_text)
    return "\n".join(text_chunks).strip()


def extract_text_pdfplumber(file_path: str) -> str:
    text_chunks: list[str] = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_chunks.append(page_text)
    return "\n".join(text_chunks).strip()


def extract_pdf_text(file_path: str) -> str:
    path = Path(file_path)
    if path.suffix.lower() != ".pdf":
        raise ValueError("extract_pdf_text expects a PDF file")

    text = extract_text_pymupdf(file_path)
    if text:
        return text

    return extract_text_pdfplumber(file_path)
