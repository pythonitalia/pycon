"""In-process tests for the DBOS foundation.

These run against a dedicated ``dbos_test`` Postgres database on the same server
as the app database (auto-created if missing, reset before each test). DBOS uses
its own SQLAlchemy engine and does not touch the Django ORM, so these tests do
not request the pytest-django ``db`` fixture and are unaffected by its
transactional rollback. See SPEC.md / tasks/plan.md (Phase A).

Note: a SQLite system DB is NOT usable here — DBOS 2.24.0's migrations are raw
Postgres DDL (``EXTRACT(epoch FROM now())`` defaults, ``gen_random_uuid()``,
``JSON[]``), so SQLite cannot honour them. Hence a real Postgres test DB.
"""

import os
from urllib.parse import urlsplit, urlunsplit

import psycopg
import pytest
from django.conf import settings
from django.test import override_settings

from dbos import DBOS, DBOSConfig, SetWorkflowID

from pycon import dbos_workflows
from pycon.dbos_app import build_dbos_config


def _dbos_test_system_database_url() -> str:
    """Build the DBOS test system DB URL from Django's DB connection params.

    Same server/credentials as the app database, but a dedicated ``dbos_test``
    database. Overridable via ``DBOS_TEST_SYSTEM_DATABASE_URL``.
    """
    override = os.environ.get("DBOS_TEST_SYSTEM_DATABASE_URL")
    if override:
        return override
    db = settings.DATABASES["default"]
    host = db.get("HOST") or "localhost"
    port = db.get("PORT") or 5432
    user = db.get("USER") or "postgres"
    password = db.get("PASSWORD") or ""
    return f"postgresql://{user}:{password}@{host}:{port}/dbos_test"


def _ensure_database(url: str) -> None:
    """Create the target database if it does not already exist."""
    parsed = urlsplit(url)
    target = parsed.path.lstrip("/")
    admin_url = urlunsplit((parsed.scheme, parsed.netloc, "/postgres", "", ""))
    with psycopg.connect(admin_url, autocommit=True) as conn:
        exists = conn.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (target,)
        ).fetchone()
        if not exists:
            conn.execute(f'CREATE DATABASE "{target}"')


@pytest.fixture()
def reset_dbos():
    """Give each test a clean DBOS instance on a reset ``dbos_test`` database."""
    url = _dbos_test_system_database_url()
    _ensure_database(url)
    DBOS.destroy(destroy_registry=False)
    config: DBOSConfig = {"name": "pycon-test", "system_database_url": url}
    DBOS(config=config)
    DBOS.reset_system_database()
    DBOS.launch()
    yield
    DBOS.destroy(destroy_registry=False)


def test_healthcheck_executes(reset_dbos):
    assert dbos_workflows.healthcheck() == "ok"


def test_healthcheck_idempotent(reset_dbos, mocker):
    spy = mocker.patch.object(dbos_workflows, "_perform_check", return_value="ok")

    workflow_id = "healthcheck-idempotency-test"
    with SetWorkflowID(workflow_id):
        first = dbos_workflows.healthcheck()
    with SetWorkflowID(workflow_id):
        second = dbos_workflows.healthcheck()

    assert first == second == "ok"
    # Same workflow ID => DBOS returns the recorded result without re-running.
    assert spy.call_count == 1


@override_settings(
    DBOS_APP_NAME="pycon",
    DBOS_SYSTEM_DATABASE_URL="postgresql://u:p@db:5432/dbos",
    DBOS_SYS_DB_POOL_SIZE=5,
)
def test_build_dbos_config():
    config = build_dbos_config()
    assert config["name"] == "pycon"
    assert config["system_database_url"].startswith("postgresql://")
    assert config["sys_db_pool_size"] == 5
    assert config["run_admin_server"] is False
