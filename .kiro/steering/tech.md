---
inclusion: auto
---

# Tech Stack

## Runtime & Language

- **Python 3.14** (free-threaded, no GIL)
- Type hints encouraged on all public functions
- Docstrings in pt-BR using Google style

## Framework & Libraries

- **FastAPI** — web framework (async endpoints)
- **Pydantic** — request/response validation via schemas
- **Uvicorn** — ASGI server
- **zoneinfo + tzdata** — IANA timezone handling (stdlib)

## Package Management

- **uv** — package manager and virtual environment tool
- Install deps: `uv pip install -e ".[dev]"`
- Run commands: `uv run <command>`
- Do NOT use pip or venv directly

## Testing

- **pytest** — test runner
- **hypothesis** — property-based testing
- **httpx** — async HTTP test client (for FastAPI TestClient)
- **pytest-cov** — coverage reporting
- Run tests: `uv run pytest`
- Run with coverage: `uv run pytest --cov=app`

## Containerization

- **Docker** with `python:3.14-alpine` base image
- Uses multi-stage copy of `uv` from `ghcr.io/astral-sh/uv:latest`
- Exposes port 8000

## Code Style

- Follow existing patterns in the codebase
- Separate concerns: routers → schemas → services
- Custom exceptions inherit from `Exception` and include a `message` attribute
- Use `JSONResponse` for error responses with `{"detail": "..."}` format
