import factory
from factory.django import DjangoModelFactory

from conferences.tests.factories import ConferenceFactory
from generic_forms.models import Form, FormAnswer, FormQuestion
from users.tests.factories import UserFactory


class FormFactory(DjangoModelFactory):
    class Meta:
        model = Form

    conference = factory.SubFactory(ConferenceFactory)
    purpose = Form.Purpose.GENERIC
    name = factory.Faker("sentence", nb_words=3)


class FormQuestionFactory(DjangoModelFactory):
    class Meta:
        model = FormQuestion

    form = factory.SubFactory(FormFactory)
    label = factory.Faker("sentence", nb_words=5)
    question_type = FormQuestion.QuestionType.TEXT
    required = False
    order = factory.Sequence(lambda n: n)


class FormAnswerFactory(DjangoModelFactory):
    class Meta:
        model = FormAnswer

    form = factory.SubFactory(FormFactory)
    user = factory.SubFactory(UserFactory)
    answers = factory.LazyFunction(dict)
