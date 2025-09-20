# Repository Guidelines

## Project Structure & Modules
- `src/`: application code (Flask app in `app.py`, SQLAlchemy models in `db/`, controllers in `controllers/`, configs in `settings.py`, Alembic in `alembic/`, OpenAPI-backed code in `openapi_server/`).
- `api/`: OpenAPI spec (`swagger.yaml`) and helpers.
- `tests/`: pytest suite.
- `scripts/`: developer and CI scripts (test, run, db, codegen).

## Build, Test, and Dev
- Init env: `. ./activate.sh` then `make reqs` (updates hooks, compiles requirements, installs dev deps).
- Run dev server: `make run` (uses `scripts/run_dev.sh`; sets `SERVER_ENV=development`).
- Run tests: `make test` or `scripts/test.sh -k name -m "mark"` (pytest with coverage; ignores Alembic).
- DB migrations: `make db-migration`, `make db-upgrade`, `make db-show-migration` (Alembic under `src/alembic`).
- Codegen from spec: `make codegen` (updates `src/openapi_server/`).
- Help: `make help` to list all targets.

## Coding Style & Naming
- Python 3.10+; 4-space indent; max line length 99.
- Naming: modules/files `snake_case.py`; functions/vars `snake_case`; classes `PascalCase`.
- Type hints required for new/changed code; keep public APIs typed.
- Linters: Ruff (`.ruff.toml`), Flake8 (`.flake8`), Pylint (`.pylintrc`), MyPy (`.mypy.ini`).
- Pre-commit: run `pre-commit install` (or `make reqs`) and commit only passing hooks.

## Testing Guidelines
- Framework: pytest with coverage (see `.coveragerc`).
- Location and names: `tests/test_*.py` with descriptive test names.
- Running: `make test`; filter with `-k` for name, `-m` for markers.
- Prefer black-box tests through Flask routes and controller-level tests; add factories/fixtures in `tests/conftest.py`.

## Commit & PR Guidelines
- Messages: concise, imperative mood (e.g., `fix: adjust JWT expiry`).
- Scope small, focused changes; include rationale in body when non-trivial.
- PRs: clear description, linked issues, steps to test, relevant screenshots/logs; note schema/API changes and migration steps.

## Security & Configuration
- Secrets live in `src/secret/` (dev only). Do not commit real keys.
- Configure via `src/settings.py`; set `SERVER_ENV` for environment selection.
- Database URL and Alembic config are derived from settings; run migrations before serving.
