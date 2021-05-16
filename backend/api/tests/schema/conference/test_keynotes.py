from pytest import mark

from schedule.models import ScheduleItem


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
def test_get_conference_keynotes_returns_only_keynotes(
    conference_factory, schedule_item_factory, graphql_client
):
    conference = conference_factory()

    schedule_item_factory(conference=conference, type=ScheduleItem.TYPES.submission)
    keynote = schedule_item_factory(
        conference=conference,
        type=ScheduleItem.TYPES.keynote,
        additional_speakers__size=1,
    )
    speaker_id = keynote.submission.speaker_id
    additional_speaker = keynote.additional_speakers.first().user_id

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
    assert len(resp["data"]["conference"]["keynotes"])

    keynote_data = resp["data"]["conference"]["keynotes"][0]

    assert keynote_data["title"] == keynote.title
    assert len(keynote_data["speakers"]) == 2

    assert {"id": str(speaker_id)} in keynote_data["speakers"]
    assert {
        "id": str(additional_speaker),
    } in keynote_data["speakers"]
