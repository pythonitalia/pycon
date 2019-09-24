from django.utils import timezone
from i18n.strings import LazyI18nString
from pytest import mark


@mark.django_db
def test_query_events_with_zero_events(graphql_client, conference_factory):
    now = timezone.now()

    conference = conference_factory(start=now, end=now + timezone.timedelta(days=3))

    resp = graphql_client.query(
        """query($code: String!) {
            conference(code: $code) {
                events {
                    slug
                }
            }
        }""",
        variables={"code": conference.code},
    )

    assert not resp.get("errors")

    assert len(resp["data"]["conference"]["events"]) == 0


@mark.django_db
def test_query_events(graphql_client, conference_factory, event_factory):
    now = timezone.now()

    conference = conference_factory(start=now, end=now + timezone.timedelta(days=3))
    event_factory(
        conference=conference,
        title=LazyI18nString({"en": "hello world", "it": "ciao mondo"}),
        slug=LazyI18nString({"en": "slug", "it": "lumaca"}),
    )

    resp = graphql_client.query(
        """query($code: String!) {
            conference(code: $code) {
                events {
                    title
                    slug
                    titleIt: title(language: "it")
                    slugIt: slug(language: "it")
                }
            }
        }""",
        variables={"code": conference.code},
    )

    assert not resp.get("errors")

    assert len(resp["data"]["conference"]["events"]) == 1
    event = resp["data"]["conference"]["events"][0]

    assert event["title"] == "hello world"
    assert event["titleIt"] == "ciao mondo"
    assert event["slug"] == "slug"
    assert event["slugIt"] == "lumaca"


@mark.django_db
def test_query_events_map(graphql_client, conference_factory, event_factory):
    now = timezone.now()

    conference = conference_factory(start=now, end=now + timezone.timedelta(days=3))
    event_factory(conference=conference, latitude=1, longitude=1)

    resp = graphql_client.query(
        """query($code: String!) {
            conference(code: $code) {
                events {
                    map {
                        latitude
                        longitude
                        link
                        image
                    }
                }
            }
        }""",
        variables={"code": conference.code},
    )

    assert not resp.get("errors")

    assert len(resp["data"]["conference"]["events"]) == 1
    event = resp["data"]["conference"]["events"][0]

    assert event["map"] is not None
