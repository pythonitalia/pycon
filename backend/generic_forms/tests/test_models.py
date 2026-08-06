import pytest
from django.db import IntegrityError

from generic_forms.models import Form
from generic_forms.tests.factories import FormAnswerFactory, FormFactory

pytestmark = pytest.mark.django_db


def test_form_answer_is_unique_per_form_and_user():
    answer = FormAnswerFactory()

    with pytest.raises(IntegrityError):
        FormAnswerFactory(form=answer.form, user=answer.user)


def test_same_user_can_answer_different_forms():
    answer = FormAnswerFactory()

    FormAnswerFactory(user=answer.user)


def test_only_one_form_per_conference_and_purpose():
    form = FormFactory(purpose=Form.Purpose.GRANT)

    with pytest.raises(IntegrityError):
        FormFactory(conference=form.conference, purpose=Form.Purpose.GRANT)


def test_multiple_generic_forms_per_conference_are_allowed():
    form = FormFactory(purpose=Form.Purpose.GENERIC)

    FormFactory(conference=form.conference, purpose=Form.Purpose.GENERIC)


def test_same_purpose_is_allowed_on_different_conferences():
    FormFactory(purpose=Form.Purpose.GRANT)

    FormFactory(purpose=Form.Purpose.GRANT)
