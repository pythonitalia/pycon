import pytest
from strawberry_forms.forms import FormWithContext


def test_using_form_context_without_creating_it():
    form = FormWithContext()

    with pytest.raises(ValueError) as e:
        form.context

    assert "Make sure you pass the context when instancing the Form" in str(e.value)
