import json

from api.schema import schema
from django.core.management.base import BaseCommand
from graphql import get_introspection_query, graphql_sync


class Command(BaseCommand):
    def handle(self, *args, **options):
        query = get_introspection_query(descriptions=False)
        result = graphql_sync(schema, query)

        output = {"data": result.data}

        with open("schema.json", "w") as f:
            json.dump(output, f, indent=4, sort_keys=True)

        self.stdout.write(
            self.style.SUCCESS("Successfully dumped GraphQL schema to schema.json")
        )
