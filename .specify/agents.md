# AGENTS.md

# ForensIQ – AI Development Guidelines

## Project Goal

Build an **offline-first, CPU-only AI investigation platform** that converts unstructured **PDFs, images, and audio** into structured investigation data. No cloud APIs or internet access should be required.

---

## Tech Stack

* **Frontend:** React + Vite + TailwindCSS
* **Backend:** FastAPI + Python
* **Database:** SQLite
* **OCR:** Tesseract OCR
* **Speech-to-Text:** Whisper.cpp
* **LLM:** Qwen2.5 3B GGUF (via Ollama or llama.cpp)
* **Validation:** Pydantic

---

## AI Pipeline

```
PDF / Image / Audio
        ↓
 Text Extraction
        ↓
 Text Normalization
        ↓
 Local LLM
        ↓
 Structured JSON
        ↓
 SQLite
        ↓
 Timeline & Dashboard
```

---

## Project Structure

```
frontend/
backend/
api/
processors/
services/
database/
schemas/
uploads/
docs/
```

---

## Development Rules

* Offline-first and CPU-only.
* Never use cloud AI APIs (OpenAI, Gemini, Anthropic, etc.).
* Keep code modular and reusable.
* Business logic belongs in `services/`, not API routes.
* Validate all AI-generated JSON before storing.
* Handle failures gracefully.
* Use semantic commits (`feat:`, `fix:`, `docs:`, etc.).

---

## MVP Features

* Upload PDF, Image, and Audio
* OCR / Speech-to-Text
* Local LLM extraction
* Structured JSON output
* SQLite storage
* Investigation timeline
* Searchable dashboard

---

## Goal

ForensIQ is **not a chatbot**. It is an **offline investigation intelligence platform** that transforms scattered evidence into structured, searchable investigation knowledge.
