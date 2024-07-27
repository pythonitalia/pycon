from django.utils import timezone
from events.tests.factories import EventFactory
from conferences.tests.factories import ConferenceFactory
from helpers.tests import get_image_url_from_request
from i18n.strings import LazyI18nString
from pytest import mark


@mark.django_db
def test_query_events_with_zero_events(graphql_client):
    now = timezone.now()

    conference = ConferenceFactory(start=now, end=now + timezone.timedelta(days=3))

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
def test_query_events(graphql_client):
    now = timezone.now()

    conference = ConferenceFactory(start=now, end=now + timezone.timedelta(days=3))
    EventFactory(
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
def test_query_events_map(
    graphql_client,
):
    now = timezone.now()

    conference = ConferenceFactory(start=now, end=now + timezone.timedelta(days=3))
    EventFactory(conference=conference, latitude=1, longitude=1)

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


@mark.django_db
def test_query_events_image(
    rf,
    graphql_client,
):
    now = timezone.now()
    request = rf.get("/")

    conference = ConferenceFactory(start=now, end=now + timezone.timedelta(days=3))
    event = EventFactory(conference=conference, latitude=1, longitude=1)

    resp = graphql_client.query(
        """query($code: String!) {
            conference(code: $code) {
                events {
                    image
                }
            }
        }""",
        variables={"code": conference.code},
    )

    assert not resp.get("errors")

    assert len(resp["data"]["conference"]["events"]) == 1
    events = resp["data"]["conference"]["events"]
    events[0]["image"] == get_image_url_from_request(request, event.image)
