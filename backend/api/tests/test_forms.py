from api.forms import ContextAwareModelForm
from users.models import User


def test_context_is_none_when_not_passed():
    class TestModelForm(ContextAwareModelForm):
        class Meta:
            model = User
            fields = ("id",)

    form = TestModelForm()
    assert not form.context
