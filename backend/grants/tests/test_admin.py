from datetime import timedelta
from unittest.mock import call

import time_machine
import pytest
from django.utils import timezone

from grants.admin import (
    create_grant_vouchers_on_pretix,
    send_reply_emails,
    send_voucher_via_email,
)
from grants.models import Grant
from api.cms.tests.factories import GenericPageFactory
from django.http import HttpRequest
from wagtail.models import Site, Page

from django.test.utils import override_settings

pytestmark = pytest.mark.django_db


@pytest.fixture(scope="session", autouse=True)
def test_settings():
    with override_settings(
        **{
            "ALLOWED_HOSTS ": ["*"],
        }
    ):
        yield


def _setup_visa_page_and_request(request: HttpRequest, site: Site):
    """
    Configures request for testing and ensures 'visa' page existence.

    Modifies request to match site's domain and creates a 'visa' page if absent.
    """
    request.META.update({"HTTP_HOST": site.hostname, "SERVER_PORT": site.port})

    if (
        not Page.objects.live()
        .descendant_of(site.root_page)
        .filter(slug="visa")
        .exists()
    ):
        GenericPageFactory(slug="visa", parent=site.root_page)


def test_send_reply_emails_with_grants_from_multiple_conferences(
    rf, grant_factory, mocker, conference_factory, site
):
    """
    Test that sending reply emails does not proceed when selected grants belong
    to different conferences and appropriately displays an error message.
    """
    mock_messages = mocker.patch("grants.admin.messages")
    conference1 = conference_factory()
    conference2 = conference_factory()
    grant1 = grant_factory(conference=conference1, status=Grant.Status.approved)
    grant2 = grant_factory(conference=conference2, status=Grant.Status.waiting_list)
    grant3 = grant_factory(conference=conference2, status=Grant.Status.rejected)
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )
    mock_send_waiting_list_email = mocker.patch(
        "grants.admin.send_grant_reply_waiting_list_email.delay"
    )
    mock_send_rejected_email = mocker.patch(
        "grants.admin.send_grant_reply_rejected_email.delay"
    )

    send_reply_emails(
        None,
        request=request,
        queryset=Grant.objects.filter(id__in=[grant1.id, grant2.id, grant3.id]),
    )

    mock_messages.error.assert_called_once_with(
        request,
        "Please select only one conference",
    )
    mock_send_approved_email.assert_not_called()
    mock_send_waiting_list_email.assert_not_called()
    mock_send_rejected_email.assert_not_called()


def test_send_reply_emails_approved_grant_missing_approved_type(
    rf, site, grant_factory, mocker
):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(status=Grant.Status.approved, approved_type=None)
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.error.assert_called_once_with(
        request,
        f"Grant for {grant.name} is missing 'Grant Approved Type'!",
    )
    mock_send_approved_email.assert_not_called()


def test_send_reply_emails_approved_missing_amount(rf, site, grant_factory, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.approved,
        approved_type=Grant.ApprovedType.ticket_accommodation,
        total_amount=None,
    )
    grant.total_amount = None
    grant.save()
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.error.assert_called_once_with(
        request,
        f"Grant for {grant.name} is missing 'Total Amount'!",
    )
    mock_send_approved_email.assert_not_called()


def test_send_reply_emails_approved_set_deadline_in_fourteen_days(
    rf, site, grant_factory, mocker
):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.approved,
        approved_type=Grant.ApprovedType.ticket_accommodation,
        total_amount=800,
    )
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request,
        f"Sent Approved reply email to {grant.name}",
    )
    mock_send_approved_email.assert_called_once_with(
        grant_id=grant.id, is_reminder=False
    )

    grant.refresh_from_db()
    assert (
        f"{grant.applicant_reply_deadline:%Y-%m-%d}"
        == f"{(timezone.now().date() + timedelta(days=14)):%Y-%m-%d}"
    )


def test_send_reply_emails_waiting_list(rf, site, grant_factory, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.waiting_list,
    )
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)
    mock_send_waiting_list_email = mocker.patch(
        "grants.admin.send_grant_reply_waiting_list_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Waiting List reply email to {grant.name}"
    )
    mock_send_waiting_list_email.assert_called_once_with(grant_id=grant.id)


def test_send_reply_emails_waiting_list_maybe(rf, site, grant_factory, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.waiting_list_maybe,
    )
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)
    mock_send_waiting_list_email = mocker.patch(
        "grants.admin.send_grant_reply_waiting_list_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Waiting List reply email to {grant.name}"
    )
    mock_send_waiting_list_email.assert_called_once_with(grant_id=grant.id)


def test_send_reply_emails_rejected(rf, site, grant_factory, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    grant = grant_factory(
        status=Grant.Status.rejected,
    )
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)
    mock_send_rejected_email = mocker.patch(
        "grants.admin.send_grant_reply_rejected_email.delay"
    )

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.info.assert_called_once_with(
        request, f"Sent Rejected reply email to {grant.name}"
    )
    mock_send_rejected_email.assert_called_once_with(grant_id=grant.id)


def test_send_reply_emails_missing_visa_page(rf, site, grant_factory, settings, mocker):
    mock_messages = mocker.patch("grants.admin.messages")
    mock_send_approved_email = mocker.patch(
        "grants.admin.send_grant_reply_approved_email.delay"
    )
    grant_factory(
        status=Grant.Status.approved,
        approved_type=Grant.ApprovedType.ticket_accommodation,
        total_amount=800,
    )
    request = rf.get("/")
    request.META.update({"HTTP_HOST": site.hostname, "SERVER_PORT": site.port})

    send_reply_emails(None, request=request, queryset=Grant.objects.all())

    mock_messages.error.assert_called_once_with(
        request,
        "Link to the Visa Page Missing or Not Public: Please ensure the "
        "'/visa/' page is created and made public on the conference CMS "
        "before sending the emails.",
    )
    mock_send_approved_email.assert_not_called()


@time_machine.travel("2020-10-10 10:00:00", tick=False)
def test_send_voucher_via_email(
    rf,
    site,
    grant_factory,
    conference_factory,
    mocker,
):
    mocker.patch("grants.admin.messages")
    mock_send_email = mocker.patch("grants.admin.send_grant_voucher_email")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)

    grant = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
        pretix_voucher_id=2345,
        voucher_code="GRANT-532VCT",
    )
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)

    send_voucher_via_email(
        None, request, queryset=Grant.objects.filter(conference=conference)
    )

    mock_send_email.delay.assert_has_calls(
        [
            call(grant_id=grant.id),
        ]
    )


def test_send_voucher_via_email_requires_filtering_by_conference(
    rf,
    site,
    grant_factory,
    conference_factory,
    mocker,
):
    conference = conference_factory(pretix_speaker_voucher_quota_id=1234)
    conference_2 = conference_factory(pretix_speaker_voucher_quota_id=1234)
    mock_messages = mocker.patch("grants.admin.messages")
    mock_send_email = mocker.patch("grants.admin.send_grant_voucher_email")
    grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    grant_factory(
        status=Grant.Status.confirmed,
        conference=conference_2,
    )
    request = rf.get("/")
    _setup_visa_page_and_request(request, site)

    send_voucher_via_email(
        None,
        request=request,
        queryset=Grant.objects.filter(conference__in=[conference, conference_2]),
    )

    mock_messages.error.assert_called_once_with(
        request, "Please select only one conference"
    )
    mock_send_email.delay.assert_not_called()


def test_create_grant_vouchers_on_pretix(rf, conference_factory, grant_factory, mocker):
    mock_create_voucher = mocker.patch(
        "grants.admin.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mocker.patch(
        "grants.admin._generate_voucher_code",
        side_effect=["GRANT-123ZYZ", "GRANT-468ADG"],
    )
    mock_messages = mocker.patch("grants.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)

    grant_1 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
        pretix_voucher_id=None,
    )
    grant_2 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
        pretix_voucher_id=None,
    )
    request = rf.get("/")

    create_grant_vouchers_on_pretix(
        None,
        request=request,
        queryset=Grant.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_has_calls(
        [
            call(
                conference=conference,
                code="GRANT-123ZYZ",
                comment=f"Voucher for user_id={grant_1.user_id}",
                tag="grants",
                quota_id=123,
                price_mode="set",
                value="0.00",
            ),
            call(
                conference=conference,
                code="GRANT-468ADG",
                comment=f"Voucher for user_id={grant_2.user_id}",
                tag="grants",
                quota_id=123,
                price_mode="set",
                value="0.00",
            ),
        ],
        any_order=True,
    )

    grant_1.refresh_from_db()
    grant_2.refresh_from_db()

    assert grant_1.pretix_voucher_id == 1
    assert grant_1.voucher_code == "GRANT-123ZYZ"
    assert grant_2.pretix_voucher_id == 2
    assert grant_2.voucher_code == "GRANT-468ADG"
    mock_messages.success.assert_called_once_with(
        request,
        "2 Vouchers created on Pretix!",
    )


def test_create_grant_vouchers_on_pretix_only_for_missing_ones(
    rf, conference_factory, grant_factory, mocker
):
    mock_create_voucher = mocker.patch(
        "grants.admin.create_voucher",
        side_effect=[
            {"id": 1},
        ],
    )
    mocker.patch("grants.admin._generate_voucher_code", return_value="GRANT-123ZYZ")
    mocker.patch("grants.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=123)

    grant_1 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
        pretix_voucher_id=None,
    )

    grant_2 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
        pretix_voucher_id=2345,
        voucher_code="GRANT-532VCT",
    )

    create_grant_vouchers_on_pretix(
        None,
        request=rf.get("/"),
        queryset=Grant.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_called_once_with(
        conference=conference,
        code="GRANT-123ZYZ",
        comment=f"Voucher for user_id={grant_1.user_id}",
        tag="grants",
        quota_id=123,
        price_mode="set",
        value="0.00",
    )

    grant_1.refresh_from_db()
    grant_2.refresh_from_db()

    assert grant_1.pretix_voucher_id == 1
    assert grant_1.voucher_code == "GRANT-123ZYZ"
    assert grant_2.pretix_voucher_id == 2345
    assert grant_2.voucher_code == "GRANT-532VCT"


def test_create_grant_vouchers_on_pretix_doesnt_work_with_multiple_conferences(
    rf, conference_factory, grant_factory, mocker
):
    conference = conference_factory(pretix_speaker_voucher_quota_id=1234)
    conference_2 = conference_factory(pretix_speaker_voucher_quota_id=1234)
    mock_messages = mocker.patch("grants.admin.messages")
    mock_create_voucher = mocker.patch(
        "grants.admin.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    grant_1 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    grant_2 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference_2,
    )
    request = rf.get("/")

    create_grant_vouchers_on_pretix(
        None,
        request=request,
        queryset=Grant.objects.filter(conference__in=[conference, conference_2]),
    )

    mock_create_voucher.assert_not_called()
    mock_messages.error.assert_called_once_with(
        request, "Please select only one conference"
    )

    grant_1.refresh_from_db()
    grant_2.refresh_from_db()

    assert grant_1.pretix_voucher_id is None
    assert grant_1.voucher_code is None
    assert grant_2.pretix_voucher_id is None
    assert grant_2.voucher_code is None


def test_create_grant_vouchers_on_pretix_doesnt_work_without_pretix_config(
    rf, conference_factory, grant_factory, mocker
):
    mock_create_voucher = mocker.patch(
        "grants.admin.create_voucher",
        side_effect=[
            {"id": 1},
            {"id": 2},
        ],
    )
    mock_messages = mocker.patch("grants.admin.messages")

    conference = conference_factory(pretix_speaker_voucher_quota_id=None)

    grant_1 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    grant_2 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
    )

    request = rf.get("/")

    create_grant_vouchers_on_pretix(
        None,
        request=request,
        queryset=Grant.objects.filter(conference=conference),
    )

    mock_create_voucher.assert_not_called()
    mock_messages.error.assert_called_once_with(
        request,
        "Please configure the grant voucher quota ID in the conference settings",
    )

    grant_1.refresh_from_db()
    grant_2.refresh_from_db()

    assert grant_1.pretix_voucher_id is None
    assert grant_1.voucher_code is None
    assert grant_2.pretix_voucher_id is None
    assert grant_2.voucher_code is None


def test_create_grant_vouchers_only_for_confirmed_grants(
    rf, conference_factory, grant_factory, mocker
):
    mock_create_voucher = mocker.patch(
        "grants.admin.create_voucher",
        side_effect=[
            {"id": 1},
        ],
    )
    mocker.patch("grants.admin._generate_voucher_code", return_value="GRANT-123ZYZ")
    mock_messages = mocker.patch("grants.admin.messages")
    conference = conference_factory(pretix_speaker_voucher_quota_id=1223)
    grant_1 = grant_factory(
        status=Grant.Status.refused,
        conference=conference,
    )
    grant_2 = grant_factory(
        status=Grant.Status.confirmed,
        conference=conference,
    )
    request = rf.get("/")

    create_grant_vouchers_on_pretix(
        None,
        request=request,
        queryset=Grant.objects.filter(conference=conference),
    )

    grant_1.refresh_from_db()
    grant_2.refresh_from_db()

    mock_create_voucher.assert_called_once()
    mock_messages.error.assert_called_once_with(
        request,
        f"Grant for {grant_1.name} is not confirmed, we can't generate voucher for it.",
    )
    mock_messages.success.assert_called_once_with(
        request,
        "1 Vouchers created on Pretix!",
    )
    assert grant_1.pretix_voucher_id is None
    assert grant_1.voucher_code is None
    assert grant_2.pretix_voucher_id == 1
    assert grant_2.voucher_code == "GRANT-123ZYZ"
