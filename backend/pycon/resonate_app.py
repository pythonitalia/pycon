"""Resonate (durable workflows) wiring for the backend.

Two roles share one module:

- **The worker** (``manage.py resonate_worker``) builds the singleton returned
  by :func:`get_resonate`, which every workflow module registers against, and
  starts it so the Resonate server can push work to it.
- **The web/admin tier** never starts that singleton. It triggers work with
  :func:`start_workflow`, which opens a short-lived, send-only client, creates
  the durable promise and returns its id.

Workflow modules live in ``<app>/workflows.py`` (or ``<app>/workflows/``) and
are imported by :func:`autodiscover_workflows`, mirroring how Celery tasks are
discovered.
"""

from __future__ import annotations

import asyncio
import functools
from typing import Any, Callable, TypeVar

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connections
from django.utils.module_loading import autodiscover_modules
from resonate.resonate import Resonate

_resonate: Resonate | None = None

T = TypeVar("T")


def _build(*, send_only: bool) -> Resonate:
    kwargs: dict[str, Any] = {
        "group": settings.RESONATE_GROUP,
        # Nothing here needs an event loop: connections are opened by
        # ``start()``, so building at import time is safe.
        "autostart": False,
        # The SDK falls back to reading RESONATE_URL (and friends) from the
        # environment; hiding it keeps Django settings the only source.
        "env": {},
    }

    if settings.RESONATE_URL:
        kwargs["url"] = settings.RESONATE_URL

    if send_only:
        # No source: this process only creates promises, it never picks work up.
        kwargs["sources"] = []

    return Resonate(**kwargs)


def get_resonate() -> Resonate:
    """The process-wide Resonate instance workflows register against."""
    global _resonate

    if _resonate is None:
        _resonate = _build(send_only=False)

    return _resonate


def require_server() -> None:
    """Refuse to run workflows without a Resonate server to run them on.

    Without a URL the SDK falls back to its in-process connection, where a
    workflow would be created and then never executed by anything.
    """
    if not settings.RESONATE_URL:
        raise ImproperlyConfigured(
            "RESONATE_URL is not set, so there is no Resonate server to run "
            "workflows on"
        )


def autodiscover_workflows() -> None:
    """Import every ``workflows`` module so its registrations happen."""
    autodiscover_modules("workflows")


def start_workflow(name: str, workflow_id: str, *args: Any, **kwargs: Any) -> str:
    """Create a durable promise for ``name`` and return its id.

    Fire-and-forget from synchronous Django code: the workflow itself runs on a
    worker subscribed to ``settings.RESONATE_GROUP``. ``workflow_id`` is the
    idempotency key -- creating the same id twice joins the existing run
    instead of starting a second one.
    """

    require_server()

    async def _dispatch() -> str:
        client = _build(send_only=True)
        client.start()

        try:
            handle = client.rpc(workflow_id, name, *args, **kwargs)
            return await handle.id()
        finally:
            await client.stop()

    return asyncio.run(_dispatch())


def database_step(fn: Callable[..., T]) -> Callable[..., Any]:
    """Adapt a synchronous, ORM-using step so it can run as a durable step.

    The SDK executes durable functions on an event loop, where Django's ORM
    refuses to run (``SynchronousOnlyOperation``). The body is therefore
    handed to asgiref's thread-sensitive executor -- a single thread, so every
    step reuses one database connection -- with stale connections recycled
    first, the way a request or a Celery task would.
    """

    @functools.wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        def run() -> T:
            _recycle_connections()
            return fn(*args, **kwargs)

        return await sync_to_async(run, thread_sensitive=True)()

    return wrapper


def _recycle_connections() -> None:
    """``close_old_connections``, minus any connection we do not own.

    A connection inside an atomic block belongs to whoever opened the
    transaction (in tests, the one wrapping each test), and closing it there
    breaks the caller.
    """
    for connection in connections.all(initialized_only=True):
        if not connection.in_atomic_block:
            connection.close_if_unusable_or_obsolete()
