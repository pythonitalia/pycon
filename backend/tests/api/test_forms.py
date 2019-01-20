import pytest

from api.forms import ContextAwareForm

from users.models import User


def test_cannot_use_form_context_if_its_not_passed():
    class TestModelForm(ContextAwareForm):
        class Meta:
            model = User
            fields = ('id',)

    form = TestModelForm()

    with pytest.raises(ValueError) as e:
        form.context

    assert str(e.value) == 'Make sure you pass the context when instancing the Form'
