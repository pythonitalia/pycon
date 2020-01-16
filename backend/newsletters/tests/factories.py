import factory
import pytz
from factory.django import DjangoModelFactory
from newsletters.models import Email, Subscription
from pytest_factoryboy import register


@register
class SubscriptionFactory(DjangoModelFactory):
    class Meta:
        model = Subscription
        django_get_or_create = ("email",)

    email = factory.Faker("email")


@register
class EmailFactory(DjangoModelFactory):
    class Meta:
        model = Email

    subject = factory.Faker("sentence")
    heading = factory.Faker("sentence", nb_words=3)
    body = factory.Faker("text")
    cta_label = factory.Faker("word")
    cta_link = factory.Faker("url")
    recipients_type = "newsletters"
    scheduled_date = factory.Faker("future_datetime", tzinfo=pytz.UTC)

    @factory.post_generation
    def recipients(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for email in extracted:
                self.recipients.append(email)
