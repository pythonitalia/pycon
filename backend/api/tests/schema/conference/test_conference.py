from users.tests.factories import UserFactory
from submissions.tests.factories import (
    SubmissionFactory,
    SubmissionTagFactory,
    SubmissionTypeFactory,
)
from conferences.tests.factories import (
    AudienceLevelFactory,
    ConferenceFactory,
    DeadlineFactory,
    DurationFactory,
    TopicFactory,
)
import pytest
import time_machine
from django.utils import timezone
from pytest import mark
import zoneinfo

from api.conferences.types import DeadlineStatus


pytestmark = mark.django_db


def test_get_conference_info(graphql_client):
    conference = ConferenceFactory()
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


def test_get_conference_deadlines_ordered_by_start_date(
    graphql_client,
):
    now = timezone.now()

    conference = ConferenceFactory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    deadline_voting = DeadlineFactory(
        start=now - timezone.timedelta(days=20),
        end=now - timezone.timedelta(days=15),
        conference=conference,
        type="voting",
    )

    deadline_cfp = DeadlineFactory(
        start=now - timezone.timedelta(days=1),
        end=now,
        conference=conference,
        type="cfp",
    )

    deadline_refund = DeadlineFactory(
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


def test_get_conference_single_deadline(
    graphql_client,
):
    now = timezone.now()

    conference = ConferenceFactory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    deadline_cfp = DeadlineFactory(
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


@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_get_conference_deadline_status(
    graphql_client,
):
    now = timezone.now()

    conference = ConferenceFactory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    # CFP happening now
    DeadlineFactory(
        start=now - timezone.timedelta(days=1),
        end=now + timezone.timedelta(days=3),
        conference=conference,
        type="cfp",
    )

    # Grants in the past
    DeadlineFactory(
        start=now - timezone.timedelta(days=3),
        end=now - timezone.timedelta(days=1),
        conference=conference,
        type="grants",
    )

    # Voting in the future
    DeadlineFactory(
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


def test_get_not_existent_conference_info(graphql_client):
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


def test_query_conference_audience_levels(graphql_client):
    conference = ConferenceFactory()

    level1 = AudienceLevelFactory()
    level2 = AudienceLevelFactory()
    level3 = AudienceLevelFactory()

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


def test_query_conference_topics(graphql_client):
    conference = ConferenceFactory()
    topic1 = TopicFactory()
    topic2 = TopicFactory()
    topic3 = TopicFactory()

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


def test_query_conference_languages(graphql_client, language):
    conference = ConferenceFactory()
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


def test_get_conference_durations(
    graphql_client,
):
    talk_type = SubmissionTypeFactory(name="talk")
    tutorial_type = SubmissionTypeFactory(name="tutorial")

    d1 = DurationFactory()
    d1.allowed_submission_types.add(talk_type)
    d2 = DurationFactory(conference=d1.conference)
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


def test_get_conference_without_map(graphql_client):
    conference = ConferenceFactory()
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


def test_get_conference_map(graphql_client):
    conference = ConferenceFactory(latitude=1, longitude=1)
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


def test_get_conference_submission_types(
    graphql_client,
):
    talk_type = SubmissionTypeFactory(name="talk")
    tutorial_type = SubmissionTypeFactory(name="tutorial")
    conference = ConferenceFactory(submission_types=[talk_type, tutorial_type])

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


@mark.parametrize("cfp_open", (True, False))
def test_is_cfp_open(graphql_client, cfp_open):
    now = timezone.now()

    conference = ConferenceFactory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    DeadlineFactory(
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


def test_is_cfp_open_false_when_no_deadline(graphql_client):
    conference = ConferenceFactory()

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


@mark.parametrize("voting_open", (True, False))
def test_is_voting_open(graphql_client, voting_open):
    now = timezone.now()

    conference = ConferenceFactory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    DeadlineFactory(
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


def test_is_voting_open_false_when_no_deadlines(graphql_client):
    conference = ConferenceFactory()

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


def test_is_voting_closed_in_the_past(
    graphql_client,
):
    now = timezone.now()
    conference = ConferenceFactory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    DeadlineFactory(
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
def test_is_voting_closed_in_the_future(
    graphql_client,
):
    now = timezone.now()
    conference = ConferenceFactory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    DeadlineFactory(
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


def test_can_see_submissions_as_staff(graphql_client):
    user = UserFactory(is_staff=True)
    submission = SubmissionFactory()

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


def test_can_see_submissions_if_they_have_sent_one(graphql_client):
    conference = ConferenceFactory()

    user = UserFactory()
    SubmissionFactory(conference=conference)
    SubmissionFactory(conference=conference, speaker_id=user.id)

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


def test_get_conference_voucher_with_invalid_code(graphql_client, requests_mock):
    conference = ConferenceFactory()

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


def test_get_conference_voucher_with_valid_until(
    graphql_client, requests_mock, settings
):
    conference = ConferenceFactory()

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


def test_get_conference_voucher(graphql_client, mocker, requests_mock, settings):
    conference = ConferenceFactory()
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


def test_filter_submission_by_status(graphql_client, user, requests_mock, settings):
    conference = ConferenceFactory()
    requests_mock.post(
        f"{settings.PRETIX_API}organizers/{conference.pretix_organizer_id}/events/{conference.pretix_event_id}/tickets/attendee-has-ticket/",
        json={"user_has_admission_ticket": True},
    )

    SubmissionFactory(conference=conference, status="cancelled")
    SubmissionFactory(conference=conference, status="proposed")
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


def test_get_conference_proposal_tags(
    graphql_client,
):
    conference = ConferenceFactory(timezone=zoneinfo.ZoneInfo("America/Los_Angeles"))

    tag1 = SubmissionTagFactory(name="a")
    tag2 = SubmissionTagFactory(name="b")
    tag3 = SubmissionTagFactory(name="c")
    SubmissionTagFactory(name="d")
    SubmissionTagFactory(name="e")

    conference.proposal_tags.set([tag1, tag2, tag3])

    resp = graphql_client.query(
        """
        query($code: String!) {
            conference(code: $code) {
                proposalTags {
                    id
                    name
                }
            }
        }
        """,
        variables={"code": conference.code},
    )

    assert len(resp["data"]["conference"]["proposalTags"]) == 3

    assert {
        "name": tag1.name,
        "id": str(tag1.id),
    } in resp["data"]["conference"]["proposalTags"]

    assert {
        "name": tag2.name,
        "id": str(tag2.id),
    } in resp["data"]["conference"]["proposalTags"]

    assert {
        "name": tag3.name,
        "id": str(tag3.id),
    } in resp["data"]["conference"]["proposalTags"]
