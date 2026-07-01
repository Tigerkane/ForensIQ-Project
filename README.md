# ForensIQ CLI
[![pipeline status](https://code.swecha.org/akhil08/forensiq/badges/main/pipeline.svg)](https://code.swecha.org/akhil08/forensiq/-/commits/main)

### Offline Investigation Intelligence CLI

> **A hundred eyes. One truth.**

ForensIQ is an **offline-first, CPU-optimized AI Command Line Interface (CLI)** that transforms unstructured criminal investigation data into structured, connected investigation intelligence. It enables investigators to process case files locally without relying on cloud services, ensuring absolute privacy, security, and usability in air-gapped environments.

---

## 🚨 Problem Statement

Modern investigations involve hundreds of scattered documents and evidence sources, including FIRs, witness statements, forensic reports, and crime scene notes. Investigators manually connect information across these sources, making the process slow, error-prone, and prone to overlooking crucial evidence.

ForensIQ CLI automates this process by extracting structured information and linking related evidence into a unified investigation report—all **offline**.

---

## 💡 Solution

ForensIQ CLI directly processes files and folders to extract and structure intelligence such as:

- People & Organizations
- Locations
- Events & Timelines
- Evidence & Financial Transactions

It automatically builds a chronological investigation timeline, links entities, detects contradictions, and outputs a highly structured JSON report.

---

## 💻 Installation & Usage

ForensIQ is provided as a fully compiled, offline-first executable. Judges, reviewers, and investigators can download and run it directly without installing Python, dependencies, or cloning the repository.

### Prerequisites
- **Ollama**: Must be installed and running locally with your chosen small language model (e.g., `llama3` or `qwen2.5:3b`).

### Standalone Binary (Recommended)
1. Go to the **Releases** tab of the GitLab repository.
2. Download the **`cli_investigator.exe`** binary.
3. Open Command Prompt or PowerShell in the download folder.
4. Run the executable, pointing it to your evidence file:
   ```cmd
   cli_investigator.exe --file "C:\Path\To\Evidence\Witness_Statement.pdf" --model "llama3"
   ```

### Running from Source
1. Clone the repository and navigate to the project directory.
2. Ensure you have Python installed and install `uv` (our package manager).
3. Install dependencies:
   ```cmd
   uv pip install -r backend/requirements.txt
   ```
4. Run the CLI tool:
   ```cmd
   python cli_investigator.py --file "C:\Path\To\Evidence\Witness_Statement.pdf"
   ```

---

## 🛠️ Tech Stack

### CLI Application
- **Python 3.12**
- **PyInstaller** (for standalone binary compilation)
- **Rich** (for beautiful terminal UI output)
- **Pydantic** (for strict data validation)

### AI & Intelligence
- **Ollama** (Local LLM engine)
- Local Speech-to-Text & OCR integrations

---

## 🎯 Core Features

- ✅ **100% Offline-first architecture**
- ✅ **CPU-optimized** inference
- ✅ **No external AI APIs or Cloud tracking**
- ✅ **Structured deep-investigation JSON extraction**
- ✅ **Contradiction & missing evidence detection**
- ✅ **Compiled Standalone Binary** for zero-setup execution

---

## 📄 License

This project is released under the **GNU AGPL v3 License**.