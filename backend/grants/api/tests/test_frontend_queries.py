from datetime import UTC, datetime

from pytest import mark

from generic_forms.models import Form
from generic_forms.tests.factories import FormAnswerFactory, FormFactory
from grants.models import Grant
from grants.tests.factories import GrantFactory

MY_GRANT_QUERY = """
    query MyGrant($conference: String!) {
      me {
        id

        grant(conference: $conference) {
          id
          status
          fullName
          name
          gender
          grantType
          occupation
          needsFundsForTravel
          needVisa
          needAccommodation
          departureCountry
          nationality
          departureCity
          formAnswers
        }
      }
    }
"""


@mark.django_db
def test_frontend_my_grant_query(graphql_client, django_assert_num_queries, user):
    graphql_client.force_login(user)
    grant = GrantFactory(
        user=user,
        status=Grant.Status.approved,
        name="Patrick",
        full_name="Patrick Arminio",
        gender="male",
        grant_type=[Grant.GrantType.speaker],
        occupation=Grant.Occupation.developer,
        needs_funds_for_travel=True,
        need_visa=False,
        need_accommodation=True,
        departure_country="IT",
        nationality="Italian",
        departure_city="Bologna",
        applicant_reply_deadline=datetime(2026, 1, 1, tzinfo=UTC),
    )
    form = FormFactory(conference=grant.conference, purpose=Form.Purpose.GRANT)
    grant.form_answer = FormAnswerFactory(
        form=form,
        user=user,
        answers={"version": 1, "answers": {"12": "My motivation"}},
    )
    grant.save()

    with django_assert_num_queries(3):
        response = graphql_client.query(
            MY_GRANT_QUERY,
            variables={"conference": grant.conference.code},
        )

    assert response["data"]["me"]["grant"] == {
        "id": str(grant.id),
        "status": "approved",
        "fullName": "Patrick Arminio",
        "name": "Patrick",
        "gender": "male",
        "grantType": ["speaker"],
        "occupation": "developer",
        "needsFundsForTravel": True,
        "needVisa": False,
        "needAccommodation": True,
        "departureCountry": "IT",
        "nationality": "Italian",
        "departureCity": "Bologna",
        "formAnswers": {"12": "My motivation"},
    }
