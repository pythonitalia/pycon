import pytest

from conferences.tests.factories import ConferenceFactory
from generic_forms.models import Form, FormQuestion
from generic_forms.tests.factories import FormFactory, FormQuestionFactory

pytestmark = pytest.mark.django_db


def _query_form(graphql_client, conference, purpose="GRANT"):
    query = """query($code: String!, $purpose: FormPurpose!) {
        conference(code: $code) {
            form(purpose: $purpose) {
                id
                name
                questions {
                    id
                    label
                    description
                    questionType
                    required
                    maxLength
                    options {
                        id
                        label
                    }
                }
            }
        }
    }"""

    return graphql_client.query(
        query, variables={"code": conference.code, "purpose": purpose}
    )


def test_form_is_none_when_not_configured(graphql_client):
    conference = ConferenceFactory()

    result = _query_form(graphql_client, conference)

    assert result["data"]["conference"]["form"] is None


def test_form_is_none_when_only_another_purpose_is_configured(graphql_client):
    form = FormFactory(purpose=Form.Purpose.GENERIC)

    result = _query_form(graphql_client, form.conference, purpose="GRANT")

    assert result["data"]["conference"]["form"] is None


def test_form_belongs_to_the_requested_conference(graphql_client):
    FormFactory(purpose=Form.Purpose.GRANT, name="Other conference form")
    conference = ConferenceFactory()

    result = _query_form(graphql_client, conference)

    assert result["data"]["conference"]["form"] is None


def test_form_with_questions(graphql_client):
    form = FormFactory(purpose=Form.Purpose.GRANT, name="Grant form")
    question = FormQuestionFactory(
        form=form,
        label="Why do you want to attend?",
        description="Tell us more",
        question_type=FormQuestion.QuestionType.TEXTAREA,
        required=True,
        max_length=500,
        order=0,
    )

    result = _query_form(graphql_client, form.conference)

    data = result["data"]["conference"]["form"]
    assert data["id"] == str(form.id)
    assert data["name"] == "Grant form"
    assert data["questions"] == [
        {
            "id": str(question.id),
            "label": "Why do you want to attend?",
            "description": "Tell us more",
            "questionType": "TEXTAREA",
            "required": True,
            "maxLength": 500,
            "options": [],
        }
    ]


def test_select_question_options_are_exposed(graphql_client):
    form = FormFactory(purpose=Form.Purpose.GRANT)
    FormQuestionFactory(
        form=form,
        question_type=FormQuestion.QuestionType.SELECT,
        options=[
            {"id": "vegan", "label": "Vegan"},
            {"id": "veggie", "label": "Veggie"},
        ],
    )

    result = _query_form(graphql_client, form.conference)

    assert result["data"]["conference"]["form"]["questions"][0]["options"] == [
        {"id": "vegan", "label": "Vegan"},
        {"id": "veggie", "label": "Veggie"},
    ]


def test_questions_follow_the_configured_order(graphql_client):
    form = FormFactory(purpose=Form.Purpose.GRANT)
    second = FormQuestionFactory(form=form, order=1)
    first = FormQuestionFactory(form=form, order=0)
    third = FormQuestionFactory(form=form, order=2)

    result = _query_form(graphql_client, form.conference)

    ids = [q["id"] for q in result["data"]["conference"]["form"]["questions"]]
    assert ids == [str(first.id), str(second.id), str(third.id)]


def test_inactive_questions_are_hidden(graphql_client):
    form = FormFactory(purpose=Form.Purpose.GRANT)
    active = FormQuestionFactory(form=form, active=True)
    FormQuestionFactory(form=form, active=False)

    result = _query_form(graphql_client, form.conference)

    ids = [q["id"] for q in result["data"]["conference"]["form"]["questions"]]
    assert ids == [str(active.id)]
