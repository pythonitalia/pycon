from django.utils import timezone
import pytest
from users.tests.factories import UserFactory
from notifications.models import (
    EmailTemplate,
    EmailTemplateIdentifier,
    SentEmail,
    SentEmailEvent,
)
from notifications.tests.factories import EmailTemplateFactory, SentEmailFactory


def test_render_email_template():
    email_template = EmailTemplateFactory(
        subject="Subject {{ test }}",
        body="Body {{ test }}",
        preview_text="Preview {{ test }}",
    )
    result = email_template.render(
        placeholders={
            "test": "abc",
        },
        show_placeholders=False,
    )

    assert result.subject == "Subject abc"
    assert result.body == "Body abc"
    assert result.preview_text == "Preview abc"
    assert "<title>Subject abc</title>" in result.html_body


def test_render_email_template_showing_placeholders():
    email_template = EmailTemplateFactory(
        subject="Subject {{ test }}",
        body="Body {{ test }}",
        preview_text="Preview {{ test }}",
    )
    result = email_template.render(placeholders={}, show_placeholders=True)

    assert result.subject == "Subject {{test}}"
    assert result.body == "Body {{test}}"
    assert result.preview_text == "Preview {{test}}"


def test_send_email_template_to_recipient_email(
    mocker, django_capture_on_commit_callbacks
):
    email_template = EmailTemplateFactory(
        subject="Subject {{ test }}",
        body="Body {{ test }}",
        preview_text="Preview {{ test }}",
        reply_to="replyto@example.com",
    )

    mock_send_pending_emails = mocker.patch(
        "notifications.tasks.send_pending_emails.delay"
    )

    with django_capture_on_commit_callbacks(execute=True):
        email_template.send_email(
            recipient_email="example@example.com",
            placeholders={
                "test": "abc",
            },
        )

    mock_send_pending_emails.assert_called_once()

    sent_email = SentEmail.objects.get(
        email_template=email_template,
    )

    assert sent_email.recipient is None
    assert sent_email.recipient_email == "example@example.com"

    assert sent_email.subject == "Subject abc"
    assert "Body abc" in sent_email.body
    assert sent_email.preview_text == "Preview abc"
    assert sent_email.reply_to == "replyto@example.com"


def test_send_email_template_to_recipient_user():
    user = UserFactory()
    email_template = EmailTemplateFactory(
        subject="Subject {{ test }}",
        body="Body {{ test }}",
        preview_text="Preview {{ test }}",
        reply_to="replyto@example.com",
    )
    email_template.send_email(
        recipient=user,
        placeholders={
            "test": "abc",
        },
    )

    sent_email = SentEmail.objects.get(
        email_template=email_template,
    )

    assert sent_email.recipient == user
    assert sent_email.recipient_email == user.email

    assert sent_email.subject == "Subject abc"
    assert "Body abc" in sent_email.body
    assert sent_email.preview_text == "Preview abc"
    assert sent_email.reply_to == "replyto@example.com"


def test_send_system_template_email(settings):
    settings.DEFAULT_FROM_EMAIL = "example@example.com"

    user = UserFactory()
    email_template = EmailTemplateFactory(
        subject="Subject {{ test }}",
        body="Body {{ test }}",
        preview_text="Preview {{ test }}",
        reply_to="replyto@example.com",
        is_system_template=True,
        conference=None,
        identifier=EmailTemplateIdentifier.reset_password,
    )
    email_template.send_email(
        recipient=user,
        placeholders={
            "test": "abc",
        },
    )

    sent_email = SentEmail.objects.get(
        email_template=email_template,
    )

    assert sent_email.conference_id is None
    assert sent_email.recipient == user
    assert sent_email.recipient_email == user.email
    assert sent_email.from_email == "example@example.com"

    assert sent_email.subject == "Subject abc"
    assert "Body abc" in sent_email.body
    assert sent_email.preview_text == "Preview abc"
    assert sent_email.reply_to == "replyto@example.com"


def test_need_to_specify_recipient():
    email_template = EmailTemplateFactory(
        subject="Subject {{ test }}",
        body="Body {{ test }}",
        preview_text="Preview {{ test }}",
        reply_to="replyto@example.com",
    )

    with pytest.raises(
        ValueError, match="Either recipient or recipient_email must be provided"
    ):
        email_template.send_email(
            placeholders={
                "test": "abc",
            }
        )


def test_email_template_placeholders_available():
    email_template = EmailTemplateFactory(
        identifier=EmailTemplateIdentifier.proposal_accepted
    )
    assert "conference_name" in email_template.get_placeholders_available()

    email_template = EmailTemplateFactory(identifier=EmailTemplateIdentifier.custom)
    assert "conference" in email_template.get_placeholders_available()


def test_email_template_is_custom():
    email_template = EmailTemplateFactory(
        identifier=EmailTemplateIdentifier.proposal_accepted
    )
    assert not email_template.is_custom

    email_template = EmailTemplateFactory(identifier=EmailTemplateIdentifier.custom)
    assert email_template.is_custom


def test_email_template_requires_conference_when_not_system_template():
    email_template = EmailTemplateFactory(
        identifier=EmailTemplateIdentifier.proposal_accepted
    )
    email_template.is_system_template = False
    email_template.conference = None

    with pytest.raises(
        ValueError,
        match="Templates must be associated with a conference if not system template",
    ):
        email_template.save()


def test_email_template_conference_must_be_null_for_system_templates():
    email_template = EmailTemplateFactory(
        identifier=EmailTemplateIdentifier.proposal_accepted
    )
    email_template.is_system_template = True

    with pytest.raises(
        ValueError, match="System templates cannot be associated with a conference"
    ):
        email_template.save()


def test_sent_email_is_bounced():
    sent_email = SentEmailFactory()

    assert not sent_email.is_bounced

    sent_email.record_event(SentEmailEvent.Event.bounced, timezone.now(), {})

    assert sent_email.is_bounced


def test_sent_email_is_complained():
    sent_email = SentEmailFactory()

    assert not sent_email.is_complained

    sent_email.record_event(SentEmailEvent.Event.complained, timezone.now(), {})

    assert sent_email.is_complained


def test_sent_email_is_delivered():
    sent_email = SentEmailFactory()

    assert not sent_email.is_delivered

    sent_email.record_event(SentEmailEvent.Event.delivered, timezone.now(), {})

    assert sent_email.is_delivered


def test_sent_email_is_opened():
    sent_email = SentEmailFactory()

    assert not sent_email.is_opened

    sent_email.record_event(SentEmailEvent.Event.opened, timezone.now(), {})

    assert sent_email.is_opened


def test_email_template_system_templates_filter():
    email_template = EmailTemplateFactory(
        subject="Subject {{ test }}",
        body="Body {{ test }}",
        preview_text="Preview {{ test }}",
        reply_to="replyto@example.com",
        is_system_template=True,
        conference=None,
        identifier=EmailTemplateIdentifier.reset_password,
    )

    EmailTemplateFactory(
        identifier=EmailTemplateIdentifier.proposal_accepted,
        is_system_template=False,
    )

    assert EmailTemplate.objects.system_templates().count() == 1
    assert EmailTemplate.objects.system_templates().first().id == email_template.id
