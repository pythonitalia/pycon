import pytest
from users.tests.factories import UserFactory
from notifications.models import SentEmail
from notifications.tests.factories import EmailTemplateFactory


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


def test_send_email_template_to_recipient_email():
    email_template = EmailTemplateFactory(
        subject="Subject {{ test }}",
        body="Body {{ test }}",
        preview_text="Preview {{ test }}",
        reply_to="replyto@example.com",
    )
    email_template.send_email(
        recipient_email="example@example.com",
        placeholders={
            "test": "abc",
        },
    )

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
