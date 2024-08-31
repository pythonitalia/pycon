from notifications.admin.views import view_email_template, view_sent_email
from notifications.tests.factories import EmailTemplateFactory, SentEmailFactory


def test_view_email_template():
    email_template = EmailTemplateFactory(body="Hello world!")
    response = view_email_template(None, email_template.id)

    assert b"Hello world!" in response.content


def test_view_sent_email():
    sent_email = SentEmailFactory(body="Hello world!")
    response = view_sent_email(None, sent_email.id)

    assert b"Hello world!" in response.content
