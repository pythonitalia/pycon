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


def test_compute_analysis_view_returns_submissions_and_clusters(rf, mocker):
    user, conference, review_session, submissions = _create_recap_setup()
    sub1, sub2 = submissions

    mocker.patch(
        "reviews.similar_talks.compute_similar_talks",
        return_value={
            sub1.id: [{"id": sub2.id, "title": str(sub2.title), "similarity": 75.0}],
            sub2.id: [],
        },
    )
    mocker.patch(
        "reviews.similar_talks.compute_topic_clusters",
        return_value={
            "topics": [{"name": "ML", "count": 2, "keywords": ["ml"], "submissions": []}],
            "outliers": [],
            "submission_topics": {},
        },
    )

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_recap_compute_analysis_view(request, review_session.id)

    assert response.status_code == 200
    data = json.loads(response.content)

    # Verify submissions_list structure
    assert len(data["submissions_list"]) == 2
    # sub1 has higher similarity (75%) so should be first
    assert data["submissions_list"][0]["id"] == sub1.id
    assert data["submissions_list"][0]["similar"] == [
        {"id": sub2.id, "title": str(sub2.title), "similarity": 75.0}
    ]
    assert data["submissions_list"][1]["id"] == sub2.id
    assert data["submissions_list"][1]["similar"] == []

    # Each submission entry has required fields
    for entry in data["submissions_list"]:
        assert "id" in entry
        assert "title" in entry
        assert "type" in entry
        assert "speaker" in entry
        assert "similar" in entry

    # Verify topic_clusters is passed through
    assert data["topic_clusters"]["topics"][0]["name"] == "ML"
    assert data["topic_clusters"]["outliers"] == []


def test_compute_analysis_view_passes_recompute_flag(rf, mocker):
    mock_similar = mocker.patch(
        "reviews.similar_talks.compute_similar_talks",
        return_value={},
    )
    mock_clusters = mocker.patch(
        "reviews.similar_talks.compute_topic_clusters",
        return_value={"topics": [], "outliers": [], "submission_topics": {}},
    )

    user, conference, review_session, submissions = _create_recap_setup()

    request = rf.get("/?recompute=1")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    admin.review_recap_compute_analysis_view(request, review_session.id)

    _, kwargs = mock_similar.call_args
    assert kwargs["force_recompute"] is True

    _, kwargs = mock_clusters.call_args
    assert kwargs["force_recompute"] is True


def test_compute_analysis_view_no_recompute_by_default(rf, mocker):
    mock_similar = mocker.patch(
        "reviews.similar_talks.compute_similar_talks",
        return_value={},
    )
    mock_clusters = mocker.patch(
        "reviews.similar_talks.compute_topic_clusters",
        return_value={"topics": [], "outliers": [], "submission_topics": {}},
    )

    user, conference, review_session, submissions = _create_recap_setup()

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    admin.review_recap_compute_analysis_view(request, review_session.id)

    _, kwargs = mock_similar.call_args
    assert kwargs["force_recompute"] is False

    _, kwargs = mock_clusters.call_args
    assert kwargs["force_recompute"] is False


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
