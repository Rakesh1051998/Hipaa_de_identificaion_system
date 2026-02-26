from __future__ import annotations

from typing import List

from paddleocr import PaddleOCR


_ocr_instance: PaddleOCR | None = None


def get_ocr() -> PaddleOCR:
    global _ocr_instance
    if _ocr_instance is None:
        _ocr_instance = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
    return _ocr_instance


def extract_text_with_ocr(file_path: str) -> str:
    ocr = get_ocr()
    result = ocr.ocr(file_path, cls=True)

    lines: List[str] = []
    for block in result or []:
        for item in block or []:
            if len(item) < 2:
                continue
            text = item[1][0] if item[1] else ""
            if text:
                lines.append(text)

    return "\n".join(lines).strip()
