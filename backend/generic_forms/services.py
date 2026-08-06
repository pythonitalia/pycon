from collections import defaultdict

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from generic_forms.models import Form, FormQuestion

ANSWERS_VERSION = 1


def wrap_answers(answers: dict) -> dict:
    return {"version": ANSWERS_VERSION, "answers": answers}


def unwrap_answers(envelope: dict) -> dict:
    version = envelope.get("version")
    if version != ANSWERS_VERSION:
        raise ValueError(f"Unknown answers version: {version}")
    return envelope["answers"]


def validate_answers(form: Form, answers: dict) -> dict[str, list[str]]:
    """Validate a flat {question_id: value} map against the form's active
    questions. Returns {question_id: [error messages]}; empty dict when valid.
    """
    errors: dict[str, list[str]] = defaultdict(list)
    questions = {
        str(question.pk): question for question in form.questions.filter(active=True)
    }

    for question_id in answers:
        if question_id not in questions:
            errors[question_id].append("Unknown or inactive question.")

    for question_id, question in questions.items():
        value = answers.get(question_id)

        if value is None or value == "" or value == []:
            if question.required:
                errors[question_id].append("This question is required.")
            continue

        errors[question_id].extend(_validate_value(question, value))

    return {
        question_id: messages for question_id, messages in errors.items() if messages
    }


def _validate_value(question: FormQuestion, value) -> list[str]:
    question_type = question.question_type
    types = FormQuestion.QuestionType

    if question_type in (types.TEXT, types.TEXTAREA, types.URL):
        if not isinstance(value, str):
            return ["Invalid value: expected text."]
        if question.max_length and len(value) > question.max_length:
            return [f"Cannot be longer than {question.max_length} characters."]
        if question_type == types.URL:
            try:
                URLValidator()(value)
            except ValidationError:
                return ["Invalid URL."]
        return []

    if question_type == types.SELECT:
        if not isinstance(value, str) or value not in _option_ids(question):
            return ["Invalid option."]
        return []

    if question_type == types.MULTI_SELECT:
        if not isinstance(value, list):
            return ["Invalid value: expected a list of options."]
        invalid = [item for item in value if item not in _option_ids(question)]
        if invalid:
            return ["Invalid options: " + ", ".join(map(str, invalid)) + "."]
        return []

    if question_type == types.BOOLEAN:
        if not isinstance(value, bool):
            return ["Invalid value: expected true or false."]
        return []

    return ["Unknown question type."]


def _option_ids(question: FormQuestion) -> set[str]:
    return {option["id"] for option in question.options}
