import pytest
from django.utils import timezone

from ..graphs import get_conference_tickets_sold_by_date, get_deadlines


@pytest.mark.django_db
def test_query_ticket_sold_by_date(
    ticket_factory, ticket_fare_factory, order_factory, conference_factory
):
    now = timezone.now()

    DAYS_TO_START = 10
    TICKETS_SOLD = 3
    start = now + timezone.timedelta(days=DAYS_TO_START)
    conference = conference_factory(start=start)
    ticket_fare = ticket_fare_factory(conference=conference)

    for _ in range(TICKETS_SOLD):
        ticket_factory(ticket_fare=ticket_fare, order=order_factory(created=now))

    resp = get_conference_tickets_sold_by_date(conference)
    assert list(resp) == [
        {
            "days_to_start": timezone.timedelta(days=-DAYS_TO_START),
            "count": TICKETS_SOLD,
        }
    ]


@pytest.mark.django_db
def test_query_get_deadlines(
    deadline_factory, ticket_fare_factory, order_factory, conference_factory
):
    now = timezone.now()

    DAYS_TO_START = 10
    start = now + timezone.timedelta(days=DAYS_TO_START)
    conference = conference_factory(start=start)

    deadline_factory(
        start=now - timezone.timedelta(days=20),
        end=now - timezone.timedelta(days=15),
        conference=conference,
        type="voting",
        name="voting",
    )

    deadline_factory(
        start=now - timezone.timedelta(days=1),
        end=now,
        conference=conference,
        type="cfp",
        name="cfp",
    )
    resp = get_deadlines(conference)
    assert resp
