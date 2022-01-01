from pytest import mark


@mark.django_db
def test_get_conference_keynotes_empty(conference_factory, graphql_client):
    conference = conference_factory()

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                keynotes {
                    title
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
def test_get_conference_keynotes(
    conference_factory,
    keynote_factory,
    keynote_speaker_factory,
    graphql_client,
    topic_factory,
):
    conference = conference_factory()

    keynote = keynote_factory(conference=conference, topic=topic_factory())
    speaker = keynote_speaker_factory(keynote=keynote)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                keynotes {
                    title
                    topic {
                        id
                        name
                    }
                    speakers {
                        name
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

    assert keynote_data["title"] == keynote.title
    assert keynote_data["topic"]["id"] == str(keynote.topic.id)
    assert len(keynote_data["speakers"]) == 1

    assert {"name": speaker.name} in keynote_data["speakers"]


@mark.django_db
def test_get_conference_keynotes_without_topic(
    conference_factory,
    keynote_factory,
    keynote_speaker_factory,
    graphql_client,
    topic_factory,
):
    conference = conference_factory()

    keynote = keynote_factory(conference=conference)
    speaker = keynote_speaker_factory(keynote=keynote)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                keynotes {
                    title
                    topic {
                        id
                        name
                    }
                    speakers {
                        name
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

    assert keynote_data["title"] == keynote.title
    assert keynote_data["topic"] is None
    assert len(keynote_data["speakers"]) == 1

    assert {"name": speaker.name} in keynote_data["speakers"]
