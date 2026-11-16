from decimal import Decimal
from typing import Literal

import pytest
from django.contrib.admin import AdminSite
from django.contrib.admin.models import LogEntry
from django.test import Client
from django.urls import reverse
from pytest_mock import MockerFixture

from conferences.tests.factories import ConferenceFactory
from grants.models import Grant
from grants.tests.factories import (
    GrantFactory,
    GrantReimbursementCategoryFactory,
    GrantReimbursementFactory,
)
from reviews.adapters import get_review_adapter
from reviews.admin import ReviewSessionAdmin
from reviews.models import AvailableScoreOption, ReviewSession, UserReview
from reviews.tests.factories import (
    AvailableScoreOptionFactory,
    ReviewSessionFactory,
    UserReviewFactory,
)
from submissions.models import Submission
from submissions.tests.factories import SubmissionFactory, SubmissionTagFactory
from users.models import User
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

    adapter = get_review_adapter(review_session)
    next_to_review = adapter.get_next_to_review_item_id(review_session, user_2)

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

    adapter = get_review_adapter(review_session)

    next_to_review = adapter.get_next_to_review_item_id(
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
        (
            [
                {"user": 0, "score": 2},
                {"user": 1, "score": None},
            ],
            2.0,
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
        None: None,
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

    adapter = get_review_adapter(review_session)
    items = adapter.get_shortlist_items_queryset(review_session).all()
    grant_to_check = next(item for item in items if item.id == grant_1.id)

    assert grant_to_check.id == grant_1.id
    assert grant_to_check.score == avg


@pytest.mark.parametrize(
    "scores, expected_std_dev",
    [
        # Multiple different scores: mean=0.6, std_dev ≈ 1.744
        (
            [
                {"user": 0, "score": 2},
                {"user": 1, "score": 2},
                {"user": 2, "score": 2},
                {"user": 3, "score": -1},
                {"user": 4, "score": -2},
            ],
            1.744,
        ),
        # All same scores: std_dev = 0
        (
            [
                {"user": 0, "score": -2},
                {"user": 1, "score": -2},
                {"user": 2, "score": -2},
                {"user": 3, "score": -2},
                {"user": 4, "score": -2},
            ],
            0.0,
        ),
        # Single score: std_dev = 0
        (
            [
                {"user": 0, "score": 1},
            ],
            0.0,
        ),
        # No scores: std_dev = None
        ([], None),
        # Two different scores (1 and -1): mean=0, std_dev = sqrt(((1-0)^2 + (-1-0)^2) / 2) = 1.0
        (
            [
                {"user": 0, "score": 1},
                {"user": 1, "score": -1},
            ],
            1.0,
        ),
        # Three scores with same value: std_dev = 0
        (
            [
                {"user": 0, "score": 1},
                {"user": 1, "score": 1},
                {"user": 2, "score": 1},
            ],
            0.0,
        ),
        # Mixed scores showing consensus with outlier: 3x score=1, 1x score=-2
        # mean = (1+1+1-2)/4 = 0.25
        # std_dev = sqrt(((1-0.25)^2 + (1-0.25)^2 + (1-0.25)^2 + (-2-0.25)^2) / 4)
        #         = sqrt((0.5625 + 0.5625 + 0.5625 + 5.0625) / 4) = sqrt(1.6875) ≈ 1.299
        (
            [
                {"user": 0, "score": 1},
                {"user": 1, "score": 1},
                {"user": 2, "score": 1},
                {"user": 3, "score": -2},
            ],
            1.299,
        ),
    ],
)
def test_grants_review_std_dev(rf, scores, expected_std_dev):
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

    grant = GrantFactory(conference=conference)
    for score in scores:
        UserReviewFactory(
            review_session=review_session,
            grant=grant,
            user=users[score["user"]],
            score=all_scores[score["score"]],
        )

    request = rf.get("/")
    request.user = users[5]

    adapter = get_review_adapter(review_session)
    items = adapter.get_shortlist_items_queryset(review_session).all()
    context_data = adapter.get_shortlist_context(
        request, review_session, items, AdminSite()
    )
    items = context_data["items"]
    grant_to_check = next(item for item in items if item.id == grant.id)

    assert grant_to_check.id == grant.id
    if expected_std_dev is None:
        assert grant_to_check.std_dev is None
    else:
        assert grant_to_check.std_dev == pytest.approx(expected_std_dev, abs=0.01)


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
        == f"/admin/reviews/reviewsession/{review_session.id}/review/shortlist/"
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


def test_save_review_grants_updates_grant_and_creates_reimbursements(rf):
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

    adapter = get_review_adapter(review_session)
    adapter.process_shortlist_post(request, review_session)

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

    # Verify log entries were created
    assert (
        LogEntry.objects.filter(object_id=grant_1.id).count() == 3
    )  # 1 pending_status change, 2 reimbursement additions
    assert (
        LogEntry.objects.filter(object_id=grant_2.id).count() == 4
    )  # 1 pending_status change, 3 reimbursement additions
    assert LogEntry.objects.filter(
        user=user,
        object_id__in=[str(grant_1.id), str(grant_2.id)],
        change_message="[Review Session] Pending status changed from 'None' to 'approved'.",
    ).exists()
    assert LogEntry.objects.filter(
        user=user,
        object_id__in=[str(grant_1.id), str(grant_2.id)],
        change_message=f"[Review Session] Reimbursement {ticket_category.name} added.",
    ).exists()
    assert LogEntry.objects.filter(
        user=user,
        object_id__in=[str(grant_1.id), str(grant_2.id)],
        change_message=f"[Review Session] Reimbursement {travel_category.name} added.",
    ).exists()
    assert LogEntry.objects.filter(
        user=user,
        object_id=str(grant_2.id),
        change_message=f"[Review Session] Reimbursement {accommodation_category.name} added.",
    ).exists()


def test_save_review_grants_update_grants_status_to_rejected_removes_reimbursements(rf):
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

    adapter = get_review_adapter(review_session)
    adapter.process_shortlist_post(request, review_session)

    grant_1.refresh_from_db()

    assert grant_1.pending_status == Grant.Status.rejected

    assert grant_1.reimbursements.count() == 0

    assert LogEntry.objects.count() == 4
    for reimbursement in grant_1.reimbursements.all():
        assert LogEntry.objects.filter(
            user=user,
            object_id=str(reimbursement.id),
            change_message=f"[Review Session] Reimbursement removed: {reimbursement.category.name}.",
        ).exists()


def test_save_review_grants_modify_reimbursements(rf):
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

    adapter = get_review_adapter(review_session)
    adapter.process_shortlist_post(request, review_session)

    grant_1.refresh_from_db()

    assert grant_1.reimbursements.count() == 1
    assert {
        reimbursement.category for reimbursement in grant_1.reimbursements.all()
    } == {ticket_category}

    # Verify log entries were created
    assert LogEntry.objects.count() == 2
    assert LogEntry.objects.filter(
        user=user,
        object_id=grant_1.id,
        change_message=f"[Review Session] Reimbursement removed: {travel_category.name}.",
    ).exists()
    assert LogEntry.objects.filter(
        user=user,
        object_id=grant_1.id,
        change_message=f"[Review Session] Reimbursement removed: {accommodation_category.name}.",
    ).exists()

    # pending_status change should not be logged because the grant status is not changed
    assert not LogEntry.objects.filter(
        user=user,
        object_id=grant_1.id,
        change_message="[Review Session] Pending status changed from 'approved' to 'None'.",
    ).exists()


def test_save_review_grants_waiting_list_does_not_create_reimbursements(rf):
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

    grant_1 = GrantFactory(conference=conference, status=Grant.Status.pending)
    grant_2 = GrantFactory(conference=conference, status=Grant.Status.pending)

    post_data = {
        f"decision-{grant_1.id}": Grant.Status.waiting_list,
        f"reimbursementcategory-{grant_1.id}": [
            str(ticket_category.id),
            str(travel_category.id),
        ],
        f"decision-{grant_2.id}": Grant.Status.waiting_list_maybe,
        f"reimbursementcategory-{grant_2.id}": [
            str(ticket_category.id),
            str(travel_category.id),
            str(accommodation_category.id),
        ],
    }

    request = rf.post("/", data=post_data)
    request.user = user

    adapter = get_review_adapter(review_session)
    adapter.process_shortlist_post(request, review_session)

    # Refresh grants from database
    grant_1.refresh_from_db()
    grant_2.refresh_from_db()

    # Verify grants were updated with pending_status
    assert grant_1.pending_status == Grant.Status.waiting_list
    assert grant_2.pending_status == Grant.Status.waiting_list_maybe

    # Verify GrantReimbursement objects were created
    assert grant_1.reimbursements.count() == 0
    assert grant_2.reimbursements.count() == 0

    # Verify log entries were created
    assert (
        LogEntry.objects.filter(object_id=grant_1.id).count() == 1
    )  # 1 pending_status change
    assert (
        LogEntry.objects.filter(object_id=grant_2.id).count() == 1
    )  # 1 pending_status change


def test_save_review_grants_two_times_does_not_create_duplicate_log_entries(rf):
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

    grant_1 = GrantFactory(conference=conference, status=Grant.Status.pending)
    post_data = {
        f"decision-{grant_1.id}": Grant.Status.approved,
        f"reimbursementcategory-{grant_1.id}": [
            str(ticket_category.id),
            str(travel_category.id),
            str(accommodation_category.id),
        ],
    }
    request = rf.post("/", data=post_data)
    request.user = user

    adapter = get_review_adapter(review_session)
    adapter.process_shortlist_post(request, review_session)  # First save
    adapter.process_shortlist_post(request, review_session)  # Second save

    grant_1.refresh_from_db()

    assert grant_1.reimbursements.count() == 3
    assert {
        reimbursement.category for reimbursement in grant_1.reimbursements.all()
    } == {ticket_category, travel_category, accommodation_category}

    assert LogEntry.objects.count() == 4
    assert LogEntry.objects.filter(
        user=user,
        object_id=grant_1.id,
        change_message="[Review Session] Pending status changed from 'None' to 'approved'.",
    ).exists()


# --- ProposalsReviewAdapter Tests ---


def test_proposals_review_get_shortlist_context(rf):
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
        status=ReviewSession.Status.COMPLETED,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    submission = SubmissionFactory(conference=conference)
    GrantFactory(conference=conference, user=submission.speaker)

    request = rf.get("/")
    request.user = user

    adapter = get_review_adapter(review_session)
    items = adapter.get_shortlist_items_queryset(review_session).all()
    context = adapter.get_shortlist_context(request, review_session, items, AdminSite())

    assert "items" in context
    assert "grants" in context
    assert "review_session_id" in context
    assert "audience_levels" in context
    assert "all_statuses" in context
    assert "speaker_submission_counts" in context
    assert context["review_session_id"] == review_session.id
    assert str(submission.speaker_id) in context["grants"]
    # Verify speaker submission count is tracked
    assert str(submission.speaker_id) in context["speaker_submission_counts"]
    assert context["speaker_submission_counts"][str(submission.speaker_id)] == 1


def test_proposals_review_get_shortlist_context_with_multiple_submissions_per_speaker(
    rf,
):
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
        status=ReviewSession.Status.COMPLETED,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    # Create a speaker with multiple submissions
    speaker = UserFactory()
    SubmissionFactory(conference=conference, speaker=speaker)
    SubmissionFactory(conference=conference, speaker=speaker)
    SubmissionFactory(conference=conference, speaker=speaker)

    # Create another speaker with only one submission
    single_speaker = UserFactory()
    SubmissionFactory(conference=conference, speaker=single_speaker)

    request = rf.get("/")
    request.user = user

    adapter = get_review_adapter(review_session)
    items = adapter.get_shortlist_items_queryset(review_session).all()
    context = adapter.get_shortlist_context(request, review_session, items, AdminSite())

    assert "speaker_submission_counts" in context
    # Speaker with 3 submissions should have count of 3
    assert context["speaker_submission_counts"][str(speaker.id)] == 3
    # Speaker with 1 submission should have count of 1
    assert context["speaker_submission_counts"][str(single_speaker.id)] == 1


def test_proposals_review_process_shortlist_post(rf):
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
        status=ReviewSession.Status.COMPLETED,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    submission_1 = SubmissionFactory(conference=conference)
    submission_2 = SubmissionFactory(conference=conference)

    post_data = {
        f"decision-{submission_1.id}": "accepted",
        f"decision-{submission_2.id}": "rejected",
    }

    request = rf.post("/", data=post_data)
    request.user = user

    adapter = get_review_adapter(review_session)
    adapter.process_shortlist_post(request, review_session)

    submission_1.refresh_from_db()
    submission_2.refresh_from_db()

    assert submission_1.pending_status == "accepted"
    assert submission_2.pending_status == "rejected"


def test_proposals_review_get_review_context(rf):
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
        status=ReviewSession.Status.REVIEWING,
    )
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=0)
    AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)

    tag = SubmissionTagFactory()
    submission = SubmissionFactory(conference=conference)
    submission.tags.add(tag)

    request = rf.get("/")
    request.user = user

    adapter = get_review_adapter(review_session)
    context = adapter.get_review_context(
        request, review_session, submission.id, None, AdminSite()
    )

    assert "proposal" in context
    assert "languages" in context
    assert "available_scores" in context
    assert "speaker" in context
    assert "tags_to_filter" in context
    assert context["proposal"].id == submission.id
    assert context["proposal_id"] == submission.id
    assert context["review_session_id"] == review_session.id


# --- GrantsReviewAdapter Tests ---


def test_grants_review_get_shortlist_context_includes_country_type_choices(rf):
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.GRANTS,
        status=ReviewSession.Status.COMPLETED,
    )

    request = rf.get("/")
    request.user = user

    adapter = get_review_adapter(review_session)
    items = adapter.get_shortlist_items_queryset(review_session).all()
    context = adapter.get_shortlist_context(request, review_session, items, AdminSite())

    assert "country_type_choices" in context
    values = [ct[0] for ct in context["country_type_choices"]]
    assert Grant.CountryType.italy in values
    assert Grant.CountryType.europe in values
    assert Grant.CountryType.extra_eu in values
    # Sentinel for grants with no departure_country (country_type is null)
    assert "" in values


def test_grants_review_get_shortlist_context_grant_with_no_departure_country(rf):
    """Grant with departure_country=None has country_type=None, which must map
    to the empty-string sentinel in country_type_choices so the template filter
    value='""' matches data-country-type=""."""
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.GRANTS,
        status=ReviewSession.Status.COMPLETED,
    )
    grant = GrantFactory(
        conference=conference,
        departure_country=None,
        departure_city=None,
    )

    request = rf.get("/")
    request.user = user

    adapter = get_review_adapter(review_session)
    items = adapter.get_shortlist_items_queryset(review_session).all()
    context = adapter.get_shortlist_context(request, review_session, items, AdminSite())

    grant_item = next(item for item in context["items"] if item.id == grant.id)
    assert grant_item.country_type is None

    # The template renders {{ item.country_type|default:'' }} which produces "".
    # Confirm the Unknown sentinel in the choices list uses the same empty string.
    sentinel_values = [
        ct[0] for ct in context["country_type_choices"] if ct[1] == "Unknown"
    ]
    assert sentinel_values == [""]


def test_grants_review_get_shortlist_context_needs_funds_for_travel(rf):
    """needs_funds_for_travel is rendered via |yesno:'true,false' in the template.
    Verify the queryset correctly exposes the boolean so the template filter
    can produce the 'true'/'false' strings matched by the JS checkboxes."""
    user = UserFactory(is_staff=True, is_superuser=True)
    conference = ConferenceFactory()

    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.GRANTS,
        status=ReviewSession.Status.COMPLETED,
    )
    grant_needs_funds = GrantFactory(conference=conference, needs_funds_for_travel=True)
    grant_no_funds = GrantFactory(conference=conference, needs_funds_for_travel=False)

    request = rf.get("/")
    request.user = user

    adapter = get_review_adapter(review_session)
    items = adapter.get_shortlist_items_queryset(review_session).all()
    context = adapter.get_shortlist_context(request, review_session, items, AdminSite())

    items_by_id = {item.id: item for item in context["items"]}
    assert items_by_id[grant_needs_funds.id].needs_funds_for_travel is True
    assert items_by_id[grant_no_funds.id].needs_funds_for_travel is False


@pytest.fixture(
    params=[ReviewSession.SessionType.PROPOSALS, ReviewSession.SessionType.GRANTS],
    ids=["proposals", "grants"],
)
def review_session(request: pytest.FixtureRequest) -> ReviewSession:
    return ReviewSessionFactory(
        session_type=request.param, status=ReviewSession.Status.REVIEWING
    )


@pytest.fixture
def stub_astro_admin_base(mocker: MockerFixture) -> None:
    mocker.patch(
        "custom_admin.template_backends.AstroContentLoader.get_contents",
        return_value="{% block content %}{% endblock %}",
    )


def _make_proposal_or_grant(review_session: ReviewSession) -> Submission | Grant:
    if review_session.is_proposals_review:
        return SubmissionFactory(conference=review_session.conference)

    return GrantFactory(conference=review_session.conference)


def _make_review(
    review_session: ReviewSession,
    item: Submission | Grant,
    *,
    score: AvailableScoreOption | None,
    user: User | None = None,
    comment: str = "",
) -> UserReview:
    item_field = "proposal" if review_session.is_proposals_review else "grant"
    return UserReviewFactory(
        review_session=review_session,
        user=user or UserFactory(),
        score=score,
        comment=comment,
        **{item_field: item},
    )


def _vote_url(review_session: ReviewSession, item: Submission | Grant) -> str:
    return reverse(
        "admin:reviews-vote-view",
        kwargs={"review_session_id": review_session.id, "review_item_id": item.id},
    )


def _shortlist_url(review_session: ReviewSession) -> str:
    return reverse(
        "admin:reviews-shortlist", kwargs={"review_session_id": review_session.id}
    )


def test_abstain_saves_empty_score_and_comment_and_item_does_not_come_back(
    client: Client, admin_superuser: User, review_session: ReviewSession
) -> None:
    client.force_login(admin_superuser)
    score = AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)
    item = _make_proposal_or_grant(review_session)

    client.post(
        _vote_url(review_session, item),
        {"_abstain": "Abstain", "score": score.id, "comment": "I know them"},
    )

    review = UserReview.objects.get(review_session=review_session)
    assert review.user == admin_superuser
    assert review.score is None
    assert review.comment == "I know them"
    adapter = get_review_adapter(review_session)
    assert adapter.get_next_to_review_item_id(review_session, admin_superuser) is None


def test_vote_without_score_saves_nothing_and_vote_with_score_replaces_abstention(
    client: Client, admin_superuser: User, review_session: ReviewSession
) -> None:
    client.force_login(admin_superuser)
    score = AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)
    unvoted_item = _make_proposal_or_grant(review_session)
    abstained_item = _make_proposal_or_grant(review_session)
    review = _make_review(
        review_session, abstained_item, score=None, user=admin_superuser
    )

    client.post(_vote_url(review_session, unvoted_item), {"_next": "Vote"})
    client.post(
        _vote_url(review_session, abstained_item), {"_next": "Vote", "score": score.id}
    )

    assert list(UserReview.objects.filter(review_session=review_session)) == [review]
    review.refresh_from_db()
    assert review.score == score


def test_next_item_to_review_does_not_count_abstentions(
    review_session: ReviewSession,
) -> None:
    score = AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)
    item_with_abstentions = _make_proposal_or_grant(review_session)
    item_with_score = _make_proposal_or_grant(review_session)
    _make_review(review_session, item_with_abstentions, score=None)
    _make_review(review_session, item_with_abstentions, score=None)
    _make_review(review_session, item_with_score, score=score)

    adapter = get_review_adapter(review_session)
    next_item_id = adapter.get_next_to_review_item_id(review_session, UserFactory())
    assert next_item_id == item_with_abstentions.id


@pytest.mark.parametrize(
    "session_type, status, page, expected_count",
    [
        pytest.param(
            ReviewSession.SessionType.PROPOSALS,
            ReviewSession.Status.REVIEWING,
            "vote",
            "Total votes: 1",
            id="proposals-vote-page",
        ),
        pytest.param(
            ReviewSession.SessionType.PROPOSALS,
            ReviewSession.Status.REVIEWING,
            "shortlist",
            "numOfVotes: 1,",
            id="proposals-shortlist",
        ),
        pytest.param(
            ReviewSession.SessionType.GRANTS,
            ReviewSession.Status.COMPLETED,
            "shortlist",
            "numOfVotes: 1,",
            id="grants-shortlist",
        ),
    ],
)
@pytest.mark.usefixtures("stub_astro_admin_base")
def test_review_pages_show_abstained_and_count_scored_votes_only(
    client: Client,
    admin_superuser: User,
    session_type: ReviewSession.SessionType,
    status: ReviewSession.Status,
    page: Literal["vote", "shortlist"],
    expected_count: str,
) -> None:
    client.force_login(admin_superuser)
    review_session = ReviewSessionFactory(session_type=session_type, status=status)
    score = AvailableScoreOptionFactory(
        review_session=review_session, numeric_value=2, label="Absolutely"
    )
    item = _make_proposal_or_grant(review_session)
    _make_review(
        review_session,
        item,
        score=score,
        user=UserFactory(full_name="Scoring Reviewer"),
    )
    _make_review(
        review_session,
        item,
        score=None,
        user=UserFactory(full_name="Passing Reviewer"),
        comment="I know them",
    )

    url = (
        _vote_url(review_session, item)
        if page == "vote"
        else _shortlist_url(review_session)
    )
    response = client.get(url)

    content = " ".join(response.content.decode().split())
    assert expected_count in content
    assert "<strong>Passing Reviewer</strong> Abstained <br /> I know them" in content
    assert "<strong>Scoring Reviewer</strong> voted Absolutely (2)" in content


@pytest.mark.usefixtures("stub_astro_admin_base")
def test_review_page_tells_me_i_abstained(
    client: Client, admin_superuser: User, review_session: ReviewSession
) -> None:
    client.force_login(admin_superuser)
    score = AvailableScoreOptionFactory(review_session=review_session, numeric_value=1)
    abstained_item = _make_proposal_or_grant(review_session)
    scored_item = _make_proposal_or_grant(review_session)
    unreviewed_item = _make_proposal_or_grant(review_session)
    _make_review(review_session, abstained_item, score=None, user=admin_superuser)
    _make_review(review_session, scored_item, score=score, user=admin_superuser)

    abstained_page = client.get(_vote_url(review_session, abstained_item))
    scored_page = client.get(_vote_url(review_session, scored_item))
    unreviewed_page = client.get(_vote_url(review_session, unreviewed_item))

    assert "You abstained" in abstained_page.content.decode()
    assert "You abstained" not in scored_page.content.decode()
    assert "You abstained" not in unreviewed_page.content.decode()


def test_get_review_adapter_with_invalid_session_type():
    conference = ConferenceFactory()
    review_session = ReviewSessionFactory(
        conference=conference,
        session_type=ReviewSession.SessionType.PROPOSALS,
    )
    # Manually set an invalid session type to test error handling
    review_session.session_type = "invalid_type"

    with pytest.raises(ValueError, match="Unknown review session type"):
        get_review_adapter(review_session)
