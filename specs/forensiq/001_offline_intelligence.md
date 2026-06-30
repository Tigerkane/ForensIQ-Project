# Feature Spec: Offline Intelligence Extraction

## Background
The application must extract structured JSON data from investigative text without utilizing external cloud APIs.

## Requirements
1. Must use local Ollama instance.
2. Must run inference via Llama 3.2 or Qwen 2.5.
3. Must fail gracefully if the model is not found.
