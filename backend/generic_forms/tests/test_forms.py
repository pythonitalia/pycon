import pytest

from generic_forms.forms import FormQuestionInlineForm, OptionsField
from generic_forms.models import FormQuestion
from generic_forms.tests.factories import FormFactory

pytestmark = pytest.mark.django_db


def test_options_render_as_one_option_per_line():
    field = OptionsField(required=False)

    value = field.prepare_value(
        [
            {"id": "vegan", "label": "Vegan"},
            {"id": "veggie", "label": "Veggie"},
        ]
    )

    assert value == "vegan | Vegan\nveggie | Veggie"


def test_lines_parse_back_to_options():
    field = OptionsField(required=False)

    assert field.to_python("vegan | Vegan\nveggie | Veggie") == [
        {"id": "vegan", "label": "Vegan"},
        {"id": "veggie", "label": "Veggie"},
    ]


def test_a_bare_label_gets_a_slugified_id():
    field = OptionsField(required=False)

    assert field.to_python("No preference") == [
        {"id": "no-preference", "label": "No preference"}
    ]


def test_blank_lines_are_ignored():
    field = OptionsField(required=False)

    assert field.to_python("\nVegan\n\n  \nVeggie\n") == [
        {"id": "vegan", "label": "Vegan"},
        {"id": "veggie", "label": "Veggie"},
    ]


def test_labels_can_contain_pipes():
    field = OptionsField(required=False)

    assert field.to_python("both | One | Two") == [{"id": "both", "label": "One | Two"}]


def test_empty_input_means_no_options():
    field = OptionsField(required=False)

    assert field.to_python("") == []
    assert field.to_python(None) == []


def test_already_parsed_values_pass_through():
    # initial form data is the stored JSON list, not text
    field = OptionsField(required=False)

    options = [{"id": "vegan", "label": "Vegan"}]
    assert field.to_python(options) == options


def test_inline_form_saves_options_from_text():
    form = FormFactory()

    question_form = FormQuestionInlineForm(
        data={
            "form": form.pk,
            "label": "Diet",
            "question_type": FormQuestion.QuestionType.SELECT,
            "options": "Vegan\nVeggie",
            "order": 0,
            "active": "on",
        }
    )

    assert question_form.is_valid(), question_form.errors
    question = question_form.save()
    assert question.options == [
        {"id": "vegan", "label": "Vegan"},
        {"id": "veggie", "label": "Veggie"},
    ]


def test_inline_form_surfaces_duplicate_id_errors():
    form = FormFactory()

    question_form = FormQuestionInlineForm(
        data={
            "form": form.pk,
            "label": "Diet",
            "question_type": FormQuestion.QuestionType.SELECT,
            "options": "dup | One\ndup | Two",
            "order": 0,
            "active": "on",
        }
    )

    assert not question_form.is_valid()
    assert "options" in question_form.errors


def test_inline_form_rejects_options_on_text_questions():
    form = FormFactory()

    question_form = FormQuestionInlineForm(
        data={
            "form": form.pk,
            "label": "Why?",
            "question_type": FormQuestion.QuestionType.TEXT,
            "options": "Vegan",
            "order": 0,
            "active": "on",
        }
    )

    assert not question_form.is_valid()
    assert "options" in question_form.errors
