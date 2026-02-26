from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from extraction.extractor import extract_text
from phi_engine.phi_detector import detect_phi
from redaction.redactor import redact_text
from redaction.report import build_redaction_report
from redaction.synthetic import synthesize_text
from utils.file_handler import save_upload_file


UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/data/uploads")

app = FastAPI(title="HIPAA De-identification API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/deidentify")
async def deidentify_document(
    file: UploadFile = File(...),
    mode: Literal["redact", "synthetic"] = Form("redact"),
    force_ocr_pdf: bool = Form(False),
) -> dict:
    try:
        saved_path = await save_upload_file(file, UPLOAD_DIR)
        original_text, extraction_method = extract_text(saved_path, force_ocr_for_pdf=force_ocr_pdf)

        if not original_text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from document")

        entities = detect_phi(original_text)

        if mode == "synthetic":
            output_text, counts = synthesize_text(original_text, entities)
        else:
            output_text, counts = redact_text(original_text, entities)

        report = build_redaction_report(
            filename=file.filename or Path(saved_path).name,
            extraction_method=extraction_method,
            mode=mode,
            entities=entities,
            counts=counts,
        )

        return {
            "filename": file.filename,
            "mode": mode,
            "original_text": original_text,
            "deidentified_text": output_text,
            "report": report,
        }
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal error: {exc}") from exc
