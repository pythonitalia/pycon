# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Backend (Django)

- **Local development**: `docker-compose up` (starts all services)
- **Run tests**: `cd backend && uv run pytest` or `DJANGO_SETTINGS_MODULE=pycon.settings.test uv run pytest`
- **Single test**: `cd backend && uv run pytest path/to/test_file.py::test_function`
- **Lint/format**: `cd backend && uv run ruff check` and `uv run ruff format`
- **Type checking**: `cd backend && uv run mypy .`
- **Django management**: `cd backend && uv run python manage.py <command>`
- **Migrations**: `cd backend && uv run python manage.py makemigrations` and `uv run python manage.py migrate`

### Frontend (Next.js)

- **Local development**: `cd frontend && pnpm dev` (or via docker-compose)
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

- Python version: 3.13.5+ (specified in pyproject.toml)
- Uses `uv` for Python package management
- Uses `pnpm` for Node.js package management
- GraphQL schema auto-generation from Django backend to frontend
- Test configuration uses separate settings (`pycon.settings.test`)
- Ruff handles both linting and formatting for Python code
- Biome handles linting and formatting for JavaScript/TypeScript
