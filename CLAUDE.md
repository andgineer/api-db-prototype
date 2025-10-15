# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is an experimental API server implementation comparing two different approaches:
1. **Connexion - Spec First**: Auto-generates Python code from OpenAPI specification
2. **Flask - Code First**: Manual routing and handler implementation

Both approaches share common controllers and use SQLAlchemy for database access, Alembic for DB versioning, and JWT authentication.

## Development Environment Setup
```bash
source ./activate.sh  # Build and/or activate virtual environment
```

**IMPORTANT**: Always activate the virtual environment before running any commands. For commands that need to run in the same shell session (like tests), use:
```bash
source ./activate.sh && <your-command>
```

## Common Development Commands

### Running the Application
- `make run` - Run development server with auto-reload
- `make dev` - Run backend on local Python (Linux)
- `make prod` - Run production server

### Testing
- `make test` - Run all tests with coverage
  - Filter by test name: `source ./activate.sh && scripts/test.sh -k <test_name>`
  - Filter by marks: `source ./activate.sh && scripts/test.sh -m "mark1 and mark2"`
  - Run specific test: `source ./activate.sh && python -m pytest tests/test_file.py::test_name -v`
- `make smoke-test` - Quick curl test (JWT + user list)

### Database Operations
- `make db-create` - Create objects in empty DB (initial setup)
- `make db-upgrade` - Run migrations from alembic/versions/
- `make db-migration` - Create migration script in alembic/versions/
- `make db-show-migration` - Show migration script as SQL

### Code Generation & Build
- `make codegen` - Generate Python code from OpenAPI spec (updates src/openapi_server/)
- `make reqs` - Upgrade requirements including pre-commit hooks

### Security & Keys
- `make create-keys` - Recreate JWT keys in secret/ folder

## Code Quality & Linting
The project uses pre-commit hooks with:
- **Ruff**: Primary linter and formatter (line length: 100 chars)
- **MyPy**: Type checking (excludes tests)
- Comprehensive rule set covering security, complexity, imports, naming conventions

Run linting:
```bash
source ./activate.sh && pre-commit run --all-files  # Run all linting and formatting checks
```

**IMPORTANT**: Always use `pre-commit run --all-files` for code quality checks. Never run ruff or mypy directly.

## Architecture Overview

### Dual Server Implementation
The project maintains two parallel server implementations:
- **Flask Server** (`src/flask_server/api_app.py`): Manual route definitions
- **Connexion Server** (`src/openapi_server/api_app.py`): Auto-generated from OpenAPI spec

### Shared Components
- **Controllers** (`src/controllers/`): Transport-agnostic application logic
  - Decorated with `@transaction`, `@api_result`, `@token_to_auth_user`
  - User CRUD operations in `src/controllers/users/`
- **Database Layer** (`src/db/`): SQLAlchemy models with custom ORMClass base
- **Authentication**: JWT-based with decorators for token validation

### Configuration System
Environment-based configuration in `src/settings.py`:
- `ConfigTest`: Temporary SQLite for testing
- `ConfigDev`: Local SQLite for development
- `ConfigProd`: Production config with environment variables

### Key Files
- `src/app.py`: Main application entry point with environment detection
- `src/jwt_token.py`: JWT token handling
- `src/journaling.py`: Centralized logging configuration
- `api/swagger.yaml`: OpenAPI specification
- `src/alembic/`: Database migration management

## API Development Workflow

### Adding New Endpoints

#### Flask Approach:
1. Implement controller in `src/controllers/`
2. Add route proxy in `src/flask_server/api_app.py`

#### Connexion Approach:
1. Implement controller in `src/controllers/`
2. Update API spec in `api/swagger.yaml`
3. Run `make codegen` to regenerate server code
4. Implement proxies in `src/openapi_server/controllers/`

### Authentication
All protected endpoints expect `Authorization: Bearer <token>` header. Get token via POST to `/auth` with email/password.

## Testing Strategy
- Tests in `tests/` directory using pytest
- Separate test configurations for Flask and Connexion
- Coverage reporting with exclusion of auto-generated code
- Integration tests cover both server implementations
