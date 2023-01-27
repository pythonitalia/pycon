import time_machine
from django.utils import timezone
from pytest import mark

from i18n.strings import LazyI18nString


@mark.django_db
def test_get_conference_keynotes_empty(conference_factory, graphql_client):
    conference = conference_factory()

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                keynotes {
                    title(language: "en")
                    speakers {
                        id
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["keynotes"] == []


@mark.django_db
@time_machine.travel("2020-10-10 10:00:00Z", tick=False)
def test_get_conference_keynotes(
    conference_factory,
    keynote_factory,
    keynote_speaker_factory,
    graphql_client,
    topic_factory,
    participant_factory,
):
    conference = conference_factory()

    keynote = keynote_factory(
        title=LazyI18nString({"en": "title", "it": "titolo"}),
        conference=conference,
        topic=topic_factory(),
        published=timezone.datetime(1995, 12, 1, 5, 10, 3),
    )
    speaker = keynote_speaker_factory(keynote=keynote)
    participant_factory(
        user_id=speaker.user_id,
        conference_id=conference.id,
        bio="test",
        photo="https://test.it/test.jpg",
    )

    future_keynote = keynote_factory(
        title=LazyI18nString({"en": "nope", "it": "noope"}),
        conference=conference,
        topic=topic_factory(),
        published=timezone.datetime(2050, 12, 1, 5, 10, 3),
    )
    keynote_speaker_factory(keynote=future_keynote)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                keynotes {
                    titleEn: title(language: "en")
                    titleIt: title(language: "it")
                    topic {
                        id
                        name
                    }
                    speakers {
                        participant {
                            photo
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert len(resp["data"]["conference"]["keynotes"]) == 1

    keynote_data = resp["data"]["conference"]["keynotes"][0]

    assert keynote_data["titleEn"] == "title"
    assert keynote_data["titleIt"] == "titolo"
    assert keynote_data["topic"]["id"] == str(keynote.topic.id)
    assert len(keynote_data["speakers"]) == 1

    assert {"participant": {"photo": "https://test.it/test.jpg"}} in keynote_data[
        "speakers"
    ]


@mark.django_db
def test_get_single_conference_keynote(
    conference_factory,
    keynote_factory,
    keynote_speaker_factory,
    graphql_client,
    topic_factory,
    participant_factory,
):
    conference = conference_factory()

    keynote = keynote_factory(
        slug=LazyI18nString({"en": "title", "it": "titolo"}),
        title=LazyI18nString({"en": "title", "it": "titolo"}),
        conference=conference,
        topic=topic_factory(),
    )
    speaker = keynote_speaker_factory(keynote=keynote)
    participant_factory(
        user_id=speaker.user_id, conference_id=conference.id, bio="test"
    )

    resp = graphql_client.query(
        """
        query($code: String!, $slug: String!) {
            conference(code: $code) {
                keynote(slug: $slug) {
                    title(language: "en")
                    topic {
                        id
                        name
                    }
                    speakers {
                        participant {
                            bio
                        }
                    }
                }
            }
        }
        """,
        variables={"code": conference.code, "slug": "title"},
    )

    assert "errors" not in resp

    keynote_data = resp["data"]["conference"]["keynote"]

    assert keynote_data["title"] == "title"
    assert keynote_data["topic"]["id"] == str(keynote.topic.id)
    assert len(keynote_data["speakers"]) == 1

    assert {"participant": {"bio": "test"}} in keynote_data["speakers"]
