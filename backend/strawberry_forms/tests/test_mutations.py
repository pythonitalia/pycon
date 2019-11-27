import strawberry
from django.forms import Form, IntegerField
from strawberry_forms.mutations import FormMutation


def test_form_mutation_without_context():
    class TestForm(Form):
        a = IntegerField()

        def save(self, *args, **kwargs):
            return "hello"

    class TestMutation(FormMutation):
        class Meta:
            form_class = TestForm

    @strawberry.input
    class TestInput:
        a: int

    assert TestMutation.Mutation(None, TestInput(a=1)) == "hello"


def test_form_mutation_response_can_be_converted_using_transform_method():
    class TestForm(Form):
        a = IntegerField()

        def save(self, *args, **kwargs):
            return "hello"

    class TestMutation(FormMutation):
        @classmethod
        def transform(cls, result):
            return "world"

        class Meta:
            form_class = TestForm

    @strawberry.input
    class TestInput:
        a: int

    assert TestMutation.Mutation(None, TestInput(a=1)) == "world"


def test_form_mutation_transform_is_not_required():
    class TestForm(Form):
        a = IntegerField()

        def save(self, *args, **kwargs):
            return "hello"

    class TestMutation(FormMutation):
        class Meta:
            form_class = TestForm

    @strawberry.input
    class TestInput:
        a: int

    assert TestMutation.Mutation(None, TestInput(a=1)) == "hello"


def test_mutation_without_input():
    class TestForm(Form):
        def save(self, *args, **kwargs):
            return "ciao"

    class TestMutation(FormMutation):
        class Meta:
            form_class = TestForm

    assert TestMutation.Mutation(None) == "ciao"
