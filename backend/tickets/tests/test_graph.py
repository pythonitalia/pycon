import datetime
import itertools

import factory
import factory.fuzzy
import pytest
from django.utils import timezone

from ..graphs import get_conference_tickets_sold_by_date, get_plot_data


@pytest.fixture
def generate_tickets(order_factory, ticket_fare_factory, ticket_factory):
    def wrapper(conference, n=10):
        ticket_fare = ticket_fare_factory(conference=conference)

        # suppose we sart selling ticket 6 months before start
        start_selling = conference.start - timezone.timedelta(days=30 * 6)
        fuzz = factory.fuzzy.FuzzyDate(start_selling, conference.start)

        tickets = []
        for _ in range(n):
            date_sold = fuzz.fuzz()
            order = order_factory(created=date_sold)
            ticket = ticket_factory(ticket_fare=ticket_fare, order=order)
            tickets.append(ticket)
        return tickets

    return wrapper


@pytest.fixture
def generate_conference(conference_factory, deadline_factory):
    def wrapper(years_ago=0):

        start = datetime.date.today() - timezone.timedelta(days=365 * years_ago)
        end = start + timezone.timedelta(days=3)
        conference = conference_factory(start=start, end=end)
        deadline_factory(
            start=start - timezone.timedelta(days=20),
            end=start - timezone.timedelta(days=15),
            conference=conference,
            type="voting",
            name="voting",
        )

        deadline_factory(
            start=start - timezone.timedelta(days=1),
            end=start,
            conference=conference,
            type="cfp",
            name="cfp",
        )

        return conference

    return wrapper


def _get_tickets_sold_output(conference, tickets):
    def order_by(ticket):
        return ticket.order.created

    output = []
    count = 0
    for date, ticket_group in itertools.groupby(
        sorted(tickets, key=order_by), key=order_by
    ):
        count += len(list(ticket_group))
        days_to_start = (date - conference.start).days
        output.append((days_to_start, count))

    return output


@pytest.mark.django_db
def test_query_ticket_sold_by_date(
    ticket_factory, ticket_fare_factory, order_factory, generate_conference
):

    DAYS_TO_START = 10
    TICKETS_SOLD = 3
    conference = generate_conference(years_ago=1)
    ticket_fare = ticket_fare_factory(conference=conference)

    for _ in range(TICKETS_SOLD):
        date_sold = conference.start - timezone.timedelta(days=DAYS_TO_START)
        order = order_factory(created=date_sold)
        ticket_factory(ticket_fare=ticket_fare, order=order)

    resp = get_conference_tickets_sold_by_date(conference)
    assert list(resp) == [
        {
            "days_to_start": timezone.timedelta(days=-DAYS_TO_START),
            "count": TICKETS_SOLD,
        }
    ]


@pytest.mark.django_db
def test_data(generate_conference, generate_tickets):

    # older conference (2 years ago)
    conference_one = generate_conference(years_ago=2)
    tickets_conf_one = generate_tickets(conference_one)

    # latest conference (1 year ago)
    conference_two = generate_conference(years_ago=1)
    tickets_conf_two = generate_tickets(conference_two)

    resp = get_plot_data()

    # the oldest conference first
    assert resp[0]["conference"].code == conference_one.code
    assert resp[1]["conference"].code == conference_two.code

    output = _get_tickets_sold_output(conference_one, tickets_conf_one)
    for index, sold in enumerate(resp[0]["sold_tickets"]):
        output_days, output_total = output[index]
        assert sold["days_to_start"].days == output_days
        assert sold["total"] == output_total

    output = _get_tickets_sold_output(conference_two, tickets_conf_two)
    for index, sold in enumerate(resp[1]["sold_tickets"]):
        output_days, output_total = output[index]
        assert sold["days_to_start"].days == output_days
        assert sold["total"] == output_total
