from django.core.management.base import BaseCommand
from strawberry.printer import print_schema

from api.schema import schema


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
        )

    def handle(self, *args, **options):
        file = options["file"]
        with open(file, "w") as f:
            f.write(print_schema(schema))

        self.stdout.write(self.style.SUCCESS("Successfully dumped GraphQL schema"))
