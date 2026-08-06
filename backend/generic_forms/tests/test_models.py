import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from generic_forms.models import Form, FormQuestion
from generic_forms.tests.factories import (
    FormAnswerFactory,
    FormFactory,
    FormQuestionFactory,
)

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


def _answered_question(**kwargs):
    question = FormQuestionFactory(**kwargs)
    FormAnswerFactory(form=question.form)
    return question


def test_question_type_is_frozen_once_form_has_answers():
    question = _answered_question(question_type=FormQuestion.QuestionType.TEXT)

    question.question_type = FormQuestion.QuestionType.TEXTAREA
    with pytest.raises(ValidationError, match="question_type"):
        question.save()


def test_options_are_frozen_once_form_has_answers():
    question = _answered_question(
        question_type=FormQuestion.QuestionType.SELECT,
        options=[{"id": "a", "label": "A"}],
    )

    question.options = [{"id": "b", "label": "B"}]
    with pytest.raises(ValidationError, match="options"):
        question.save()


def test_required_is_frozen_once_form_has_answers():
    question = _answered_question(required=False)

    question.required = True
    with pytest.raises(ValidationError, match="required"):
        question.save()


def test_question_cannot_move_to_another_form_once_answered():
    question = _answered_question()

    question.form = FormFactory()
    with pytest.raises(ValidationError, match="form"):
        question.save()


def test_semantic_fields_are_editable_while_form_has_no_answers():
    question = FormQuestionFactory(question_type=FormQuestion.QuestionType.TEXT)

    question.question_type = FormQuestion.QuestionType.TEXTAREA
    question.required = True
    question.save()


def test_label_description_order_active_stay_editable_once_answered():
    question = _answered_question()

    question.label = "Updated label"
    question.description = "Updated description"
    question.order = 42
    question.active = False
    question.save()

    question.refresh_from_db()
    assert question.label == "Updated label"
    assert question.active is False


def test_question_cannot_be_deleted_once_form_has_answers():
    question = _answered_question()

    with pytest.raises(ValidationError, match="deleted"):
        question.delete()


def test_question_can_be_deleted_while_form_has_no_answers():
    question = FormQuestionFactory()

    question.delete()

    assert not FormQuestion.objects.filter(pk=question.pk).exists()


def test_new_question_can_be_added_to_answered_form():
    question = _answered_question()

    FormQuestionFactory(form=question.form)
