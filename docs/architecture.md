# Architecture Overview

This project is intentionally minimal to support a clean Python development setup and a test-first workflow.

## Components
- `app/` contains the application code
- `tests/` contains automated tests
- `docs/` stores specification and architecture notes

## Design direction
The project follows a simple layered structure:
- application entry point in `app/main.py`
- configuration values in `app/config.py`
- future domain logic can be added under `app/domain/`
- future service logic can live under `app/services/`
