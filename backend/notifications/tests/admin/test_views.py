from notifications.admin.views import view_email_template, view_sent_email
from notifications.tests.factories import EmailTemplateFactory, SentEmailFactory


def test_view_email_template(rf):
    request = rf.get("/")
    email_template = EmailTemplateFactory(body="Hello world!")
    response = view_email_template(request, email_template.id)

    assert b"Hello world!" in response.content


def test_view_sent_email(rf):
    request = rf.get("/")
    sent_email = SentEmailFactory(body="Hello world!")
    response = view_sent_email(request, sent_email.id)

    assert b"Hello world!" in response.content
