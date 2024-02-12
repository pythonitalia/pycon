from django.core.management import call_command


def test_export_graphql_schema_command():
    call_command("graphql_schema")
    with open("./schema.graphql", "r") as file_:
        schema = file_.read()

    assert "type Query" in schema
