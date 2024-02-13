from api.schema import schema
from django.core.management.base import BaseCommand
from strawberry.printer import print_schema


class Command(BaseCommand):
    def handle(self, *args, **options):
        output = print_schema(schema)

        with open("schema.graphql", "w") as f:
            f.write(output)

        self.stdout.write(
            self.style.SUCCESS("Successfully dumped GraphQL schema to schema.graphql")
        )
