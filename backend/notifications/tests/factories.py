from users.tests.factories import UserFactory
from conferences.tests.factories import ConferenceFactory
from notifications.models import EmailTemplate, EmailTemplateIdentifier, SentEmail
import factory.fuzzy
from factory.django import DjangoModelFactory


class EmailTemplateFactory(DjangoModelFactory):
    conference = factory.SubFactory(ConferenceFactory)
    identifier = EmailTemplateIdentifier.proposal_accepted
    subject = "Subject"
    preview_text = "Preview text"
    body = "Body"

    class Meta:
        model = EmailTemplate
        django_get_or_create = ("conference", "identifier")


class SentEmailFactory(DjangoModelFactory):
    email_template = factory.SubFactory(EmailTemplateFactory)
    conference = factory.SelfAttribute("email_template.conference")
    recipient = factory.SubFactory(UserFactory)
    recipient_email = factory.SelfAttribute("recipient.email")
    subject = "subject"
    body = "body"
    text_body = "text body"
    preview_text = "preview text"
    from_email = "example@example.com"

    class Meta:
        model = SentEmail
