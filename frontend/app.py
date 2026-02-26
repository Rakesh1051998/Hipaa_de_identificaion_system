from __future__ import annotations

import json
import os

import gradio as gr
import requests


BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000/deidentify")


def process_document(file_obj, mode: str, force_ocr_pdf: bool):
    if file_obj is None:
        return "", "", "Please upload a file."

    file_path = file_obj.name
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        data = {
            "mode": mode,
            "force_ocr_pdf": str(force_ocr_pdf).lower(),
        }
        response = requests.post(BACKEND_URL, files=files, data=data, timeout=300)

    if response.status_code != 200:
        return "", "", f"Error {response.status_code}: {response.text}"

    payload = response.json()
    report_str = json.dumps(payload.get("report", {}), indent=2)

    return payload.get("original_text", ""), payload.get("deidentified_text", ""), report_str


with gr.Blocks(title="HIPAA De-identification System") as demo:
    gr.Markdown("## AI-Powered HIPAA Medical De-identification System")

    with gr.Row():
        file_input = gr.File(label="Upload PDF / Image / Text")
        mode_input = gr.Radio(
            choices=["redact", "synthetic"],
            value="redact",
            label="De-identification Mode",
        )
        force_ocr_input = gr.Checkbox(label="Force OCR for PDF", value=False)

    run_btn = gr.Button("Process")

    with gr.Row():
        before_box = gr.Textbox(label="Before (Extracted Text)", lines=20)
        after_box = gr.Textbox(label="After (De-identified Text)", lines=20)

    report_box = gr.Code(label="Redaction Report (Audit Trail)", language="json")

    run_btn.click(
        fn=process_document,
        inputs=[file_input, mode_input, force_ocr_input],
        outputs=[before_box, after_box, report_box],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
