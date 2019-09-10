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


def _get_image_url(request, image):
    if not image:
        return None

    return request.build_absolute_uri(image.url)


@mark.django_db
def test_query_sponsors(rf, graphql_client, sponsor_factory, sponsor_level_factory):
    request = rf.get("/")

    gold_level = sponsor_level_factory(name="gold", conference__code="pycon11")
    bronze_level = sponsor_level_factory(name="bronze", conference__code="pycon11")

    sponsor_factory(
        level__name="gold",
        level__conference__code="pycon10",
        name="patrick",
        link="https://patrick.wtf",
        image=None,
        order=0,
    )
    sponsor_factory(
        level=gold_level,
        name="patrick",
        link="https://patrick.wtf",
        image=None,
        order=0,
    )
    sponsor_factory(
        level=gold_level, name="marco", link="https://marco.pizza", image=None, order=1
    )
    sponsor = sponsor_factory(level=bronze_level, name="jake")

    resp = _query_sponsors(graphql_client, conference_code="pycon11")

    assert not resp.get("errors")

    assert len(resp["data"]["conference"]["sponsorsByLevel"]) == 2

    assert {
        "level": "gold",
        "sponsors": [
            {"name": "patrick", "image": None, "link": "https://patrick.wtf"},
            {"name": "marco", "image": None, "link": "https://marco.pizza"},
        ],
    } in resp["data"]["conference"]["sponsorsByLevel"]

    assert {
        "level": "bronze",
        "sponsors": [
            {
                "name": "jake",
                "image": _get_image_url(request, sponsor.image),
                "link": None,
            }
        ],
    } in resp["data"]["conference"]["sponsorsByLevel"]
