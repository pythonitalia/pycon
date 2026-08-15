import pytest

from generic_forms.models import FormQuestion
from generic_forms.services import (
    display_answer_value,
    display_answers,
    unwrap_answers,
    validate_answers,
    wrap_answers,
)
from generic_forms.tests.factories import FormFactory, FormQuestionFactory

pytestmark = pytest.mark.django_db


OPTIONS = [{"id": "vegan", "label": "Vegan"}, {"id": "veggie", "label": "Veggie"}]


def _question(question_type, **kwargs):
    return FormQuestionFactory(question_type=question_type, **kwargs)


def test_valid_answers_return_no_errors():
    form = FormFactory()
    text = _question(FormQuestion.QuestionType.TEXT, form=form, required=True)
    textarea = _question(FormQuestion.QuestionType.TEXTAREA, form=form)
    select = _question(FormQuestion.QuestionType.SELECT, form=form, options=OPTIONS)
    multi = _question(
        FormQuestion.QuestionType.MULTI_SELECT, form=form, options=OPTIONS
    )
    boolean = _question(FormQuestion.QuestionType.BOOLEAN, form=form)
    url = _question(FormQuestion.QuestionType.URL, form=form)

    errors = validate_answers(
        form,
        {
            str(text.pk): "an answer",
            str(textarea.pk): "a longer answer",
            str(select.pk): "vegan",
            str(multi.pk): ["vegan", "veggie"],
            str(boolean.pk): True,
            str(url.pk): "https://example.com",
        },
    )

    assert errors == {}


def test_missing_required_answer_is_an_error():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.TEXT, form=form, required=True)

    errors = validate_answers(form, {})

    assert errors == {str(question.pk): ["This question is required."]}


def test_empty_string_fails_required():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.TEXT, form=form, required=True)

    errors = validate_answers(form, {str(question.pk): ""})

    assert errors == {str(question.pk): ["This question is required."]}


def test_optional_question_can_be_omitted():
    form = FormFactory()
    _question(FormQuestion.QuestionType.TEXT, form=form, required=False)

    assert validate_answers(form, {}) == {}


def test_answering_false_satisfies_a_required_boolean():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.BOOLEAN, form=form, required=True)

    assert validate_answers(form, {str(question.pk): False}) == {}


def test_unknown_question_id_is_an_error():
    form = FormFactory()

    errors = validate_answers(form, {"9999": "hello"})

    assert errors == {"9999": ["Unknown or inactive question."]}


def test_inactive_question_id_is_an_error():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.TEXT, form=form, active=False)

    errors = validate_answers(form, {str(question.pk): "hello"})

    assert errors == {str(question.pk): ["Unknown or inactive question."]}


def test_text_answer_must_be_a_string():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.TEXT, form=form)

    errors = validate_answers(form, {str(question.pk): 123})

    assert errors == {str(question.pk): ["Invalid value: expected text."]}


def test_text_answer_respects_max_length():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.TEXT, form=form, max_length=5)

    errors = validate_answers(form, {str(question.pk): "too long"})

    assert errors == {str(question.pk): ["Cannot be longer than 5 characters."]}


def test_select_answer_must_be_a_known_option():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.SELECT, form=form, options=OPTIONS)

    errors = validate_answers(form, {str(question.pk): "carnivore"})

    assert errors == {str(question.pk): ["Invalid option."]}


def test_multi_select_must_be_a_list():
    form = FormFactory()
    question = _question(
        FormQuestion.QuestionType.MULTI_SELECT, form=form, options=OPTIONS
    )

    errors = validate_answers(form, {str(question.pk): "vegan"})

    assert errors == {
        str(question.pk): ["Invalid value: expected a list of option ids."]
    }


def test_multi_select_rejects_non_string_items_without_crashing():
    form = FormFactory()
    question = _question(
        FormQuestion.QuestionType.MULTI_SELECT, form=form, options=OPTIONS
    )

    errors = validate_answers(form, {str(question.pk): [["vegan"]]})

    assert errors == {
        str(question.pk): ["Invalid value: expected a list of option ids."]
    }


def test_non_dict_answers_return_a_global_error():
    form = FormFactory()

    errors = validate_answers(form, ["not", "a", "dict"])

    assert errors == {"__all__": ["Invalid answers format."]}


def test_multi_select_rejects_a_single_unknown_item():
    form = FormFactory()
    question = _question(
        FormQuestion.QuestionType.MULTI_SELECT, form=form, options=OPTIONS
    )

    errors = validate_answers(form, {str(question.pk): ["vegan", "carnivore"]})

    assert errors == {str(question.pk): ["Invalid options: carnivore."]}


def test_boolean_answer_must_be_a_bool():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.BOOLEAN, form=form)

    errors = validate_answers(form, {str(question.pk): "yes"})

    assert errors == {str(question.pk): ["Invalid value: expected true or false."]}


def test_url_answer_must_be_a_valid_url():
    form = FormFactory()
    question = _question(FormQuestion.QuestionType.URL, form=form)

    errors = validate_answers(form, {str(question.pk): "not a url"})

    assert errors == {str(question.pk): ["Invalid URL."]}


def test_multiple_errors_are_collected_per_call():
    form = FormFactory()
    required = _question(FormQuestion.QuestionType.TEXT, form=form, required=True)
    boolean = _question(FormQuestion.QuestionType.BOOLEAN, form=form)

    errors = validate_answers(form, {str(boolean.pk): "yes"})

    assert errors == {
        str(required.pk): ["This question is required."],
        str(boolean.pk): ["Invalid value: expected true or false."],
    }


def test_wrap_and_unwrap_answers_round_trip():
    answers = {"1": "hello", "2": ["a", "b"], "3": False}

    envelope = wrap_answers(answers)

    assert envelope == {"version": 1, "answers": answers}
    assert unwrap_answers(envelope) == answers


def test_unwrap_answers_rejects_unknown_versions():
    with pytest.raises(ValueError, match="version"):
        unwrap_answers({"version": 2, "answers": {}})


def test_unwrap_answers_treats_empty_envelope_as_no_answers():
    assert unwrap_answers({}) == {}


def test_unwrap_answers_rejects_malformed_envelopes():
    with pytest.raises(ValueError, match="Malformed answers envelope"):
        unwrap_answers(["not", "a", "dict"])
    with pytest.raises(ValueError, match="missing answers map"):
        unwrap_answers({"version": 1})
    with pytest.raises(ValueError, match="missing answers map"):
        unwrap_answers({"version": 1, "answers": "not a dict"})


def test_display_answer_value_formats_by_question_type():
    select = FormQuestionFactory(
        question_type=FormQuestion.QuestionType.SELECT, options=OPTIONS
    )
    multi = FormQuestionFactory(
        question_type=FormQuestion.QuestionType.MULTI_SELECT, options=OPTIONS
    )
    boolean = FormQuestionFactory(question_type=FormQuestion.QuestionType.BOOLEAN)
    text = FormQuestionFactory(question_type=FormQuestion.QuestionType.TEXT)

    assert display_answer_value(select, "vegan") == "Vegan"
    assert display_answer_value(select, "unknown-id") == "unknown-id"
    assert display_answer_value(multi, ["vegan", "veggie"]) == "Vegan, Veggie"
    assert display_answer_value(boolean, True) == "Yes"
    assert display_answer_value(boolean, False) == "No"
    assert display_answer_value(text, "hello") == "hello"
    assert display_answer_value(text, None) == ""


def test_display_answers_pairs_labels_with_values_in_question_order():
    from generic_forms.tests.factories import FormAnswerFactory

    form = FormFactory()
    second = FormQuestionFactory(form=form, label="Second", order=1)
    first = FormQuestionFactory(
        form=form,
        label="First",
        order=0,
        question_type=FormQuestion.QuestionType.BOOLEAN,
    )
    FormQuestionFactory(form=form, label="Unanswered", order=2)
    inactive = FormQuestionFactory(
        form=form, label="Deactivated", order=3, active=False
    )
    answer = FormAnswerFactory(
        form=form,
        answers=wrap_answers(
            {
                str(second.pk): "text answer",
                str(first.pk): True,
                str(inactive.pk): "historical",
                "9999": "orphan",
            }
        ),
    )

    assert display_answers(answer) == [
        ("First", "Yes"),
        ("Second", "text answer"),
        ("Deactivated", "historical"),
        ("Question 9999", "orphan"),
    ]
