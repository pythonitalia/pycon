import datetime
from zoneinfo import ZoneInfo

from association.domain.entities import SubscriptionState
from association.tests.factories import SubscriptionFactory
from ward import test

rome_tz = ZoneInfo("Europe/Rome")


@test("calculated_state == pending if no due_date")
def _():
    s = SubscriptionFactory(due_date=None)
    assert s.get_calculated_state() == SubscriptionState.PENDING


@test("calculated_state == active if due_date is in this year")
def _():
    s = SubscriptionFactory(
        due_date=datetime.datetime.now(rome_tz) - datetime.timedelta(days=1)
    )
    assert s.get_calculated_state() == SubscriptionState.ACTIVE


@test("calculated_state == expired if due_date more than one year ago year")
def _():
    s = SubscriptionFactory(
        due_date=datetime.datetime.now(rome_tz) - datetime.timedelta(days=1 + 365)
    )
    assert s.get_calculated_state() == SubscriptionState.EXPIRED
