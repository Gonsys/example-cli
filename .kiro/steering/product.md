---
inclusion: auto
---

# Product Context

## What is this project?

Time Service is a REST API that returns the current time for any IANA timezone. It serves as a lightweight, reliable utility service for applications that need timezone-aware datetime information.

## Core Functionality

- Single endpoint: `GET /time?timezone=<IANA_ID>`
- Returns current datetime in ISO 8601 format, the timezone used, and the UTC offset
- Defaults to `America/Sao_Paulo` when no timezone is provided
- Validates timezone input against IANA database and returns descriptive error messages

## Target Users

- Backend services that need accurate, timezone-aware timestamps
- Frontend applications displaying localized time
- DevOps tooling and monitoring dashboards

## Language

- Code comments, docstrings, and API descriptions are written in **Brazilian Portuguese (pt-BR)**
- Variable names, function names, and technical identifiers use English
- When writing new code or documentation, follow this same convention

## Quality Standards

- Responses must be fast (sub-100ms for valid requests)
- Error messages must be clear and actionable
- The service must be stateless and horizontally scalable
