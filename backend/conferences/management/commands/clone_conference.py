"""Trigger the clone-conference durable workflow."""

from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime

from conferences.models import Conference
from conferences.workflows import CLONE_CONFERENCE
from pycon.resonate_app import start_workflow


class Command(BaseCommand):
    help = "Create a new conference using an existing one as base"

    def add_arguments(self, parser):
        parser.add_argument("source_code", help="Code of the conference to copy")
        parser.add_argument("new_code", help="Code of the conference to create")
        parser.add_argument("--name", required=True, help="Name of the new conference")
        parser.add_argument(
            "--hostname", required=True, help="Hostname of the new conference"
        )
        parser.add_argument(
            "--start", required=True, help="Start date (ISO 8601, with timezone)"
        )
        parser.add_argument(
            "--end", required=True, help="End date (ISO 8601, with timezone)"
        )
        parser.add_argument(
            "--workflow-id",
            default=None,
            help=(
                "Workflow id, the idempotency key of the run. "
                "Defaults to clone-conference-<new_code>."
            ),
        )

    def handle(self, *args, **options):
        source_code = options["source_code"]

        if not Conference.objects.filter(code=source_code).exists():
            raise CommandError(f"Conference {source_code} does not exist")

        start = self._parse_datetime(options["start"], "--start")
        end = self._parse_datetime(options["end"], "--end")

        if start > end:
            raise CommandError("--start cannot be after --end")

        new_code = options["new_code"]
        workflow_id = options["workflow_id"] or f"clone-conference-{new_code}"

        start_workflow(
            CLONE_CONFERENCE,
            workflow_id,
            source_code=source_code,
            new_code=new_code,
            new_name=options["name"],
            new_start=start.isoformat(),
            new_end=end.isoformat(),
            new_hostname=options["hostname"],
        )

        self.stdout.write(
            self.style.SUCCESS(f"Started workflow {workflow_id}, follow it in Resonate")
        )

    def _parse_datetime(self, value, flag):
        parsed = parse_datetime(value)

        if parsed is None:
            raise CommandError(f"{flag} is not a valid ISO 8601 datetime: {value}")

        return parsed
