import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from generic_forms.models import Form, FormQuestion
from generic_forms.services import wrap_answers
from generic_forms.tests.factories import (
    FormAnswerFactory,
    FormFactory,
    FormQuestionFactory,
)
from grants.tests.factories import GrantFactory
from reviews.adapters import GrantsReviewAdapter
from reviews.tests.factories import ReviewSessionFactory
from users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def _review_context(grant):
    review_session = ReviewSessionFactory(
        session_type="grants", conference=grant.conference
    )
    request = RequestFactory().get("/")
    request.user = UserFactory(is_staff=True, is_superuser=True)

    return GrantsReviewAdapter().get_review_context(
        request,
        review_session,
        grant.id,
        None,
        AdminSite(),
    )


def test_review_context_includes_dynamic_answers():
    grant = GrantFactory()
    form = FormFactory(conference=grant.conference, purpose=Form.Purpose.GRANT)
    why = FormQuestionFactory(
        form=form,
        label="Why do you need it?",
        question_type=FormQuestion.QuestionType.TEXTAREA,
        order=0,
    )
    diet = FormQuestionFactory(
        form=form,
        label="Diet",
        question_type=FormQuestion.QuestionType.SELECT,
        options=[{"id": "vegan", "label": "Vegan"}],
        order=1,
    )
    grant.form_answer = FormAnswerFactory(
        form=form,
        user=grant.user,
        answers=wrap_answers({str(why.pk): "My motivation", str(diet.pk): "vegan"}),
    )
    grant.save()

    context = _review_context(grant)

    assert context["grant_answers"] == [
        ("Why do you need it?", "My motivation"),
        ("Diet", "Vegan"),
    ]


def test_review_context_has_no_answers_for_legacy_grants():
    grant = GrantFactory()

    context = _review_context(grant)

    assert context["grant_answers"] == []
