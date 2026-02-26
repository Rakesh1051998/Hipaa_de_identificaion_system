from __future__ import annotations

import os
import uuid
from pathlib import Path

from fastapi import UploadFile


ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp", ".txt", ".md"}


def ensure_upload_dir(upload_dir: str) -> str:
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    return upload_dir


def _safe_filename(filename: str) -> str:
    base = os.path.basename(filename)
    return base.replace(" ", "_")


def validate_extension(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")
    return suffix


async def save_upload_file(upload_file: UploadFile, upload_dir: str) -> str:
    ensure_upload_dir(upload_dir)

    original_name = upload_file.filename or "uploaded_file"
    validate_extension(original_name)

    safe_name = _safe_filename(original_name)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    file_path = str(Path(upload_dir) / unique_name)

    with open(file_path, "wb") as f:
        content = await upload_file.read()
        f.write(content)

    return file_path
