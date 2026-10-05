# AGENTS.md

This file provides guidance to coding agents when working with code in this repository.

## Development Commands

### Backend (Django)

- **Local development**: `docker compose up` (starts all services)
- **Run tests**: `cd backend && uv run pytest` or `DJANGO_SETTINGS_MODULE=pycon.settings.test uv run pytest`
- **Single test**: `cd backend && uv run pytest path/to/test_file.py::test_function`
- **Lint/format**: `cd backend && uv run ruff check` and `uv run ruff format`
- **Type checking**: `cd backend && uv run mypy .`
- **Django management**: `cd backend && uv run python manage.py <command>`
- **Migrations**: `cd backend && uv run python manage.py makemigrations` and `uv run python manage.py migrate`

### Frontend (Next.js)

- **Local development**: `cd frontend && pnpm dev` (or via docker compose)
- **Build**: `cd frontend && pnpm build`
- **Tests**: `cd frontend && pnpm test`
- **GraphQL codegen**: `cd frontend && pnpm codegen` (or `pnpm codegen:watch`)
- **Lint/format**: Use Biome via `npx @biomejs/biome check` and `npx @biomejs/biome format`

## Architecture Overview

This is a monorepo for PyCon Italia's website with:

### Backend Structure (Django)

- **API Layer**: GraphQL API using Strawberry at `/backend/api/`
- **Django Apps**: Modular apps in `/backend/` including:
  - `conferences/` - Conference management and configuration
  - `submissions/` - Talk/proposal submissions
  - `users/` - User management and authentication
  - `schedule/` - Event scheduling and video uploads
  - `sponsors/` - Sponsor management
  - `grants/` - Financial assistance program
  - `blog/` - Blog posts and news
  - `cms/` - Content management via Wagtail
  - `api/` - GraphQL schema and resolvers
- **Database**: PostgreSQL with migrations in each app's `migrations/` folder
- **Task Queue**: Celery with Redis backend for async processing
- **Storage**: Configurable (filesystem local, cloud for production)

### Frontend Structure (Next.js)

- **Framework**: Next.js
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Apollo Client for GraphQL
- **Type Safety**: Full TypeScript with generated types from GraphQL schema
- **Location**: `/frontend/src/` contains pages, components, and utilities

### Key Integrations

- **Pretix**: Ticketing system integration for event registration
- **Stripe**: Payment processing
- **ClamAV**: File scanning for security
- **Wagtail**: CMS for page content management
- **Google APIs**: For YouTube video management and calendar integration

## Development Environment

The project uses Docker Compose for local development with services:

- **backend**: Django API server (port 8000)
- **frontend**: Next.js dev server (port 3000)
- **custom-admin**: Admin interface (ports 3002-3003)
- **backend-db**: PostgreSQL database (port 15501)
- **redis**: Caching and task queue
- **clamav**: File virus scanning

## Important Notes

- Python version: 3.14.7+ (specified in pyproject.toml)
- Uses `uv` for Python package management
- Uses `pnpm` for Node.js package management
- GraphQL schema auto-generation from Django backend to frontend
- Test configuration uses separate settings (`pycon.settings.test`)
- Ruff handles both linting and formatting for Python code
- Biome handles linting and formatting for JavaScript/TypeScript

## GraphQL API Conventions

When working in `backend/api`:

- Name Strawberry GraphQL classes after their GraphQL schema types, without a
  `Type` suffix.
- Import Django model modules and access models through the module namespace,
  for example `from job_board import models` and `models.JobListing`.
- If a file needs models from multiple Django apps, alias the modules, for
  example `job_board_models` and `conference_models`.
- Do not alias individual Django models with a `Model` suffix or GraphQL types
  with a `Type` suffix solely to avoid naming conflicts.
- Use `strawberry.auto` instead of importing `auto` directly from Strawberry.
- Use `strawberry.ID` instead of importing `ID` directly from Strawberry.
- Preserve existing GraphQL schema names when migrating types to Strawberry
  Django.

## Local Development

**IMPORTANT**: When running locally, all Python/Django commands must run inside Docker. The local virtual environment will not work.

- **Start services**: `docker compose up` (starts all services)
- **Run tests**: `docker compose exec backend uv run pytest -l -s -vvv`
- **Single test**: `docker compose exec backend uv run pytest path/to/test_file.py::test_function -l -s -vvv`
- **Lint/format**: `docker compose exec backend uv run ruff check` and `docker compose exec backend uv run ruff format`
- **Type checking**: `docker compose exec backend uv run mypy .`
- **Django management**: `docker compose exec backend uv run python manage.py <command>`
- **Migrations**: `docker compose exec backend uv run python manage.py makemigrations` and `docker compose exec backend uv run python manage.py migrate`

**Troubleshooting**: If the backend container is not working:
1. Restart container: `docker compose restart backend`
2. If dependencies changed: Remove `backend/.venv` and rebuild with `docker compose build --no-cache && docker compose up`

## Comments

- A comment states a constraint the code cannot express and a reader would otherwise undo: an external quirk (OpenSearch, DRF, a library), a non-obvious invariant, a reason not to take the obvious shortcut. Nothing else.
- Never describe what the code did before, why it changed, or what it replaces. If the comment only makes sense to someone who saw the old code, delete it. It belongs in the commit message. Self-check before finishing: grep the diff for `used to|previously|before|no longer|already|now|instead of|pinned|this PR` in comment lines and delete or rewrite every hit.
- No ticket IDs, PR numbers, spec or plan file names in code or comments.
- One or two lines. A longer comment means the code or the name needs work.
- No section-divider comments (`# -- foo ---`), no narration (`# increment count`), no docstring that restates the function or class name.
- Docstrings only on public interfaces: API views, serializers used by the FE, functions exported for other apps. Private helpers get a name, not a docstring.

### Writing tests

- No comments and no docstrings in test files. The test name is the documentation. If a fixture needs explaining, rename the variable; if a class needs a docstring, split it or rename it.
- Test behaviour, never structure.
- One layer per behaviour. Handler logic is tested through the search class; the view is tested only for what the view adds (status codes, error bodies, scope routing). Do not re-assert search results through the view.
- A test earns its place only if a plausible bug would fail it and no other test. Before adding one, name that bug. Delete tests that are implied by another test (`x is not None` when another test dereferences `x`; "is accepted" when another test already gets results through the same path).
- Assert complements together. `exists: true` and `exists: false`, or any pair of opposite directions, share fixtures and live in one test.
- Use `pytest.mark.parametrize` for cases that differ only in inputs. Do not write near-identical test methods.
- Do not add guard tests for pre-existing behaviour the change cannot affect.
- Extend the existing test module for a feature. Do not create a parallel `*_edge_cases` module or "pin" a test file as unmodifiable.
