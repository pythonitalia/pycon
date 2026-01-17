from decimal import Decimal

import pytest
from django.contrib.admin import AdminSite

from conferences.tests.factories import ConferenceFactory
from grants.models import Grant
from grants.tests.factories import (
    GrantFactory,
    GrantReimbursementCategoryFactory,
    GrantReimbursementFactory,
)
from reviews.admin import ReviewSessionAdmin, get_next_to_review_item_id
from reviews.models import ReviewSession
from reviews.tests.factories import (
    AvailableScoreOptionFactory,
    ReviewSessionFactory,
    UserReviewFactory,
)
from submissions.tests.factories import SubmissionFactory, SubmissionTagFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_next_item_to_review_prefers_items_with_fewer_votes():
    tag = SubmissionTagFactory()

    user_1 = UserFactory(is_staff=True, is_superuser=True)
    user_2 = UserFactory(is_staff=True, is_superuser=True)

    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
    )
    score_0 = AvailableScoreOptionFactory(
        review_session=review_session, numeric_value=0
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    submission_1 = SubmissionFactory(conference=conference)
    submission_1.tags.add(tag)
    submission_2 = SubmissionFactory(conference=conference)
    submission_2.tags.add(tag)

    UserReviewFactory(
        review_session=review_session,
        proposal=submission_1,
        user=user_1,
        score=score_0,
    )

    next_to_review = get_next_to_review_item_id(review_session, user_2)
    assert next_to_review == submission_2.id


@pytest.mark.parametrize("iteration", range(10))
def test_next_item_to_review_for_submissions_ignores_excluded_tags(iteration):
    tag_1 = SubmissionTagFactory(name="A")
    tag_2 = SubmissionTagFactory(name="B")
    tag_3 = SubmissionTagFactory(name="C")

    user_1 = UserFactory(is_staff=True, is_superuser=True)

    conference = ConferenceFactory()
    conference_2 = ConferenceFactory()

    SubmissionFactory(conference=conference_2)
    SubmissionFactory(conference=conference_2)
    SubmissionFactory(conference=conference_2)

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    submission_1 = SubmissionFactory(conference=conference)
    submission_1.tags.add(tag_1)
    submission_1.tags.add(tag_3)

    submission_2 = SubmissionFactory(conference=conference)
    submission_2.tags.add(tag_1)
    submission_2.tags.add(tag_2)
    submission_2.tags.add(tag_3)

    next_to_review = get_next_to_review_item_id(
        review_session, user_1, exclude=[tag_2.id]
    )
    assert next_to_review == submission_1.id


@pytest.mark.parametrize(
    "scores, avg",
    [
        (
            [
                {"user": 0, "score": 2},
                {"user": 1, "score": 2},
                {"user": 2, "score": 2},
                {"user": 3, "score": -1},
                {"user": 4, "score": -2},
            ],
            0.6,
        ),
        (
            [
                {"user": 0, "score": -2},
                {"user": 1, "score": -2},
                {"user": 2, "score": -2},
                {"user": 3, "score": -2},
                {"user": 4, "score": -2},
            ],
            -2.0,
        ),
        (
            [
                {"user": 0, "score": 1},
            ],
            1.0,
        ),
        ([], None),
    ],
)
def test_grants_review_scores(rf, scores, avg):
    conference = ConferenceFactory()
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.GRANTS,
        status=ReviewSession.Status.COMPLETED,
    )

    users = UserFactory.create_batch(10, is_staff=True, is_superuser=True)
    all_scores = {
        -2: AvailableScoreOptionFactory(
            review_session=review_session, numeric_value=-2, label="Rejected"
        ),
        -1: AvailableScoreOptionFactory(
            review_session=review_session, numeric_value=-1, label="Not convinced"
        ),
        0: AvailableScoreOptionFactory(
            review_session=review_session, numeric_value=0, label="Maybe"
        ),
        1: AvailableScoreOptionFactory(
            review_session=review_session, numeric_value=1, label="Yes"
        ),
        2: AvailableScoreOptionFactory(
            review_session=review_session, numeric_value=2, label="Absolutely"
        ),
    }

    grant_1 = GrantFactory(conference=conference)
    for score in scores:
        UserReviewFactory(
            review_session=review_session,
            grant=grant_1,
            user=users[score["user"]],
            score=all_scores[score["score"]],
        )

    grant_2 = GrantFactory(conference=conference)

    UserReviewFactory(
        review_session=review_session,
        grant=grant_2,
        user=users[9],
        score=all_scores[-2],
    )

    UserReviewFactory(
        review_session=review_session,
        grant=grant_2,
        user=users[8],
        score=all_scores[-1],
    )

    request = rf.get("/")
    request.user = users[5]

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin._review_grants_recap_view(request, review_session)
    context_data = response.context_data
    items = context_data["items"]
    grant_to_check = next(item for item in items if item.id == grant_1.id)

    assert grant_to_check.id == grant_1.id
    assert grant_to_check.score == avg


def test_review_start_view_when_no_items_are_left(rf, mocker):
    mock_messages = mocker.patch("reviews.admin.messages")

    tag = SubmissionTagFactory()
    user = UserFactory(is_staff=True, is_superuser=True)

    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
    )
    score = AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    submission_1 = SubmissionFactory(conference=conference)
    submission_1.tags.add(tag)
    submission_2 = SubmissionFactory(conference=conference)
    submission_2.tags.add(tag)

    UserReviewFactory(
        review_session=review_session,
        proposal=submission_1,
        user=user,
        score=score,
    )

    UserReviewFactory(
        review_session=review_session,
        proposal=submission_2,
        user=user,
        score=score,
    )

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_start_view(request, review_session.id)

    assert response.status_code == 302
    assert (
        response.url
        == f"/admin/reviews/reviewsession/{review_session.id}/review/recap/"
    )
    mock_messages.warning.assert_called_once_with(request, "No new proposal to review.")


def test_review_start_view(rf, mocker):
    mocker.patch("reviews.admin.messages")

    tag = SubmissionTagFactory()
    user = UserFactory(is_staff=True, is_superuser=True)

    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
    )
    score = AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    submission_1 = SubmissionFactory(conference=conference)
    submission_1.tags.add(tag)
    submission_2 = SubmissionFactory(conference=conference)
    submission_2.tags.add(tag)

    UserReviewFactory(
        review_session=review_session,
        proposal=submission_2,
        user=user,
        score=score,
    )

    request = rf.get("/")
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin.review_start_view(request, review_session.id)

    assert response.status_code == 302
    assert (
        response.url
        == f"/admin/reviews/reviewsession/{review_session.id}/review/{submission_1.id}/"
    )


def test_save_review_grants_updates_grant_and_creates_reimbursements(rf, mocker):
    mock_messages = mocker.patch("reviews.admin.messages")

    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    # Create reimbursement categories
    travel_category = GrantReimbursementCategoryFactory(
        conference=conference,
        travel=True,
        max_amount=Decimal("500"),
    )
    ticket_category = GrantReimbursementCategoryFactory(
        conference=conference,
        ticket=True,
        max_amount=Decimal("100"),
    )
    accommodation_category = GrantReimbursementCategoryFactory(
        conference=conference,
        accommodation=True,
        max_amount=Decimal("200"),
    )

    # Create review session for grants
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.GRANTS,
        status=ReviewSession.Status.COMPLETED,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    # Create grants with initial status
    grant_1 = GrantFactory(conference=conference, status=Grant.Status.pending)
    grant_2 = GrantFactory(conference=conference, status=Grant.Status.pending)

    # Build POST data
    # Note: The current admin code uses data.items() which only keeps the last value
    # when multiple checkboxes have the same name. For multiple categories, the code
    # would need to use request.POST.getlist(). Testing with one category per grant.
    post_data = {
        f"decision-{grant_1.id}": Grant.Status.approved,
        f"reimbursementcategory-{grant_1.id}": [
            str(ticket_category.id),
            str(travel_category.id),
        ],
        f"decision-{grant_2.id}": Grant.Status.approved,
        f"reimbursementcategory-{grant_2.id}": [
            str(ticket_category.id),
            str(travel_category.id),
            str(accommodation_category.id),
        ],
    }

    request = rf.post("/", data=post_data)
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin._review_grants_recap_view(request, review_session)

    # Should redirect after successful save
    assert response.status_code == 302
    assert (
        response.url
        == f"/admin/reviews/reviewsession/{review_session.id}/review/recap/"
    )

    # Refresh grants from database
    grant_1.refresh_from_db()
    grant_2.refresh_from_db()

    # Verify grants were updated with pending_status
    assert grant_1.pending_status == Grant.Status.approved
    assert grant_2.pending_status == Grant.Status.approved

    # Verify GrantReimbursement objects were created
    assert grant_1.reimbursements.count() == 2
    assert {
        reimbursement.category for reimbursement in grant_1.reimbursements.all()
    } == {ticket_category, travel_category}

    assert grant_2.reimbursements.count() == 3
    assert {
        reimbursement.category for reimbursement in grant_2.reimbursements.all()
    } == {ticket_category, travel_category, accommodation_category}

    mock_messages.success.assert_called_once()


def test_save_review_grants_update_grants_status_to_rejected_removes_reimbursements(
    rf, mocker
):
    mock_messages = mocker.patch("reviews.admin.messages")

    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    # Create reimbursement categories
    travel_category = GrantReimbursementCategoryFactory(
        conference=conference,
        travel=True,
        max_amount=Decimal("500"),
    )
    ticket_category = GrantReimbursementCategoryFactory(
        conference=conference,
        ticket=True,
        max_amount=Decimal("100"),
    )
    accommodation_category = GrantReimbursementCategoryFactory(
        conference=conference,
        accommodation=True,
        max_amount=Decimal("200"),
    )

    # Create review session for grants
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.GRANTS,
        status=ReviewSession.Status.COMPLETED,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    # Create grants with initial status
    grant_1 = GrantFactory(conference=conference, status=Grant.Status.approved)
    GrantReimbursementFactory(
        grant=grant_1,
        category=travel_category,
        granted_amount=Decimal("500"),
    )
    GrantReimbursementFactory(
        grant=grant_1,
        category=ticket_category,
        granted_amount=Decimal("100"),
    )
    GrantReimbursementFactory(
        grant=grant_1,
        category=accommodation_category,
        granted_amount=Decimal("200"),
    )

    # Build POST data
    post_data = {
        f"decision-{grant_1.id}": Grant.Status.rejected,
        f"reimbursementcategory-{grant_1.id}": [],
    }

    request = rf.post("/", data=post_data)
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin._review_grants_recap_view(request, review_session)

    # Should redirect after successful save
    assert response.status_code == 302
    assert (
        response.url
        == f"/admin/reviews/reviewsession/{review_session.id}/review/recap/"
    )
    grant_1.refresh_from_db()

    assert grant_1.pending_status == Grant.Status.rejected

    assert grant_1.reimbursements.count() == 0


def test_save_review_grants_modify_reimbursements(rf, mocker):
    mock_messages = mocker.patch("reviews.admin.messages")

    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    # Create reimbursement categories
    travel_category = GrantReimbursementCategoryFactory(
        conference=conference,
        travel=True,
        max_amount=Decimal("500"),
    )
    ticket_category = GrantReimbursementCategoryFactory(
        conference=conference,
        ticket=True,
        max_amount=Decimal("100"),
    )
    accommodation_category = GrantReimbursementCategoryFactory(
        conference=conference,
        accommodation=True,
        max_amount=Decimal("200"),
    )

    # Create review session for grants
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.GRANTS,
        status=ReviewSession.Status.COMPLETED,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    # Create grants with initial status
    grant_1 = GrantFactory(conference=conference, status=Grant.Status.approved)
    GrantReimbursementFactory(
        grant=grant_1,
        category=travel_category,
        granted_amount=Decimal("500"),
    )
    GrantReimbursementFactory(
        grant=grant_1,
        category=ticket_category,
        granted_amount=Decimal("100"),
    )
    GrantReimbursementFactory(
        grant=grant_1,
        category=accommodation_category,
        granted_amount=Decimal("200"),
    )

    # Removing the travel and accommodation reimbursements
    post_data = {
        f"decision-{grant_1.id}": Grant.Status.approved,
        f"reimbursementcategory-{grant_1.id}": [str(ticket_category.id)],
    }

    request = rf.post("/", data=post_data)
    request.user = user

    admin = ReviewSessionAdmin(ReviewSession, AdminSite())
    response = admin._review_grants_recap_view(request, review_session)

    grant_1.refresh_from_db()

    assert grant_1.reimbursements.count() == 1
    assert {
        reimbursement.category for reimbursement in grant_1.reimbursements.all()
    } == {ticket_category}
