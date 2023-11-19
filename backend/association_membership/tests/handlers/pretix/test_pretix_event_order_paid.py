import pytest
import datetime
from datetime import timezone

import time_machine
from django.conf import settings
from association_membership.models import (
    Membership,
)
from association_membership.enums import (
    PaymentStatus,
    MembershipStatus,
)
from association_membership.tests.factories import MembershipFactory
from association_membership.exceptions import (
    NotEnoughPaid,
    NoUserFoundWithEmail,
    UserIsAlreadyAMember,
)
from association_membership.handlers.pretix.pretix_event_order_paid import (
    pretix_event_order_paid,
)
from association_membership.tests.handlers.pretix.payloads import (
    CATEGORIES,
    ITEMS_WITH_CATEGORY,
    ORDER_DATA_WITH_MEMBERSHIP,
    ORDER_DATA_WITH_REFUND_EVERYTHING_AND_NOT_ENOUGH_TO_COVER_MEMBERSHIP,
    ORDER_DATA_WITH_REFUND_EVERYTHING_BUT_MEMBERSHIP,
    ORDER_DATA_WITH_REFUNDS,
    ORDER_DATA_WITHOUT_MEMBERSHIP,
    ORDER_PAID,
)
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_receive_order_paid_with_membership(requests_mock):
    user = UserFactory(email="pretix@example.org")
    with time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )
        pretix_event_order_paid(ORDER_PAID)

    created_membership = Membership.objects.get(user_id=user.id)

    assert created_membership.status == MembershipStatus.ACTIVE
    assert created_membership.user_id == user.id
    assert created_membership.payments.count() == 1

    payment = created_membership.payments.all()[0]
    assert payment.total == 1000
    assert payment.payment_date == datetime.datetime(
        2021, 12, 16, 1, 4, 43, tzinfo=timezone.utc
    )
    assert payment.period_start == datetime.datetime(
        2021, 12, 16, 1, 4, 43, tzinfo=timezone.utc
    )
    assert payment.period_end == datetime.datetime(
        2022, 12, 16, 1, 4, 43, tzinfo=timezone.utc
    )
    assert payment.status == PaymentStatus.PAID

    pretix_payment = payment.pretix_payments.first()
    assert pretix_payment.order_code == "9YKZK"
    assert pretix_payment.event_organizer == "test-organizer"
    assert pretix_payment.event_id == "local-conf-test"


def test_receive_order_paid_twice_doesnt_process_the_payment_twice(requests_mock):
    user = UserFactory(email="pretix@example.org")

    with time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )
        pretix_event_order_paid(ORDER_PAID)

        created_membership = Membership.objects.get(user_id=user.id)

        assert created_membership.status == MembershipStatus.ACTIVE
        assert created_membership.payments.count() == 1

        pretix_event_order_paid(ORDER_PAID)

        created_membership = Membership.objects.get(user_id=user.id)

        assert created_membership.status == MembershipStatus.ACTIVE
        assert created_membership.payments.count() == 1


def test_receive_order_paid_without_membership_purchase(requests_mock):
    with time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITHOUT_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )
        pretix_event_order_paid(ORDER_PAID)

    assert not Membership.objects.filter(user_id=1).exists()


def test_receive_order_paid_fails_if_no_user_maps_to_the_email(requests_mock):
    with time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )

        with pytest.raises(
            NoUserFoundWithEmail,
            match="No user found with the email of order_code=9YKZK",
        ):
            pretix_event_order_paid(ORDER_PAID)

    assert not Membership.objects.exists()


def test_receive_order_paid_with_canceled_subscription(requests_mock):
    """
    Test receiving an order paid with a canceled subscription.
    """
    user = UserFactory(email="pretix@example.org")
    existing_subscription = MembershipFactory(
        user=user, status=MembershipStatus.CANCELED
    )

    with time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )

        pretix_event_order_paid(ORDER_PAID)

    created_membership = Membership.objects.get(user=user)

    assert created_membership.id == existing_subscription.id
    assert created_membership.status == MembershipStatus.ACTIVE
    assert created_membership.user_id == user.id
    assert created_membership.payments.count() == 1


def test_receive_order_paid_of_period_outside_current_one(requests_mock):
    """
    Test receiving an order paid of a period outside the current one.
    """
    user = UserFactory(email="pretix@example.org")

    with time_machine.travel("2023-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )
        pretix_event_order_paid(ORDER_PAID)

    created_membership = Membership.objects.get(user_id=user.id)

    # We still accept the payment but we don't change to ACTIVE
    assert created_membership.status == MembershipStatus.PENDING
    assert created_membership.user_id == user.id
    assert created_membership.payments.count() == 1


def test_receive_order_paid_of_already_subscribed_fails_with_error_message(
    requests_mock,
):
    """
    Test receiving an order paid of a user who is already subscribed to the association.
    """
    user = UserFactory(email="pretix@example.org")
    MembershipFactory(user=user, status=MembershipStatus.ACTIVE)

    with time_machine.travel("2023-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )

        with pytest.raises(
            UserIsAlreadyAMember, match="User is already subscribed to the association"
        ):
            pretix_event_order_paid(ORDER_PAID)

    created_membership = Membership.objects.get(user_id=user.id)

    # We still accept the payment but we don't change ACTIVE
    assert created_membership.status == MembershipStatus.ACTIVE
    assert created_membership.payments.count() == 0


def test_can_subscribe_with_mix_of_manual_and_refunds(requests_mock):
    """
    Test subscribing with a mix of manual and refunds.
    """
    user = UserFactory(email="pretix@example.org")

    with time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_REFUNDS,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )
        requests_mock.post(
            "http://users-backend-url/internal-api",
            json={"data": {"userByEmail": {"id": 1}}},
        )

        pretix_event_order_paid(ORDER_PAID)

    created_membership = Membership.objects.get(user_id=user.id)

    assert created_membership.status == MembershipStatus.ACTIVE
    assert created_membership.user_id == user.id
    assert created_membership.payments.count() == 1

    payment = created_membership.payments.all()[0]
    assert payment.total == 1000


def test_receive_order_paid_with_refunds_but_enough_to_cover_membership(requests_mock):
    """
    If some has been refunded but the user paid enough to cover
    the membership price it gets accepted.
    """
    user = UserFactory(email="pretix@example.org")

    with time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_REFUND_EVERYTHING_BUT_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )
        requests_mock.post(
            "http://users-backend-url/internal-api",
            json={"data": {"userByEmail": {"id": 1}}},
        )

        pretix_event_order_paid(ORDER_PAID)

    created_membership = Membership.objects.get(user_id=user.id)

    assert created_membership.status == MembershipStatus.ACTIVE
    assert created_membership.user_id == user.id
    assert created_membership.payments.count() == 1

    payment = created_membership.payments.all()[0]
    assert payment.total == 1000


def test_order_rejected_if_not_enough_paid(requests_mock):
    user = UserFactory(email="pretix@example.org")

    with time_machine.travel("2021-12-16 01:04:50Z", tick=False):
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/orders/9YKZK/",
            json=ORDER_DATA_WITH_REFUND_EVERYTHING_AND_NOT_ENOUGH_TO_COVER_MEMBERSHIP,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/items/?active=true&category=25",
            json=ITEMS_WITH_CATEGORY,
        )
        requests_mock.get(
            f"{settings.PRETIX_API}organizers/test-organizer/events/local-conf-test/categories/",
            json=CATEGORIES,
        )

        with pytest.raises(NotEnoughPaid):
            pretix_event_order_paid(ORDER_PAID)

    created_membership = Membership.objects.get(user_id=user.id)

    assert created_membership.status == MembershipStatus.PENDING
    assert created_membership.user_id == user.id
    assert created_membership.payments.count() == 0
