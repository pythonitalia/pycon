"""Run the dedicated DBOS worker process.

This launches DBOS and blocks, executing durable workflows. It plays the same
role for DBOS that the Celery worker plays for Celery, and runs alongside it.
The web tier never launches DBOS — it only enqueues via ``get_dbos_client()``.

See SPEC.md / tasks/plan.md (Phase B).
"""

import signal
import threading

from django.core.management.base import BaseCommand, CommandError

from dbos import DBOS

# Importing the workflow module registers its @DBOS.workflow / @DBOS.step
# functions before launch so the worker can execute them.
from pycon import dbos_workflows  # noqa: F401
from pycon.dbos_app import DBOS_QUEUE_NAME, build_dbos_config


class Command(BaseCommand):
    help = "Launch the DBOS worker (executes durable workflows). Runs alongside Celery."

    def handle(self, *args, **options):
        config = build_dbos_config()
        if not config.get("system_database_url"):
            raise CommandError(
                "DBOS_SYSTEM_DATABASE_URL is not set; cannot launch the DBOS worker."
            )

        DBOS(config=config)
        DBOS.launch()
        # Register the shared queue (after launch) so this worker dequeues the
        # workflows the web tier enqueues onto it.
        DBOS.register_queue(DBOS_QUEUE_NAME)
        self.stdout.write(
            self.style.SUCCESS(
                f"DBOS launched (app={config['name']}, queue={DBOS_QUEUE_NAME}). "
                "Waiting for work — Ctrl-C to stop."
            )
        )

        stop = threading.Event()

        def _shutdown(signum, frame):
            self.stdout.write("Received shutdown signal, stopping DBOS...")
            stop.set()

        signal.signal(signal.SIGTERM, _shutdown)
        signal.signal(signal.SIGINT, _shutdown)

        try:
            stop.wait()
        finally:
            DBOS.destroy(workflow_completion_timeout_sec=30)
            self.stdout.write("DBOS stopped.")
