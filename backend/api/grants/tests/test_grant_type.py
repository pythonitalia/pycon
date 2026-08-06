import pytest

from generic_forms.models import Form
from generic_forms.tests.factories import FormAnswerFactory, FormFactory
from grants.tests.factories import GrantFactory

pytestmark = pytest.mark.django_db


def _query_my_grant(graphql_client, conference):
    query = """query($conference: String!) {
        me {
            grant(conference: $conference) {
                id
                formAnswers
            }
        }
    }"""

    return graphql_client.query(query, variables={"conference": conference.code})


def test_form_answers_are_exposed_as_a_flat_map(graphql_client, user):
    graphql_client.force_login(user)
    grant = GrantFactory(user=user)
    form = FormFactory(conference=grant.conference, purpose=Form.Purpose.GRANT)
    grant.form_answer = FormAnswerFactory(
        form=form,
        user=user,
        answers={"version": 1, "answers": {"12": "My motivation", "13": ["vegan"]}},
    )
    grant.save()

    result = _query_my_grant(graphql_client, grant.conference)

    assert result["data"]["me"]["grant"]["formAnswers"] == {
        "12": "My motivation",
        "13": ["vegan"],
    }


def test_form_answers_are_null_for_legacy_grants(graphql_client, user):
    graphql_client.force_login(user)
    grant = GrantFactory(user=user)

    result = _query_my_grant(graphql_client, grant.conference)

    assert result["data"]["me"]["grant"]["formAnswers"] is None
