# ForensIQ Task Tracker

- `[ ]` **1. Foundation**
  - `[ ]` Scaffold FastAPI backend (`backend/` directory)
  - `[ ]` Scaffold React frontend (`frontend/` directory)
  - `[ ]` Setup SQLite database and Pydantic schemas

- `[ ]` **2. Modality Processors**
  - `[ ]` Implement `processors/pdf.py` (PyMuPDF)
  - `[ ]` Implement `processors/image.py` (Tesseract)
  - `[ ]` Implement `processors/audio.py` (Whisper)

- `[ ]` **3. AI Integration**
  - `[ ]` Setup `services/llm.py` (Ollama/llama.cpp connector)
  - `[ ]` Write JSON extraction prompts for Entities & Events

- `[ ]` **4. Frontend Development**
  - `[ ]` Upload Page UI
  - `[ ]` Timeline Viewer component
  - `[ ]` Entity Search & Relationship graph

- `[ ]` **5. Polish**
  - `[ ]` E2E testing in Airplane Mode
