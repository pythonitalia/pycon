import pytest
from django.contrib.admin.sites import site
from django.test import RequestFactory

from generic_forms.admin import FormAnswerAdmin, FormQuestionInline
from generic_forms.models import Form, FormAnswer
from generic_forms.tests.factories import FormAnswerFactory, FormFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_request(admin_superuser):
    request = RequestFactory().get("/")
    request.user = admin_superuser
    return request


def test_form_and_form_answer_are_registered():
    assert site.is_registered(Form)
    assert site.is_registered(FormAnswer)


def test_questions_cannot_be_deleted_from_an_answered_form(admin_request):
    answer = FormAnswerFactory()
    inline = FormQuestionInline(Form, site)

    assert inline.has_delete_permission(admin_request, answer.form) is False


def test_questions_can_be_deleted_from_an_unanswered_form(admin_request):
    form = FormFactory()
    inline = FormQuestionInline(Form, site)

    assert inline.has_delete_permission(admin_request, form) is True


def test_form_answers_are_read_only_in_admin(admin_request):
    answer_admin = FormAnswerAdmin(FormAnswer, site)

    assert answer_admin.has_add_permission(admin_request) is False
    assert answer_admin.has_change_permission(admin_request) is False
    assert (
        answer_admin.has_change_permission(admin_request, FormAnswerFactory()) is False
    )
