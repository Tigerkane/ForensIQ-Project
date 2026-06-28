# ForensIQ Technical Research Notes

## 1. Local AI Engines
- **llama.cpp**: Best for raw CPU inference performance. Supports GGUF quantization. Requires `llama-cpp-python` for FastAPI integration.
- **Ollama**: Provides a clean REST API running locally. Very easy to swap models (e.g., `ollama run qwen2.5`). Preferred for rapid prototyping.

## 2. Models
- **Qwen2.5 3B Instruct**: Highly capable at structured JSON output. Excellent context window.
- **Phi-3 Mini**: Very fast on CPU, good reasoning capabilities, but requires strict prompting for JSON.

## 3. Modality Processors
- **PDF Extraction**: `PyMuPDF` (fitz) is faster and more robust than `PyPDF2`.
- **OCR**: `pytesseract` binding for Tesseract OCR. Requires local installation of the Tesseract binary.
- **Audio**: `whisper.cpp` (via `pywhispercpp` or executing the binary via subprocess).

## 4. Structured Output Enforcement
To guarantee the LLM outputs valid JSON for the `Relationships` and `Events` tables, we will use `Pydantic` models in FastAPI combined with `instructor` or raw GBNF grammar files in `llama.cpp`.
