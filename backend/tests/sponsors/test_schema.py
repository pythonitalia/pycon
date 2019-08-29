from pytest import mark


def _query_sponsors(client, conference_code):
    return client.query(
        """query Sponsors($code: String!) {
            sponsorsByLevel(code: $code) {
                level
                sponsors {
                    name
                    image
                    link
                }
            }
        }""",
        variables={"code": conference_code},
    )


def _get_image_url(request, image):
    if not image:
        return None

    return request.build_absolute_uri(image.url)


@mark.django_db
def test_query_sponsors(rf, graphql_client, sponsor_factory):
    request = rf.get("/")

    sponsor_factory(
        conference__code="pycon10",
        name="patrick",
        link="https://patrick.wtf",
        level="gold",
        image=None,
    )
    sponsor_factory(
        conference__code="pycon11",
        name="patrick",
        link="https://patrick.wtf",
        level="gold",
        image=None,
    )
    sponsor_factory(
        conference__code="pycon11",
        name="marco",
        link="https://marco.pizza",
        level="gold",
        image=None,
    )
    sponsor = sponsor_factory(conference__code="pycon11", name="jake", level="bronze")

    resp = _query_sponsors(graphql_client, conference_code="pycon11")

    assert not resp.get("errors")

    assert len(resp["data"]["sponsorsByLevel"]) == 2

    assert {
        "level": "gold",
        "sponsors": [
            {"name": "patrick", "image": None, "link": "https://patrick.wtf"},
            {"name": "marco", "image": None, "link": "https://marco.pizza"},
        ],
    } in resp["data"]["sponsorsByLevel"]

    assert {
        "level": "bronze",
        "sponsors": [
            {
                "name": "jake",
                "image": _get_image_url(request, sponsor.image),
                "link": None,
            }
        ],
    } in resp["data"]["sponsorsByLevel"]
