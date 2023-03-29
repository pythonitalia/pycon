from unittest.mock import ANY
from pytest import mark


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
def test_query_sponsors(rf, graphql_client, sponsor_factory, sponsor_level_factory):
    patrick = sponsor_factory(
        name="patrick",
        link="https://patrick.wtf",
        image=None,
        order=0,
    )
    marco = sponsor_factory(
        name="marco", link="https://marco.pizza", image=None, order=1
    )
    ester = sponsor_factory(name="ester", link="https://ester.cool", order=0)
    sponsor_level_factory(
        name="gold", conference__code="pycon12", sponsors=[patrick, marco]
    )
    sponsor_level_factory(name="bronze", conference__code="pycon12", sponsors=[ester])

    resp = _query_sponsors(graphql_client, conference_code="pycon12")

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
    assert resp["data"]["conference"]["sponsorsByLevel"][1]["sponsors"][0][
        "image"
    ].startswith("http://testserver/media/CACHE")
