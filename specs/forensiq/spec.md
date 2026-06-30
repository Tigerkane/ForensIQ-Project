# ForensIQ – Complete Project Specification

**ForensIQ**
*Transforming scattered evidence into connected investigation intelligence — completely offline.*

## 1. Project Overview
ForensIQ is an **Offline-First, CPU-Optimized Investigation Intelligence Platform** that converts unstructured criminal investigation data (PDFs, Images, Audio) into structured investigation records using only locally running AI models.

## 2. Hackathon Alignment
- **Offline First**: Runs completely locally. No cloud inference.
- **CPU First**: AI models run on CPU (quantized GGUF via llama.cpp/Ollama, Tesseract OCR, Whisper.cpp).
- **Structured Data Extraction**: Converts unstructured text into structured JSON persisted in SQLite.

## 3. Pipeline
PDF/Image/Audio $\rightarrow$ Text Extraction $\rightarrow$ Normalization $\rightarrow$ Local LLM $\rightarrow$ Structured JSON $\rightarrow$ Entity Linking $\rightarrow$ Timeline Generation $\rightarrow$ SQLite Storage $\rightarrow$ Frontend Dashboard.

## 4. Tech Stack
- **Frontend**: React, Vite, TailwindCSS
- **Backend**: Python, FastAPI
- **AI Engine**: Ollama or llama.cpp (Qwen2.5 3B / Phi-3 Mini)
- **OCR/Speech**: Tesseract OCR, Whisper.cpp
- **Database**: SQLite

## 5. Folder Structure
```
ForensIQ/
├── frontend/
├── backend/
│   ├── api/
│   ├── processors/
│   ├── services/
│   ├── database/
│   └── uploads/
└── docs/
```
