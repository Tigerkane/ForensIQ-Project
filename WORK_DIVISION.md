# Work Division Plan

Since we are operating as a lean, agile team, roles will be distributed as follows:

## 1. AI & Backend Engineer
**Responsibilities:**
- Download and configure the quantized `.gguf` models.
- Set up the Python virtual environment and install dependencies.
- Build the FastAPI backend and SQLite database schema.
- Write the prompts and grammar constraints for extracting investigation entities via `llama.cpp`.

## 2. Frontend Engineer
**Responsibilities:**
- Design the Intelligence Dashboard using pure HTML and custom CSS.
- Implement a dark-mode "detective board" aesthetic.
- Write vanilla JavaScript to query the backend and render the chronological investigation timeline.

## 3. DevOps & QA
**Responsibilities:**
- Enforce the "Offline-First" rule by testing the entire pipeline in Airplane Mode.
- Configure local CI (`pre-commit` hooks).
- Ensure all 10 local checks (linting, formatting, security scanning) pass cleanly for Phase 3.
- Maintain documentation (README, CONTRIBUTING, CHANGELOG).
