import io
from unittest.mock import Mock, mock_open, patch

import strawberry
from django.core.management import call_command


def test_generate_graphql_schema():
    out = io.StringIO()

    m_open = mock_open()

    @strawberry.type
    class TestSchema:
        a: int

    with patch("api.management.commands.graphql_schema.json.dump") as mock_j, patch(
        "api.management.commands.graphql_schema.graphql_sync"
    ) as p, patch("api.management.commands.graphql_schema.open", m_open, create=True):
        m = Mock()
        m.data = {"a": 1}
        p.return_value = m

        call_command("graphql_schema", stdout=out)

    assert "Successfully dumped GraphQL schema to schema.json\n" in out.getvalue()

    mock_j.assert_called_once()
    assert mock_j.call_args_list[0][0][0] == {"data": {"a": 1}}
