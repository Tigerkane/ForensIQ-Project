# ForensIQ - Technical Specification Kit

## 1. System Architecture
- **Frontend Dashboard**: Vanilla HTML5, CSS3, and Vanilla JS.
- **Backend API**: Python (FastAPI).
- **Local AI Inference**: `llama.cpp` (via `llama-cpp-python`).
- **Data Persistence**: Local SQLite (Relational structure mapping entities to events).

## 2. AI Model Details
- **Base Model**: Highly quantized SLM (e.g., Llama-3-8B-Instruct.Q4_K_M or Phi-3).
- **Optimization Strategy**: CPU-only inference via `llama.cpp`.
- **JSON Grammar Enforcement**: Using GBNF grammars in `llama.cpp` to force the model to output strict JSON arrays of entities, ensuring zero parse errors.

## 3. Data Flow & Transformation
1. **Ingestion**: Unstructured text (e.g., a witness statement) is submitted to the local FastAPI backend.
2. **Structuring**: The text is passed to `llama.cpp` with a prompt instructing it to extract `Person`, `Location`, and `Timestamp` objects.
3. **Linking**: The backend parses the JSON and links new entities to existing entities in the SQLite database.
4. **Presentation**: The frontend queries the linked data to render a chronological intelligence timeline.

## 4. Future Modalities (Roadmap)
- **Audio Processing**: Implementing `whisper.cpp` for officer voice notes.
- **Image Processing**: Implementing `tesseract` for scanned FIRs.
