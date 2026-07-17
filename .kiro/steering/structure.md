---
inclusion: auto
---

# Project Structure

```
exemplo_cli/
├── app/                    # Application source code
│   ├── __init__.py
│   ├── main.py             # FastAPI app instance, global exception handlers
│   ├── routers/            # API route definitions (one file per domain)
│   │   ├── __init__.py
│   │   └── time.py         # GET /time endpoint
│   ├── schemas/            # Pydantic models for request/response validation
│   │   ├── __init__.py
│   │   └── time.py         # TimeResponse, ErrorResponse
│   └── services/           # Business logic (no HTTP/framework dependencies)
│       ├── __init__.py
│       └── time.py         # validate_timezone(), get_current_time()
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_final_validation.py
├── .kiro/
│   ├── specs/              # Spec-driven development documents
│   ├── steering/           # Steering files (this file, tech, product, etc.)
│   └── agents/             # Custom agent definitions
├── pyproject.toml          # Project metadata and dependencies
├── Dockerfile              # Container build definition
├── uv.lock                 # Locked dependency versions
└── .venv/                  # Local virtual environment (not committed)
```

## Architecture Conventions

- **Routers** handle HTTP concerns (path params, query params, status codes). They call services and return schema objects.
- **Schemas** define the shape of data going in and out. They are pure Pydantic models with no logic.
- **Services** contain business logic. They raise domain exceptions (not HTTP exceptions) and return plain dicts or domain objects.
- **Exception handlers** are registered in `main.py` and translate domain exceptions to HTTP responses.

## Adding a New Endpoint

1. Create or update the schema in `app/schemas/`
2. Implement business logic in `app/services/`
3. Add the route in `app/routers/`
4. Register the router in `app/main.py` (if new file)
5. Add tests in `tests/`

## File Naming

- One domain per file (e.g., `time.py` for time-related code in each layer)
- Test files prefixed with `test_` (pytest convention)
- Steering files use kebab-case (e.g., `windows-cmd.md`)
