---
name: forensiq-extraction
description: Skill for extracting structured entities from investigation text.
---

# ForensIQ Entity Extraction Skill

## Instructions
When instructed to process an investigation document (FIR, statement), follow these steps:
1. Ensure the text has been normalized (newlines removed, OCR artifacts cleaned).
2. Construct a prompt instructing the LLM to extract: People, Locations, Events, Evidence, and Relationships.
3. Enforce a strict JSON grammar output.
4. If the JSON fails validation against the Pydantic schema, retry the inference with a higher temperature or updated prompt.
5. Store the validated entities in the SQLite database.
