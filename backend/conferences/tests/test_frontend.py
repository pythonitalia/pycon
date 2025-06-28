from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory
from conferences.tests.factories import ConferenceFactory
from job_board.tests.factories import JobListingFactory
from schedule.tests.factories import ScheduleItemFactory
from conferences.frontend import get_paths, trigger_frontend_revalidate
from schedule.models import ScheduleItem


def test_get_paths_for_keynote():
    keynote = ScheduleItem(
        slug="keynote-1",
        type=ScheduleItem.TYPES.keynote,
    )

    assert get_paths(keynote) == [
        "/keynotes/keynote-1",
    ]


def test_get_paths_for_event():
    event = ScheduleItemFactory(
        slug="event-1",
        type=ScheduleItem.TYPES.submission,
    )

    assert get_paths(event) == [
        "/event/event-1",
    ]


def test_get_paths_for_job_listing():
    job_listing = JobListingFactory(
        id=1,
    )

    assert get_paths(job_listing) == [
        "/jobs/1",
        "/jobs/",
    ]


def test_get_paths_for_unknown_object():
    assert get_paths(object()) == []


def test_get_paths_for_accepted_submission_invalidates_schedule_items():
    submission = SubmissionFactory(
        status=Submission.STATUS.accepted,
    )

    schedule_item = ScheduleItemFactory(
        submission=submission,
        conference=submission.conference,
        type=ScheduleItem.TYPES.talk,
    )

    assert get_paths(submission) == [
        f"/event/{schedule_item.slug}",
    ]


def test_trigger_frontend_revalidate(mocker):
    mock_call = mocker.patch("conferences.frontend.execute_frontend_revalidate.delay")

    conference = ConferenceFactory(
        frontend_revalidate_url="https://example.com",
        frontend_revalidate_secret="secret",
    )

    object = ScheduleItemFactory(
        slug="event-1",
        type=ScheduleItem.TYPES.submission,
    )

    trigger_frontend_revalidate(conference, object)

    mock_call.assert_has_calls(
        [
            mocker.call(
                url="https://example.com",
                path="/en/event/event-1",
                secret="secret",
            ),
            mocker.call(
                url="https://example.com",
                path="/it/event/event-1",
                secret="secret",
            ),
        ],
        any_order=True,
    )
