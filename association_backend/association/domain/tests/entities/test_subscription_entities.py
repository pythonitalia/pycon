import datetime
from zoneinfo import ZoneInfo

from association.domain.entities import SubscriptionState
from association.tests.factories import SubscriptionFactory
from ward import test

rome_tz = ZoneInfo("Europe/Rome")


@test("not is_payed if no payment_date")
def _():
    s = SubscriptionFactory(payment_date=None)
    assert s.is_payed() is False


@test("is_payed if payment_date is in this year")
def _():
    s = SubscriptionFactory(
        payment_date=datetime.datetime.now(rome_tz) - datetime.timedelta(days=1)
    )
    assert s.is_payed() is True


@test("is_payed if payment_date more than one year ago year")
def _():
    s = SubscriptionFactory(
        payment_date=datetime.datetime.now(rome_tz) - datetime.timedelta(days=1 + 365)
    )
    assert s.is_payed() is True


@test("not is_expired if no payment_date")
def _():
    s = SubscriptionFactory(payment_date=None)
    print(s.payment_date)
    assert s.is_expired() is False


@test("not is_expired if payment_date is in this year")
def _():
    s = SubscriptionFactory(
        payment_date=datetime.datetime.now(rome_tz) - datetime.timedelta(days=1)
    )
    assert s.is_expired() is False


@test("is_expired if payment_date more than one year ago year")
def _():
    s = SubscriptionFactory(
        payment_date=datetime.datetime.now(rome_tz) - datetime.timedelta(days=1 + 365)
    )
    assert s.is_expired() is True


@test("calculated_state == pending if no payment_date")
def _():
    s = SubscriptionFactory(payment_date=None)
    assert s.get_calculated_state() == SubscriptionState.PENDING


@test("calculated_state == active if payment_date is in this year")
def _():
    s = SubscriptionFactory(
        payment_date=datetime.datetime.now(rome_tz) - datetime.timedelta(days=1)
    )
    assert s.get_calculated_state() == SubscriptionState.ACTIVE


@test("calculated_state == expired if payment_date more than one year ago year")
def _():
    s = SubscriptionFactory(
        payment_date=datetime.datetime.now(rome_tz) - datetime.timedelta(days=1 + 365)
    )
    assert s.get_calculated_state() == SubscriptionState.EXPIRED
