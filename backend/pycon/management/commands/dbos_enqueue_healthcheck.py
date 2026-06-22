"""Enqueue the proof-of-concept ``healthcheck`` workflow via ``DBOSClient``.

Demonstrates how the web tier submits work to DBOS without launching it: build a
client against the system database and enqueue by workflow name. With the
``dbos_worker`` process running, the workflow is dequeued, executed, and its
result returned here — proving the full round-trip. See SPEC.md (Phase B).
"""

from django.core.management.base import BaseCommand, CommandError

from dbos import DBOSClient, EnqueueOptions

from pycon.dbos_app import DBOS_QUEUE_NAME
from pycon.dbos_workflows import HEALTHCHECK_WORKFLOW_NAME


class Command(BaseCommand):
    help = "Enqueue the healthcheck workflow via DBOSClient (proves the round-trip)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--workflow-id",
            help="Optional explicit workflow ID (re-using one is idempotent).",
        )

    def handle(self, *args, **options):
        from django.conf import settings

        if not settings.DBOS_SYSTEM_DATABASE_URL:
            raise CommandError("DBOS_SYSTEM_DATABASE_URL is not set.")

        client = DBOSClient(system_database_url=settings.DBOS_SYSTEM_DATABASE_URL)
        try:
            enqueue_options: EnqueueOptions = {
                "workflow_name": HEALTHCHECK_WORKFLOW_NAME,
                "queue_name": DBOS_QUEUE_NAME,
            }
            if options.get("workflow_id"):
                enqueue_options["workflow_id"] = options["workflow_id"]

            handle = client.enqueue(enqueue_options)
            self.stdout.write(f"Enqueued workflow id={handle.workflow_id}")
            result = handle.get_result()
            self.stdout.write(self.style.SUCCESS(f"Workflow completed -> {result!r}"))
        finally:
            client.destroy()
