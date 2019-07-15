from django import forms
from graphene_form.mutations import FormMutation


def test_mutation_with_generic_form_errors():
    class ErrorsForm(forms.Form):
        def clean(self):
            raise forms.ValidationError("generic error")

    class TestMutation(FormMutation):
        class Meta:
            form_class = ErrorsForm

    output = TestMutation().mutate(None, None, {})

    assert type(output) == TestMutation._meta.error_type

    assert output.nonFieldErrors
    assert output.nonFieldErrors == ["generic error"]
