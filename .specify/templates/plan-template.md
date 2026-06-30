# ForensIQ Execution Plan

## Phase 2: MVP Development
1. **Backend Infrastructure**: Initialize FastAPI project. Setup SQLAlchemy models matching `data-model.md`.
2. **Document Processors**: Implement PyMuPDF for PDFs, Tesseract for Images, and Whisper.cpp for Audio.
3. **AI Pipeline**: Implement integration with Ollama/llama.cpp. Create prompts for structured JSON entity extraction.
4. **Frontend Dashboard**: Initialize React/Vite/Tailwind project. Build UI for uploading files and viewing the timeline and entity graphs.

## Phase 3: Polish & Deployment
1. **Offline Verification**: Disable all network adapters and run end-to-end tests.
2. **CI/CD**: Setup `.gitlab-ci.yml` for linting and security checks.
3. **Demo Preparation**: Prepare mock FIRs, witness statements, and audio files for the hackathon presentation.
