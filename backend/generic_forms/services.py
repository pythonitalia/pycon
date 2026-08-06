from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from generic_forms.models import Form, FormQuestion

ANSWERS_VERSION = 1

_validate_url = URLValidator()


def wrap_answers(answers: dict) -> dict:
    return {"version": ANSWERS_VERSION, "answers": answers}


def unwrap_answers(envelope: dict) -> dict:
    if not isinstance(envelope, dict):
        raise ValueError("Malformed answers envelope.")
    if not envelope:
        # a FormAnswer created without going through wrap_answers
        return {}
    version = envelope.get("version")
    if version != ANSWERS_VERSION:
        raise ValueError(f"Unknown answers version: {version}")
    answers = envelope.get("answers")
    if not isinstance(answers, dict):
        raise ValueError("Malformed answers envelope: missing answers map.")
    return answers


def validate_answers(form: Form, answers: dict) -> dict[str, list[str]]:
    """Validate a flat {question_id: value} map against the form's active
    questions. Returns {question_id: [error messages]}; empty dict when valid.
    """
    if not isinstance(answers, dict):
        return {"__all__": ["Invalid answers format."]}

    errors: dict[str, list[str]] = {}
    questions = {
        str(question.pk): question for question in form.questions.filter(active=True)
    }

    for question_id in answers:
        if question_id not in questions:
            errors[question_id] = ["Unknown or inactive question."]

    for question_id, question in questions.items():
        value = answers.get(question_id)

        if value is None or value == "" or value == []:
            if question.required:
                errors[question_id] = ["This question is required."]
            continue

        messages = _validate_value(question, value)
        if messages:
            errors[question_id] = messages

    return errors


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
                _validate_url(value)
            except ValidationError:
                return ["Invalid URL."]
        return []

    if question_type == types.SELECT:
        if not isinstance(value, str) or value not in _option_ids(question):
            return ["Invalid option."]
        return []

    if question_type == types.MULTI_SELECT:
        if not isinstance(value, list) or not all(
            isinstance(item, str) for item in value
        ):
            return ["Invalid value: expected a list of option ids."]
        invalid = [item for item in value if item not in _option_ids(question)]
        if invalid:
            return [f"Invalid options: {', '.join(invalid)}."]
        return []

    if question_type == types.BOOLEAN:
        if not isinstance(value, bool):
            return ["Invalid value: expected true or false."]
        return []

    return ["Unknown question type."]


def _option_ids(question: FormQuestion) -> set[str]:
    return {option["id"] for option in question.options}


def display_answer_value(question: FormQuestion | None, value) -> str:
    """Human-readable rendering of a stored answer value (admin, exports)."""
    if value is None:
        return ""
    if question is None:
        return str(value)

    types = FormQuestion.QuestionType
    if question.question_type == types.BOOLEAN:
        return "Yes" if value else "No"

    option_labels = {option["id"]: option["label"] for option in question.options}
    if question.question_type == types.SELECT:
        return option_labels.get(value, str(value))
    if question.question_type == types.MULTI_SELECT:
        return ", ".join(option_labels.get(item, str(item)) for item in value)

    return str(value)


def display_answers(form_answer) -> list[tuple[str, str]]:
    """(question label, human-readable value) pairs for the answered
    questions, in question order. Answers to questions that no longer exist
    are appended as "Question <id>".
    """
    # copy: unwrap returns the stored dict and we pop from it below
    answers = dict(unwrap_answers(form_answer.answers))
    pairs = []

    for question in form_answer.form.questions.all():
        question_id = str(question.pk)
        if question_id in answers:
            value = display_answer_value(question, answers.pop(question_id))
            pairs.append((question.label, value))

    for question_id, value in answers.items():
        pairs.append((f"Question {question_id}", display_answer_value(None, value)))

    return pairs
