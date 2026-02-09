import json

import pytest
from django.contrib.admin import AdminSite
from django.core.exceptions import PermissionDenied

from conferences.tests.factories import ConferenceFactory
from reviews.admin import ReviewSessionAdmin
from reviews.models import ReviewSession
from reviews.tests.factories import (
    AvailableScoreOptionFactory,
    ReviewSessionFactory,
)
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def _create_recap_setup(*, session_status=ReviewSession.Status.COMPLETED):
    """Create a review session with accepted submissions for recap tests."""
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
        status=session_status,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    submission_1 = SubmissionFactory(
        conference=conference, status=Submission.STATUS.accepted
    )
    submission_2 = SubmissionFactory(
        conference=conference, status=Submission.STATUS.accepted
    )

    return user, conference, review_session, [submission_1, submission_2]


# --- review_recap_view tests ---


def test_recap_view_returns_correct_context(rf):
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
        status=ReviewSession.Status.COMPLETED,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)

    speaker_1 = UserFactory(gender="female")
    speaker_2 = UserFactory(gender="male")

    sub1 = SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.accepted,
        speaker=speaker_1,
        speaker_level="new",
    )
    sub2 = SubmissionFactory(
        conference=conference,
        status=Submission.STATUS.accepted,
        speaker=speaker_2,
        speaker_level="experienced",
        type=sub1.type,  # same type so they group together
    )
    conference.submission_types.add(sub1.type)

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_recap_view(request, review_session.id)

    assert response.status_code == 200

    ctx = response.context_data
    assert ctx["total_accepted"] == 2
    assert ctx["review_session_id"] == review_session.id
    assert ctx["review_session_repr"] == str(review_session)
    assert ctx["compute_analysis_url"] == (
        f"/admin/reviews/reviewsession/{review_session.id}/review/recap/compute-analysis/"
    )

    # submissions_data should contain both submissions with actual values
    submissions_by_id = {s["id"]: s for s in ctx["submissions_data"]}
    assert set(submissions_by_id.keys()) == {sub1.id, sub2.id}
    assert submissions_by_id[sub1.id]["title"] == str(sub1.title)
    assert submissions_by_id[sub1.id]["type"] == sub1.type.name
    assert submissions_by_id[sub1.id]["speaker"] == speaker_1.display_name
    assert submissions_by_id[sub2.id]["speaker"] == speaker_2.display_name

    # stats_by_type should have actual counts
    type_name = sub1.type.name
    assert type_name in ctx["stats_by_type"]
    stats = ctx["stats_by_type"][type_name]
    assert stats["total"] == 2
    assert stats["gender_counts"]["female"] == (1, 50.0)
    assert stats["gender_counts"]["male"] == (1, 50.0)
    assert stats["speaker_level_counts"]["new"] == (1, 50.0)
    assert stats["speaker_level_counts"]["experienced"] == (1, 50.0)


def test_recap_view_does_not_call_ml_functions(rf, mocker):
    mock_similar = mocker.patch("reviews.similar_talks.compute_similar_talks")
    mock_clusters = mocker.patch("reviews.similar_talks.compute_topic_clusters")

    user, conference, review_session, submissions = _create_recap_setup()

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    admin.review_recap_view(request, review_session.id)

    mock_similar.assert_not_called()
    mock_clusters.assert_not_called()


def test_recap_view_only_counts_accepted_submissions(rf):
    user, conference, review_session, submissions = _create_recap_setup()

    # Add a rejected submission - should not be counted
    SubmissionFactory(conference=conference, status=Submission.STATUS.rejected)

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_recap_view(request, review_session.id)

    assert response.context_data["total_accepted"] == 2


def test_recap_view_permission_denied_for_non_reviewer(rf):
    user = UserFactory(is_staff=True, is_superuser=False)
    conference = ConferenceFactory()
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
    )

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())

    with pytest.raises(PermissionDenied):
        admin.review_recap_view(request, review_session.id)


def test_recap_view_redirects_when_shortlist_not_visible(rf, mocker):
    mocker.patch("reviews.admin.messages")

    user, conference, review_session, submissions = _create_recap_setup(
        session_status=ReviewSession.Status.DRAFT,
    )

    # Grants sessions need COMPLETED to see shortlist; DRAFT won't work
    review_session.session_type = ReviewSession.SessionType.GRANTS
    review_session.save()

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_recap_view(request, review_session.id)

    assert response.status_code == 302
    assert (
        response.url
        == f"/admin/reviews/reviewsession/{review_session.id}/change/"
    )


# --- review_recap_compute_analysis_view tests ---


def _mock_analysis_deps(mocker, cache_return=None):
    """Mock the lazy-imported dependencies used in the compute analysis view."""
    mock_cache = mocker.patch("django.core.cache.cache.get", return_value=cache_return)
    mock_task = mocker.patch("reviews.tasks.compute_recap_analysis.apply_async")
    mock_check = mocker.patch("pycon.tasks.check_pending_heavy_processing_work.delay")
    mocker.patch(
        "reviews.similar_talks._get_cache_key",
        return_value="recap_analysis:conf_test:abc123",
    )
    return mock_cache, mock_task, mock_check


def test_compute_analysis_view_returns_cached_result(rf, mocker):
    user, conference, review_session, submissions = _create_recap_setup()
    sub1, sub2 = submissions

    cached_data = {
        "submissions_list": [
            {
                "id": sub1.id,
                "title": str(sub1.title),
                "type": sub1.type.name,
                "speaker": sub1.speaker.display_name,
                "similar": [
                    {"id": sub2.id, "title": str(sub2.title), "similarity": 75.0}
                ],
            },
            {
                "id": sub2.id,
                "title": str(sub2.title),
                "type": sub2.type.name,
                "speaker": sub2.speaker.display_name,
                "similar": [],
            },
        ],
        "topic_clusters": {
            "topics": [
                {"name": "ML", "count": 2, "keywords": ["ml"], "submissions": []}
            ],
            "outliers": [],
            "submission_topics": {},
        },
    }

    mock_cache, mock_task, _ = _mock_analysis_deps(mocker, cache_return=cached_data)

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_recap_compute_analysis_view(request, review_session.id)

    assert response.status_code == 200
    data = json.loads(response.content)

    assert len(data["submissions_list"]) == 2
    assert data["submissions_list"][0]["id"] == sub1.id
    assert data["topic_clusters"]["topics"][0]["name"] == "ML"

    # Task should NOT have been dispatched since cache was hit
    mock_task.assert_not_called()


def test_compute_analysis_view_dispatches_task_on_cache_miss(rf, mocker):
    user, conference, review_session, submissions = _create_recap_setup()

    _, mock_task, mock_check = _mock_analysis_deps(mocker, cache_return=None)

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_recap_compute_analysis_view(request, review_session.id)

    assert response.status_code == 200
    data = json.loads(response.content)
    assert data == {"status": "processing"}

    mock_task.assert_called_once_with(
        args=[conference.id],
        kwargs={"force_recompute": False},
        queue="heavy_processing",
    )

    mock_check.assert_called_once()


def test_compute_analysis_view_dispatches_task_with_recompute(rf, mocker):
    user, conference, review_session, submissions = _create_recap_setup()

    _, mock_task, _ = _mock_analysis_deps(mocker, cache_return=None)

    request = rf.get("/?recompute=1")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_recap_compute_analysis_view(request, review_session.id)

    assert response.status_code == 200
    data = json.loads(response.content)
    assert data == {"status": "processing"}

    mock_task.assert_called_once()
    call_kwargs = mock_task.call_args
    assert call_kwargs[1]["kwargs"]["force_recompute"] is True


def test_compute_analysis_view_recompute_skips_cache(rf, mocker):
    user, conference, review_session, submissions = _create_recap_setup()

    cached_data = {"submissions_list": [], "topic_clusters": {"topics": []}}
    mock_cache, mock_task, _ = _mock_analysis_deps(mocker, cache_return=cached_data)

    request = rf.get("/?recompute=1")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_recap_compute_analysis_view(request, review_session.id)

    data = json.loads(response.content)
    assert data == {"status": "processing"}

    # Cache should NOT have been checked when recompute=1
    mock_cache.assert_not_called()
    mock_task.assert_called_once()


def test_compute_analysis_view_permission_denied_for_non_reviewer(rf):
    user = UserFactory(is_staff=True, is_superuser=False)
    conference = ConferenceFactory()
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
    )

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())

    with pytest.raises(PermissionDenied):
        admin.review_recap_compute_analysis_view(request, review_session.id)


def test_compute_analysis_view_permission_denied_when_shortlist_not_visible(rf):
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.GRANTS,
        status=ReviewSession.Status.DRAFT,
    )

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())

    with pytest.raises(PermissionDenied):
        admin.review_recap_compute_analysis_view(request, review_session.id)
