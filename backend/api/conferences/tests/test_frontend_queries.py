from datetime import UTC, datetime

from pytest import mark

from conferences.tests.factories import ConferenceFactory, DeadlineFactory

INFORMATION_SECTION_QUERY = """
    query InformationSection($code: String!) {
      conference(code: $code) {
        id
        cfp: deadline(type: "cfp") {
          id
          start
          end
        }

        voting: deadline(type: "voting") {
          id
          start
          end
        }

        grants: deadline(type: "grants") {
          id
          start
          end
        }
      }
    }
"""


@mark.django_db
def test_frontend_information_section_query(
    graphql_client,
    django_assert_num_queries,
):
    conference = ConferenceFactory()
    deadlines = {
        deadline_type: DeadlineFactory(
            conference=conference,
            type=deadline_type,
            start=datetime(2026, month, 1, tzinfo=UTC),
            end=datetime(2026, month, 2, tzinfo=UTC),
        )
        for month, deadline_type in enumerate(("cfp", "voting", "grants"), start=1)
    }

    with django_assert_num_queries(4):
        response = graphql_client.query(
            INFORMATION_SECTION_QUERY,
            variables={"code": conference.code},
        )

    assert "errors" not in response
    assert response["data"] == {
        "conference": {
            "id": str(conference.id),
            **{
                deadline_type: {
                    "id": str(deadline.id),
                    "start": deadline.start.isoformat(),
                    "end": deadline.end.isoformat(),
                }
                for deadline_type, deadline in deadlines.items()
            },
        }
    }
