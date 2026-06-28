# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `.gitlab-ci.yml` pipeline configuration.
- `CONTRIBUTING.md` rules and guidelines.

## [1.0.0] - 2026-06-28 - Hackathon MVP Release

### Added
- **FastAPI Backend**: Fully modular architecture (`api/`, `processors/`, `services/`, `database/`).
- **SQLite Schema**: Relational database for Cases, Events, People, Documents, etc.
- **Offline Modality Processors**: 
  - `PyMuPDF` for local PDF extraction.
  - `Tesseract OCR` integration for images.
  - `Whisper.cpp` (mocked) for audio transcripts.
- **AI Integration**: Connected to local Ollama (`qwen2.5:3b`) enforcing strict JSON output for entity extraction.
- **React Frontend**: Beautiful Dark-mode glassmorphic Dashboard built with Vite and TailwindCSS v4.
- **Test Evidence**: Included `mock_witness_statement.txt` for rapid offline demoing.
