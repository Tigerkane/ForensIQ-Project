# ForensIQ Agent Operations

This document defines the rules, roles, and boundaries for AI agents operating within the ForensIQ repository.

## Roles
- **Coding Agents:** Responsible for writing React and FastAPI code. Must adhere to `.editorconfig` and Ruff formatting.
- **Review Agents:** Responsible for analyzing code against Bandit security rules.

## Boundaries
- AI Agents must never commit secrets to the repository.
- AI Agents must respect the Git-Cliff changelog format.
