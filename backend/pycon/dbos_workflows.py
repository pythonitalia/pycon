"""DBOS proof-of-concept workflow.

A minimal ``healthcheck`` workflow used to prove that DBOS launches and executes
a durable, idempotent workflow end to end. It is intentionally *not* wired into
any request path, signal, or Celery task — this is the single proof the
foundation slice owes (see SPEC.md). Real task migration is out of scope here.
"""

from __future__ import annotations

from dbos import DBOS

# Explicit, stable workflow name so external enqueuers (DBOSClient) reference it
# by string without depending on the function's location.
HEALTHCHECK_WORKFLOW_NAME = "healthcheck"


def _perform_check() -> str:
    """The unit of work the healthcheck performs.

    Pulled out as a plain function so tests can observe how many times it runs:
    re-invoking the workflow under the same workflow ID must execute this once,
    proving DBOS's exactly-once / idempotent behaviour.
    """
    return "ok"


@DBOS.step()
def healthcheck_step() -> str:
    """Single checkpointed step. Its result is recorded for recovery."""
    return _perform_check()


@DBOS.workflow(name=HEALTHCHECK_WORKFLOW_NAME)
def healthcheck() -> str:
    """Run one step and return its result."""
    result = healthcheck_step()
    DBOS.logger.info(f"healthcheck workflow {DBOS.workflow_id} -> {result}")
    return result
