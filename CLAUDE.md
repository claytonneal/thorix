# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Project Overview

Python SDK for VeChain Thor blockchain integrating with the Thorest REST API.
Primary users are blockchain developers.
Minimal dependencies, security focus.

## Tech Stack
- python
- pydantic
- httpx
- pytest
- poetry

Do not introduce additional dependencies unless explicitly requested

## Architecture

The SDK has three layers with strict unidirectional flow:

```
HTTP JSON  →  schemas/  →  mappers.py  →  types/
```

- `http/` — httpx sync/async wrappers with retry logic
- `schemas/` — Pydantic models for raw Thorest JSON; all inherit `ThorestModel`
- `schemas/primitives.py` — Pydantic `Annotated` type aliases used only inside Pydantic models
- `thorest/` — endpoint classes (e.g. `AccountsAPI` / `AsyncAccountsAPI`): transport → schema validation → mapper → domain type
- `client/` — `ThorClient` / `AsyncThorClient` compose transport and all `thorest/` APIs into one entry point
- `config/` — dataclass for SDK configuration
- `types/` — user-facing dataclasses and types
- `types/primitives.py` — `Address`, `BlockId`, `BlockRef`, `BlockLabel` (StrEnum) as `str` subclasses with validation in `__new__`; used in domain types and public APIs

Rules:
- Do not mix pydantic schema types (`schemas/primitives.py`) with domain types (`types/primitives.py`)

## Coding Conventions
- Use concise, confident language
- All classes, methods, functions to have doc comments
- All Python code to be Python 3.11+ compatible
- Keep sync and async clients and APIs separated
- Do not leave dead code or commented-out blocks
- Extract repeated logic into helpers
- All type aliases in `schemas/primitives.py` must be annotated with `TypeAlias` so pyright recognises them as valid type expressions (not bare function calls)


## Commands

```bash
# Install dependencies (requires Poetry 2.x)
poetry install --with dev

# Run all tests with coverage (term + HTML + XML)
make test

# Run unit tests only (no Docker required)
make test-unit

# Run a single test file
poetry run pytest tests/unit/schemas/test_account_schema.py

# Run a single test by name
poetry run pytest tests/unit/schemas/test_account_schema.py::TestAccountSchemaValid::test_valid_payload

# Run integration tests against Thor solo node (requires Docker)
make solo-up && make test-solo && make solo-down
```

## Testing & Quality

Testing conventions:
- Mock transports with plain `MagicMock()` — no `spec=` — so `assert_called_once_with` is available. Use `AsyncMock` for async transport methods
- For schema tests always use `Model.model_validate(dict)`, not the constructor
- `ThorestModel` sets `serialize_by_alias=True`, so use `model_dump(by_alias=False)` to access snake_case field names in assertions

Before completing a task, run relevant tests for modified logic.
