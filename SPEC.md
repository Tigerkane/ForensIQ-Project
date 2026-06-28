# ForensIQ – Complete Project Specification

## Project Name
**ForensIQ**
*Transforming scattered evidence into connected investigation intelligence — completely offline.*

---

## 1. Project Overview
ForensIQ is an **Offline-First, CPU-Optimized Investigation Intelligence Platform** that converts unstructured criminal investigation data into structured, searchable investigation intelligence. The system processes PDF documents, images, and audio recordings, transforming them into structured investigation records using only locally running AI models. No internet connection or cloud APIs are required.

## 2. Real World Problem
Modern investigations involve hundreds of different files (FIRs, Witness Statements, Crime Scene Reports, Bank Statements, Officer Voice Notes). Investigators manually read, identify entities, connect relationships, and build timelines—a slow and error-prone process. ForensIQ automates this completely offline.

## 3. Hackathon Alignment
- **Offline First**: Runs completely locally. No OpenAI/Anthropic/Gemini.
- **CPU First**: AI models run on CPU (quantized GGUF via llama.cpp/Ollama, Tesseract OCR, Whisper.cpp).
- **Structured Data**: Converts unstructured text into structured JSON persisted in SQLite.

## 4. Supported Inputs
- **PDFs**: Extracted via PyMuPDF/pdfplumber.
- **Images**: Extracted via Tesseract OCR.
- **Audio**: Extracted via Whisper.cpp.

## 5. Database Design (SQLite)
- **Cases**: case_id, title, created_at, status
- **Events**: event_id, case_id, event, time, location, description
- **People**: person_id, case_id, name, role
- **Organizations**: organization_id, case_id, name
- **Vehicles**: vehicle_id, case_id, registration, model
- **Evidence**: evidence_id, case_id, type, source_document
- **Relationships**: relationship_id, entity1, relation, entity2
- **Documents**: document_id, case_id, filename, type, processed_at

## 6. Tech Stack
- **Frontend**: React, Vite, TailwindCSS
- **Backend**: Python, FastAPI, Pydantic
- **AI Engine**: Ollama / llama.cpp (Qwen2.5 3B / Phi-3 Mini)
- **OCR/Speech**: Tesseract OCR, Whisper.cpp
- **Database**: SQLite

## 7. Folder Structure
```
ForensIQ/
├── frontend/ (React UI)
├── backend/
│   ├── api/
│   ├── processors/ (pdf.py, image.py, audio.py)
│   ├── services/ (ocr.py, speech.py, llm.py, timeline.py)
│   ├── database/ (models, schemas)
│   └── uploads/
└── docs/
```
