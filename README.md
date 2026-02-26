# 🏥 HIPAA Medical De-identification System

**Automatically remove Protected Health Information (PHI) from medical documents**

Transform raw clinical documents into HIPAA-compliant, de-identified versions safe for research and AI training.

## ✨ Features

- 🔍 **Smart PHI Detection** - Identifies Names, Dates, SSN, MRN, Phone Numbers, Emails, Locations
- 📄 **Multi-Format Support** - Text, PDFs, Scanned Documents, Images
- 🔒 **Dual Protection Modes** - Redact with placeholders OR replace with synthetic data
- 📊 **Audit Trail** - Complete reporting of all detected and removed PHI
- 🖥️ **Web Interface** - Easy-to-use UI showing before/after comparison
- 🐳 **Docker Ready** - One-command deployment

---

## 🚀 Quick Start

### 1. Start the System
```bash
cd /home/CUB/Quanteon/hipaa-deid-system
docker compose up --build
```

### 2. Access the Application
- **Web UI:** http://localhost:7860
- **API Docs:** http://localhost:8000/docs

### 3. Upload & Process
1. Upload a medical document (TXT, PDF, or Image)
2. Choose mode: **Redact** (placeholders) or **Synthetic** (fake data)
3. Click "Process Document"
4. View results: Original text, De-identified text, and Audit Report

---

## 📋 How It Works

```
┌─────────────────┐
│  Upload File    │  (TXT, PDF, Image)
└────────┬────────┘
         ↓
┌────────────────────────────────┐
│  Text Extraction               │
│  • Digital PDF → PyMuPDF       │
│  • Scanned PDF → PaddleOCR     │
│  • Images → PaddleOCR          │
└────────┬───────────────────────┘
         ↓
┌────────────────────────────────┐
│  PHI Detection                 │
│  • Names, Dates, SSN, MRN      │
│  • Phone, Email, Location      │
│  • Using Presidio + Regex      │
└────────┬───────────────────────┘
         ↓
┌────────────────────────────────┐
│  De-identification             │
│  • Redact Mode: [PERSON]       │
│  • Synthetic Mode: Fake Data   │
└────────┬───────────────────────┘
         ↓
┌────────────────────────────────┐
│  Results + Audit Report        │
│  • Before/After Comparison     │
│  • Entity Counts & Confidence  │
└────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
hipaa-deid-system/
├── backend/               # FastAPI application
│   ├── api/              # REST endpoints
│   ├── extraction/       # PDF & OCR engines
│   ├── phi_engine/       # PHI detection logic
│   ├── redaction/        # De-identification modules
│   └── utils/            # File handling
│
├── frontend/             # Gradio web interface
│   └── app.py
│
├── data/                 # Sample medical notes
└── docker-compose.yml    # Container orchestration
```

---

## 🔌 API Usage

### De-identify Document

**Endpoint:** `POST /deidentify`

**Parameters:**
| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `file` | File | - | Medical document (TXT/PDF/Image) |
| `mode` | String | `redact` or `synthetic` | De-identification method |
| `force_ocr_pdf` | Boolean | `true`/`false` | Force OCR on PDFs (optional) |

**Example:**
```bash
curl -X POST http://localhost:8000/deidentify \
  -F "file=@medical_note.txt" \
  -F "mode=redact"
```

**Response:**
```json
{
  "original_text": "Patient Name: John Smith...",
  "deidentified_text": "Patient Name: [PERSON]...",
  "report": {
    "total_entities_detected": 17,
    "entities_by_type": {
      "PERSON": 3,
      "DATE_TIME": 8,
      "PHONE_NUMBER": 2,
      "SSN": 1,
      "MRN": 1
    },
    "extraction_method": "raw_text",
    "timestamp_utc": "2026-02-26T05:48:37.321038+00:00"
  }
}
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | REST API server |
| **PHI Detection** | Microsoft Presidio + Regex | Entity recognition |
| **OCR Engine** | PaddleOCR | Scanned document processing |
| **PDF Parser** | PyMuPDF, pdfplumber | Digital PDF text extraction |
| **Synthetic Data** | Faker | Realistic fake data generation |
| **Frontend** | Gradio | Web interface |
| **Deployment** | Docker Compose | Container orchestration |

---

## 📊 Example Results

### Original Text:
```
Patient Name: John Smith
Date of Birth: 03/15/1975
Medical Record Number: MRN-87654321
Social Security Number: 123-45-6789
Phone: (555) 123-4567
Email: john.smith@email.com
```

### Redaction Mode:
```
Patient Name: [PERSON]
Date of Birth: [DATE_TIME]
Medical Record Number: [MRN]
Social Security Number: [SSN]
Phone: [PHONE_NUMBER]
Email: [EMAIL_ADDRESS]
```

### Synthetic Mode:
```
Patient Name: Robert Griffith
Date of Birth: 1993-12-23
Medical Record Number: MRN-16801209
Social Security Number: 594-98-3095
Phone: 9485303432
Email: robert.griffith@example.com
```

---

## 🎯 Key Features Explained

### 🔍 PHI Detection
- **HIPAA Identifiers:** Names, Dates, SSN, MRN, Phone, Email, Locations
- **Technology:** Presidio NER + Custom Regex patterns
- **Accuracy:** Confidence threshold filtering + Medical context awareness
- **No False Positives:** Filters medical terms and credentials (MD, RN, etc.)

### 📄 Multi-Format Support
- **Text Files:** Direct processing (.txt, .md)
- **Digital PDFs:** Fast text extraction with PyMuPDF
- **Scanned PDFs:** Automatic OCR fallback with PaddleOCR
- **Images:** Full OCR support (.jpg, .png, .tiff, .bmp)

### 🔒 De-identification Modes
1. **Redact Mode:** Replace PHI with type-specific placeholders
   - Preserves document structure
   - Easy manual verification
   
2. **Synthetic Mode:** Replace with realistic fake data
   - Maintains clinical context
   - Preserves narrative flow
   - Uses Faker library for authenticity

---

## 🐳 Docker Deployment

### Requirements
- Docker Engine 20.10+
- Docker Compose 2.0+

### Commands
```bash
# Start services
docker compose up --build

# Stop services
docker compose down

# View logs
docker logs hipaa_deid_backend
docker logs hipaa_deid_frontend

# Rebuild from scratch
docker compose down -v
docker compose build --no-cache
docker compose up
```

### Services
- **Backend:** Port 8000 (FastAPI)
- **Frontend:** Port 7860 (Gradio)

---

## 📝 Environment Configuration

Copy the example environment file:
```bash
cp .env.example .env
```

Available settings:
```bash
BACKEND_URL=http://backend:8000/deidentify
LOG_LEVEL=INFO
```

---

## 🔒 HIPAA Compliance

This system handles key HIPAA identifiers per 45 CFR § 164.514(b)(2):

✅ Names  
✅ Dates (birth dates, admission dates, etc.)  
✅ Telephone numbers  
✅ Email addresses  
✅ Social Security numbers  
✅ Medical record numbers  
✅ Geographic locations (cities, states)  

**Note:** This is a prototype for evaluation. For production HIPAA compliance, additional security measures, access controls, and audit logging are required.

---

## 📚 Additional Documentation


- **API Documentation:** http://localhost:8000/docs (when running)


