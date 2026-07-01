# ForensIQ
[![pipeline status](https://code.swecha.org/akhil08/forensiq/badges/main/pipeline.svg)](https://code.swecha.org/akhil08/forensiq/-/commits/main)

### Offline Investigation Intelligence Platform

> **A hundred eyes. One truth.**

ForensIQ is an **offline-first, CPU-optimized AI platform** that transforms unstructured criminal investigation data into structured, connected investigation intelligence. It enables investigators to process case files without relying on cloud services, ensuring privacy, security, and usability even in air-gapped environments.

---

## 🚨 Problem Statement

Modern investigations involve hundreds of scattered documents and evidence sources, including:

- FIRs
- Witness statements
- Forensic reports
- Medical reports
- Crime scene photographs
- Officer voice notes
- Scanned evidence documents

Investigators manually connect information across these sources, making the process slow, error-prone, and prone to overlooking crucial evidence or contradictions.

ForensIQ automates this process by extracting structured information and linking related evidence into a unified investigation timeline—all **offline**.

---

## 💡 Solution

ForensIQ processes multiple input formats:

- 📄 PDF Documents
- 🖼️ Images
- 🎙️ Audio Recordings

The system extracts and structures information such as:

- People
- Locations
- Events
- Dates & Time
- Evidence
- Vehicles
- Weapons
- Financial Transactions

It then automatically:

- Builds a chronological investigation timeline
- Links related entities across documents
- Detects conflicting statements
- Highlights missing or incomplete evidence
- Stores everything locally for fast retrieval

---

## 🏗️ System Workflow

```
             PDF / Image / Audio
                     │
                     ▼
          Text Extraction Layer
      (OCR / Whisper / PDF Parser)
                     │
                     ▼
          Text Normalization
                     │
                     ▼
      Local Small Language Model
                     │
                     ▼
     Structured Investigation JSON
                     │
                     ▼
          Relationship Linking
                     │
                     ▼
      Timeline & Intelligence Engine
                     │
                     ▼
             SQLite Database
                     │
                     ▼
            Investigation Dashboard
```

---

## ✨ Features

- Offline-first architecture
- CPU-only inference
- Local OCR
- Local Speech-to-Text
- Structured JSON extraction
- Entity extraction
- Relationship mapping
- Investigation timeline generation
- Contradiction detection
- Local SQLite database
- Fast evidence search
- Privacy-first (No cloud APIs)

---

## 🧠 AI Pipeline

### Input

- Investigation PDFs
- Evidence Images
- Officer Voice Notes

↓

### Extraction

- OCR
- Speech-to-Text
- PDF Parsing

↓

### AI Processing

Local Small Language Model extracts:

- People
- Events
- Locations
- Dates
- Evidence
- Relationships

↓

### Intelligence Generation

- Timeline
- Linked Evidence
- Contradictions
- Missing Evidence

↓

### Storage

SQLite Database

---

## 📦 Structured Output Example

```json
{
  "case_id": "CASE-1042",
  "people": [
    "Rahul Sharma",
    "Inspector Ravi"
  ],
  "location": "Hyderabad",
  "event": "Money Transfer",
  "date": "2026-06-24",
  "evidence_type": "Bank Statement",
  "related_documents": [
    "FIR.pdf",
    "Witness_1.pdf"
  ],
  "confidence": 0.94
}
```

---

## 🛠️ Tech Stack

### Frontend

- React
- Tailwind CSS

### Backend

- FastAPI
- Python

### AI

- OCR (Tesseract / PaddleOCR)
- Whisper.cpp
- Ollama / llama.cpp
- Small Local Language Model

### Database

- SQLite

---

## 💻 Offline CLI Tool Installation & Usage

ForensIQ includes a fully compiled, offline-first forensic intelligence CLI tool. Judges and reviewers can download and run it directly without installing Python, dependencies, or cloning the repository.

### Option 1: Standalone Binary (Recommended for Reviewers)
1. Go to the **Releases** tab of the GitLab repository.
2. Download the **`cli_investigator.exe`** binary from the Release Assets.
3. Open Command Prompt or PowerShell and navigate to the folder where you downloaded it.
4. Run the executable directly:
   ```cmd
   cli_investigator.exe
   ```

*Note: Ensure **Ollama** is running on your machine (configured with local models like `qwen2.5:3b` or `llama3.2`).*

---

### Option 2: Running from Source
If you wish to run the CLI directly from source:
1. Clone the repository and navigate to the project directory.
2. Activate the virtual environment:
   - **CMD:** `venv\Scripts\activate`
   - **PowerShell:** `.\venv\Scripts\Activate.ps1`
3. Install required libraries:
   ```bash
   pip install requests pymupdf
   ```
4. Run the CLI investigator script:
   ```bash
   python cli_investigator.py
   ```

---

## 📂 Project Structure

```
ForensIQ/

├── frontend/
│
├── backend/
│
├── api/
│
├── processors/
│   ├── pdf.py
│   ├── image.py
│   └── audio.py
│
├── ai/
│   ├── prompts.py
│   ├── inference.py
│   └── entity_linking.py
│
├── database/
│
├── uploads/
│
├── models/
│
└── docs/
```

---

## 🎯 Hackathon Requirements

- ✅ Offline-first
- ✅ CPU-first
- ✅ No external AI APIs
- ✅ Local AI inference
- ✅ Structured data extraction
- ✅ SQLite storage
- ✅ Open Source

---

## 🚀 Future Scope

- Face matching from evidence images
- Multi-case suspect linking
- Geospatial crime mapping
- Knowledge graph visualization
- Digital evidence similarity search
- AI-generated investigation summaries
- Offline semantic search across cases

---

## 📄 License

This project is released under the **GNU AGPL v3 License**.