import datetime
import pytest
import time_machine
from django.utils import timezone
from pytest import mark
import zoneinfo

from api.conferences.types import DeadlineStatus


@mark.django_db
def test_get_conference_info(conference, graphql_client):
    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                id
                code
                name
                introduction
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert {
        "id": str(conference.id),
        "code": conference.code,
        "name": str(conference.name),
        "introduction": str(conference.introduction),
    } == resp["data"]["conference"]


@mark.django_db
def test_get_conference_deadlines_ordered_by_start_date(
    graphql_client, conference_factory, deadline_factory
):
    now = timezone.now()

    conference = conference_factory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    deadline_voting = deadline_factory(
        start=now - timezone.timedelta(days=20),
        end=now - timezone.timedelta(days=15),
        conference=conference,
        type="voting",
    )

    deadline_cfp = deadline_factory(
        start=now - timezone.timedelta(days=1),
        end=now,
        conference=conference,
        type="cfp",
    )

    deadline_refund = deadline_factory(
        start=now - timezone.timedelta(days=14),
        end=now - timezone.timedelta(days=10),
        conference=conference,
        type="refund",
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                start
                end
                timezone
                deadlines {
                    start
                    end
                    type
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert resp["data"]["conference"]["timezone"] == "America/Los_Angeles"

    assert resp["data"]["conference"]["start"] == conference.start.isoformat()
    assert resp["data"]["conference"]["end"] == conference.end.isoformat()

    assert {
        "start": deadline_voting.start.isoformat(),
        "end": deadline_voting.end.isoformat(),
        "type": "voting",
    } == resp["data"]["conference"]["deadlines"][0]

    assert {
        "start": deadline_refund.start.isoformat(),
        "end": deadline_refund.end.isoformat(),
        "type": "refund",
    } == resp["data"]["conference"]["deadlines"][1]

    assert {
        "start": deadline_cfp.start.isoformat(),
        "end": deadline_cfp.end.isoformat(),
        "type": "cfp",
    } == resp["data"]["conference"]["deadlines"][2]


@mark.django_db
def test_get_conference_single_deadline(
    graphql_client, conference_factory, deadline_factory
):
    now = timezone.now()

    conference = conference_factory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    deadline_cfp = deadline_factory(
        start=now - timezone.timedelta(days=1),
        end=now,
        conference=conference,
        type="cfp",
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                deadline(type: "cfp") {
                    start
                    end
                    type
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert {
        "start": deadline_cfp.start.isoformat(),
        "end": deadline_cfp.end.isoformat(),
        "type": "cfp",
    } == resp["data"]["conference"]["deadline"]


@mark.django_db
@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_get_conference_deadline_status(
    graphql_client, conference_factory, deadline_factory
):
    now = timezone.now()

    conference = conference_factory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    # CFP happening now
    deadline_factory(
        start=now - timezone.timedelta(days=1),
        end=now + timezone.timedelta(days=3),
        conference=conference,
        type="cfp",
    )

    # Grants in the past
    deadline_factory(
        start=now - timezone.timedelta(days=3),
        end=now - timezone.timedelta(days=1),
        conference=conference,
        type="grants",
    )

    # Voting in the future
    deadline_factory(
        start=now + timezone.timedelta(days=10),
        end=now + timezone.timedelta(days=15),
        conference=conference,
        type="voting",
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                deadlineCfp: deadline(type: "cfp") {
                    status
                }
                deadlineGrants: deadline(type: "grants") {
                    status
                }
                deadlineVoting: deadline(type: "voting") {
                    status
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert not resp.get("errors")

    assert {"status": DeadlineStatus.HAPPENING_NOW.name} == resp["data"]["conference"][
        "deadlineCfp"
    ]

    assert {"status": DeadlineStatus.IN_THE_PAST.name} == resp["data"]["conference"][
        "deadlineGrants"
    ]

    assert {"status": DeadlineStatus.IN_THE_FUTURE.name} == resp["data"]["conference"][
        "deadlineVoting"
    ]


@mark.django_db
def test_get_not_existent_conference_info(conference, graphql_client):
    resp = graphql_client.query(
        """
        {
            conference(code: "random-conference-code") {
                name
            }
        }
        """
    )

    assert "errors" in resp
    assert resp["errors"][0]["message"] == "Conference matching query does not exist."


@mark.django_db
def test_query_conference_audience_levels(
    graphql_client, conference, audience_level_factory
):
    level1 = audience_level_factory()
    level2 = audience_level_factory()
    level3 = audience_level_factory()

    conference.audience_levels.add(level1, level2, level3)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                audienceLevels {
                    id
                    name
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp

    assert {"name": level1.name, "id": str(level1.id)} in resp["data"]["conference"][
        "audienceLevels"
    ]

    assert {"name": level2.name, "id": str(level2.id)} in resp["data"]["conference"][
        "audienceLevels"
    ]

    assert {"name": level3.name, "id": str(level3.id)} in resp["data"]["conference"][
        "audienceLevels"
    ]


@mark.django_db
def test_query_conference_topics(graphql_client, conference, topic_factory):
    topic1 = topic_factory()
    topic2 = topic_factory()
    topic3 = topic_factory()

    conference.topics.add(topic1, topic2, topic3)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                topics {
                    id
                    name
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp

    assert {"name": topic1.name, "id": str(topic1.id)} in resp["data"]["conference"][
        "topics"
    ]

    assert {"name": topic2.name, "id": str(topic2.id)} in resp["data"]["conference"][
        "topics"
    ]

    assert {"name": topic3.name, "id": str(topic3.id)} in resp["data"]["conference"][
        "topics"
    ]


@mark.django_db
def test_query_conference_languages(graphql_client, conference, language):
    lang_it = language("it")
    lang_en = language("en")

    conference.languages.add(lang_en, lang_it)

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                languages {
                    id
                    name
                    code
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp

    assert {"name": lang_it.name, "code": lang_it.code, "id": str(lang_it.id)} in resp[
        "data"
    ]["conference"]["languages"]

    assert {"name": lang_en.name, "code": lang_en.code, "id": str(lang_en.id)} in resp[
        "data"
    ]["conference"]["languages"]


@mark.django_db
def test_get_conference_durations(
    graphql_client, duration_factory, submission_type_factory
):
    talk_type = submission_type_factory(name="talk")
    tutorial_type = submission_type_factory(name="tutorial")

    d1 = duration_factory()
    d1.allowed_submission_types.add(talk_type)
    d2 = duration_factory(conference=d1.conference)
    d2.allowed_submission_types.add(tutorial_type)

    conference = d1.conference

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                durations {
                    id
                    name
                    duration
                    notes
                    allowedSubmissionTypes {
                        id
                        name
                    }
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert {
        "id": str(d1.id),
        "name": d1.name,
        "duration": d1.duration,
        "notes": d1.notes,
        "allowedSubmissionTypes": [{"id": str(talk_type.id), "name": talk_type.name}],
    } in resp["data"]["conference"]["durations"]

    assert {
        "id": str(d2.id),
        "name": d2.name,
        "duration": d2.duration,
        "notes": d2.notes,
        "allowedSubmissionTypes": [
            {"id": str(tutorial_type.id), "name": tutorial_type.name}
        ],
    } in resp["data"]["conference"]["durations"]


@mark.django_db
def test_get_conference_without_map(conference, graphql_client):
    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                map {
                    latitude
                    longitude
                    link
                    image
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["map"] is None


@mark.django_db
def test_get_conference_map(conference_factory, graphql_client):
    conference = conference_factory(latitude=1, longitude=1)
    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                map {
                    latitude
                    longitude
                    link
                    image
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["map"] is not None


@mark.django_db
def test_get_conference_submission_types(
    graphql_client, conference_factory, submission_type_factory
):
    talk_type = submission_type_factory(name="talk")
    tutorial_type = submission_type_factory(name="tutorial")
    conference = conference_factory(submission_types=[talk_type, tutorial_type])

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                submissionTypes {
                    id
                    name
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["submissionTypes"] == [
        {"id": str(talk_type.id), "name": talk_type.name},
        {"id": str(tutorial_type.id), "name": tutorial_type.name},
    ]


@mark.django_db
def test_get_conference_hotel_rooms(
    graphql_client, conference_factory, bed_layout_factory, hotel_room
):
    hotel_room.conference = conference_factory(
        start=timezone.datetime(2019, 1, 1, tzinfo=datetime.timezone.utc),
        end=timezone.datetime(2019, 1, 5, tzinfo=datetime.timezone.utc),
    )

    bed_layout = bed_layout_factory()
    hotel_room.available_bed_layouts.add(bed_layout)

    hotel_room.save()

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                hotelRooms {
                    id
                    name(language: "it")
                    description(language: "it")
                    price
                    availableBedLayouts {
                        id
                        name(language: "en")
                    }
                    checkInDates
                    checkOutDates
                }
            }
        }
        """,
        variables={"code": hotel_room.conference.code},
    )

    assert "errors" not in resp
    assert resp["data"]["conference"]["hotelRooms"] == [
        {
            "id": str(hotel_room.id),
            "name": hotel_room.name.localize("it"),
            "description": hotel_room.description.localize("it"),
            "price": f"{hotel_room.price:0.2f}",
            "checkInDates": ["2019-01-01", "2019-01-02", "2019-01-03", "2019-01-04"],
            "checkOutDates": ["2019-01-02", "2019-01-03", "2019-01-04", "2019-01-05"],
            "availableBedLayouts": [
                {"name": bed_layout.name.localize("en"), "id": str(bed_layout.id)},
            ],
        }
    ]


@mark.django_db
@mark.parametrize("cfp_open", (True, False))
def test_is_cfp_open(graphql_client, conference_factory, deadline_factory, cfp_open):
    now = timezone.now()

    conference = conference_factory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    deadline_factory(
        start=now - timezone.timedelta(days=1),
        end=now + timezone.timedelta(days=1) if cfp_open else now,
        conference=conference,
        type="cfp",
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                isCFPOpen
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert resp["data"]["conference"]["isCFPOpen"] is cfp_open


@mark.django_db
def test_is_cfp_open_false_when_no_deadline(graphql_client, conference):
    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                isCFPOpen
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert resp["data"]["conference"]["isCFPOpen"] is False


@mark.django_db
@mark.parametrize("voting_open", (True, False))
def test_is_voting_open(
    graphql_client, conference_factory, deadline_factory, voting_open
):
    now = timezone.now()

    conference = conference_factory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    deadline_factory(
        start=now - timezone.timedelta(days=1),
        end=now + timezone.timedelta(days=1) if voting_open else now,
        conference=conference,
        type="voting",
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                isVotingOpen
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert resp["data"]["conference"]["isVotingOpen"] is voting_open


@mark.django_db
def test_is_voting_open_false_when_no_deadlines(graphql_client, conference):
    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                isVotingOpen
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert resp["data"]["conference"]["isVotingOpen"] is False


@mark.django_db
def test_is_voting_closed_in_the_past(
    graphql_client,
    conference_factory,
    deadline_factory,
):
    now = timezone.now()
    conference = conference_factory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    deadline_factory(
        start=now - timezone.timedelta(days=2),
        end=now - timezone.timedelta(days=1),
        conference=conference,
        type="voting",
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                isVotingClosed
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert resp["data"]["conference"]["isVotingClosed"] is True


@pytest.mark.xfail(reason="it only check if the deadline has passed atm")
@mark.django_db
def test_is_voting_closed_in_the_future(
    graphql_client,
    conference_factory,
    deadline_factory,
):
    now = timezone.now()
    conference = conference_factory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    deadline_factory(
        start=now + timezone.timedelta(days=1),
        end=now + timezone.timedelta(days=2),
        conference=conference,
        type="voting",
    )

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                isVotingClosed
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert resp["data"]["conference"]["isVotingClosed"] is True


@mark.django_db
def test_can_see_submissions_as_staff(graphql_client, submission_factory, user_factory):
    user = user_factory(is_staff=True)
    submission = submission_factory()

    graphql_client.force_login(user)

    response = graphql_client.query(
        """query($code: String!) {
            conference(code: $code) {
                submissions {
                    id
                }
            }
        }""",
        variables={"code": submission.conference.code},
    )

    assert len(response["data"]["conference"]["submissions"]) == 1


@mark.django_db
def test_can_see_submissions_if_they_have_sent_one(
    graphql_client, conference, submission_factory, user_factory
):
    user = user_factory()
    submission_factory(conference=conference)
    submission_factory(conference=conference, speaker_id=user.id)

    graphql_client.force_login(user)

    response = graphql_client.query(
        """query($code: String!) {
            conference(code: $code) {
                submissions {
                    id
                }
            }
        }""",
        variables={"code": conference.code},
    )

    assert len(response["data"]["conference"]["submissions"]) == 2


@mark.django_db
def test_get_conference_voucher_with_invalid_code(
    graphql_client, conference, mocker, requests_mock
):
    requests_mock.get(
        "https://pretix/api/organizers/base-pretix-organizer-id/events/base-pretix-event-id/extended-vouchers/test/",
        status_code=404,
    )
    response = graphql_client.query(
        """query($code: String!, $voucherCode: String!) {
            conference(code: $code) {
                voucher(code: $voucherCode) {
                    id
                }
            }
        }""",
        variables={"code": conference.code, "voucherCode": "test"},
    )

    assert response["data"]["conference"]["voucher"] is None


@mark.django_db
def test_get_conference_voucher_with_valid_until(
    graphql_client, conference, mocker, requests_mock, settings
):
    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/extended-vouchers/test/",
        status_code=200,
        json={
            "id": 1,
            "code": "test",
            "valid_until": "2023-05-27T22:00:00Z",
            "value": 10,
            "item": 1,
            "variation": None,
            "redeemed": 0,
            "price_mode": "set",
            "max_usages": 3,
        },
    )
    response = graphql_client.query(
        """query($code: String!, $voucherCode: String!) {
            conference(code: $code) {
                voucher(code: $voucherCode) {
                    id
                    validUntil
                }
            }
        }""",
        variables={"code": conference.code, "voucherCode": "test"},
    )

    assert not response.get("errors")
    assert response["data"]["conference"]["voucher"] == {
        "id": "1",
        "validUntil": "2023-05-27T22:00:00+00:00",
    }


@mark.django_db
def test_get_conference_voucher(
    graphql_client, conference, mocker, requests_mock, settings
):
    requests_mock.get(
        f"{settings.PRETIX_API}organizers/base-pretix-organizer-id/events/base-pretix-event-id/extended-vouchers/test/",
        status_code=200,
        json={
            "id": 1,
            "code": "test",
            "valid_until": None,
            "value": 10,
            "item": 1,
            "variation": None,
            "redeemed": 0,
            "price_mode": "set",
            "max_usages": 3,
        },
    )
    response = graphql_client.query(
        """query($code: String!, $voucherCode: String!) {
            conference(code: $code) {
                voucher(code: $voucherCode) {
                    id
                    validUntil
                    value
                    items
                    allItems
                    redeemed
                    maxUsages
                }
            }
        }""",
        variables={"code": conference.code, "voucherCode": "test"},
    )

    assert not response.get("errors")
    assert response["data"]["conference"]["voucher"] == {
        "id": "1",
        "validUntil": None,
        "value": "10",
        "items": ["1"],
        "allItems": False,
        "redeemed": 0,
        "maxUsages": 3,
    }


@mark.django_db
def test_filter_submission_by_status(
    graphql_client, submission_factory, conference, user, requests_mock, settings
):
    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": True},
    )

    submission_factory(conference=conference, status="cancelled")
    submission_factory(conference=conference, status="proposed")
    graphql_client.force_login(user)

    query = """
        query($code: String!) {
            conference(code: $code) {
                submissions{
                    id
                    status
                }
            }
        }
    """

    response = graphql_client.query(
        query,
        variables={"code": conference.code},
    )

    assert len(response["data"]["conference"]["submissions"]) == 1
    assert response["data"]["conference"]["submissions"][0]["status"] == "proposed"
