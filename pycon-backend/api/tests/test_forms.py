from api.forms import ContextAwareModelForm
from api.helpers.ids import encode_hashid
from api.voting.forms import HashidModelChoiceField
from django.forms import ValidationError
from pytest import mark, raises
from submissions.models import Submission
from users.models import User


def test_context_is_none_when_not_passed():
    class TestModelForm(ContextAwareModelForm):
        class Meta:
            model = User
            fields = ("id",)

    form = TestModelForm()
    assert not form.context


@mark.django_db
def test_hashid_model_choice_field(submission):
    field = HashidModelChoiceField(queryset=Submission.objects.all())
    assert field.to_python(submission.hashid) == submission


@mark.django_db
def test_hashid_model_choice_field_with_invalid_hashid():
    field = HashidModelChoiceField(queryset=Submission.objects.all())

    with raises(ValidationError) as e:
        field.to_python(encode_hashid(5))

    assert e.value.code == "invalid_choice"


@mark.django_db
def test_hashid_model_choice_field_with_empty_value():
    field = HashidModelChoiceField(queryset=Submission.objects.all())

    assert field.to_python(None) is None
    assert field.to_python("") is None
    assert field.to_python([]) is None
    assert field.to_python({}) is None
