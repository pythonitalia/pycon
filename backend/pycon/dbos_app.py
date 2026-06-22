"""Central DBOS configuration for the backend.

Single source of truth for ``DBOSConfig``. The dedicated ``dbos_worker``
management command launches DBOS with :func:`build_dbos_config`; the web tier
uses :func:`get_dbos_client` to *enqueue* workflows without ever launching DBOS.

DBOS runs alongside Celery (purely additive) and stores its workflow state in a
separate ``dbos`` database on the existing Postgres server. See SPEC.md.
"""

from __future__ import annotations

from dbos import DBOSClient, DBOSConfig
from django.conf import settings

# Name of the database-backed queue the worker dequeues from and the web tier
# enqueues onto. Centralised so producer and consumer cannot drift.
DBOS_QUEUE_NAME = "dbos_default"


def build_dbos_config() -> DBOSConfig:
    """Build the DBOSConfig from Django settings.

    Used by the worker process to configure and launch DBOS. ``run_admin_server``
    is disabled for now to avoid binding an extra port (see SPEC.md open items).
    """
    config: DBOSConfig = {
        "name": settings.DBOS_APP_NAME,
        "system_database_url": settings.DBOS_SYSTEM_DATABASE_URL,
        "sys_db_pool_size": settings.DBOS_SYS_DB_POOL_SIZE,
        "run_admin_server": False,
    }
    return config


_client: DBOSClient | None = None


def get_dbos_client() -> DBOSClient:
    """Return a lazily-created, process-wide ``DBOSClient`` for the web tier.

    The client enqueues workflows by name against the DBOS system database. It
    never calls ``DBOS.launch()`` (only the dedicated worker process does). The
    singleton is reused across calls and torn down at process exit.
    """
    global _client
    if _client is None:
        _client = DBOSClient(
            system_database_url=settings.DBOS_SYSTEM_DATABASE_URL,
        )
    return _client
