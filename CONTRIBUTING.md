# Contributing to ForensIQ

First off, thank you for considering contributing to ForensIQ! 

We welcome contributions from everyone. By participating in this project, you agree to abide by our Code of Conduct and to ensure the core philosophy of **Offline-First, CPU-Optimized Inference** is never compromised.

## How Can I Contribute?

### 1. Reporting Bugs
If you find a bug, please create a GitLab Issue with the following:
* Your Operating System and CPU architecture.
* The exact error log from either the FastAPI backend or Vite frontend.
* The local AI model you were attempting to run (e.g., Ollama qwen2.5:3b).

### 2. Suggesting Enhancements
We are always looking to improve our Entity Extraction and Timeline generation logic. If you have an idea, create an Issue titled `[ENHANCEMENT] - Your Idea`. 

### 3. Submitting Pull / Merge Requests
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and test them completely **Offline** (Disable your Wi-Fi).
4. Ensure all code passes local linting.
5. Push to your fork and submit a Merge Request.

## Core Rules for Code Changes
* **NO CLOUD APIs**: Do not import or utilize OpenAI, AWS, Anthropic, or any other cloud-based processing API.
* **CPU First**: Any AI additions (like Facial Recognition or Graph generation) must be capable of running via CPU bindings.
