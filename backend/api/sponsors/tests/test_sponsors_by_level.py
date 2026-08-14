from unittest.mock import ANY

from pytest import mark

from conferences.tests.factories import ConferenceFactory
from sponsors.tests.factories import SponsorFactory, SponsorLevelFactory


def _query_sponsors(client, conference_code):
    return client.query(
        """query Sponsors($code: String!) {
            conference(code: $code) {
                sponsorsByLevel {
                    level
                    sponsors {
                        name
                        image
                        link
                    }
                }
            }
        }""",
        variables={"code": conference_code},
    )


@mark.django_db
def test_query_sponsors(graphql_client):
    conference = ConferenceFactory()
    patrick = SponsorFactory(
        name="patrick",
        link="https://patrick.wtf",
        image=None,
        order=0,
    )
    marco = SponsorFactory(
        name="marco", link="https://marco.pizza", image=None, order=1
    )
    ester = SponsorFactory(name="ester", link="https://ester.cool", order=0)
    SponsorLevelFactory(name="gold", conference=conference, sponsors=[patrick, marco])
    SponsorLevelFactory(name="bronze", conference=conference, sponsors=[ester])

    resp = _query_sponsors(graphql_client, conference_code=conference.code)

    assert not resp.get("errors")
    assert len(resp["data"]["conference"]["sponsorsByLevel"]) == 2
    assert resp["data"]["conference"]["sponsorsByLevel"][0] == {
        "level": "gold",
        "sponsors": [
            {
                "name": patrick.name,
                "image": "",
                "link": patrick.link,
            },
            {
                "name": "marco",
                "image": "",
                "link": "https://marco.pizza",
            },
        ],
    }
    assert resp["data"]["conference"]["sponsorsByLevel"][1] == {
        "level": "bronze",
        "sponsors": [
            {
                "name": "ester",
                "image": ANY,
                "link": "https://ester.cool",
            }
        ],
    }
    assert (
        "/CACHE/images/sponsors"
        in resp["data"]["conference"]["sponsorsByLevel"][1]["sponsors"][0]["image"]
    )


@mark.parametrize("level_count", [1, 4])
@mark.django_db
def test_frontend_sponsors_query_is_constant(
    graphql_client, django_assert_num_queries, level_count
):
    conference = ConferenceFactory()
    for index in range(level_count):
        sponsor = SponsorFactory(image=None, order=index)
        SponsorLevelFactory(
            conference=conference,
            name=f"level-{index}",
            sponsors=[sponsor],
        )

    with django_assert_num_queries(3):
        resp = graphql_client.query(
            """
            query SponsorsSection($code: String!) {
                conference(code: $code) {
                    id
                    sponsorsByLevel {
                        name: level
                        sponsors {
                            id
                            name
                            url: link
                            logo: image
                        }
                    }
                }
            }
            """,
            variables={"code": conference.code},
        )

    assert "errors" not in resp
    assert len(resp["data"]["conference"]["sponsorsByLevel"]) == level_count
