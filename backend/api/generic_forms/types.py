import strawberry

from api.context import Info
from generic_forms.models import Form as FormModel
from generic_forms.models import FormQuestion as FormQuestionModel

FormPurpose = strawberry.enum(FormModel.Purpose, name="FormPurpose")
FormQuestionType = strawberry.enum(
    FormQuestionModel.QuestionType, name="FormQuestionType"
)


@strawberry.type
class FormQuestionOption:
    id: str
    label: str


@strawberry.type
class FormQuestion:
    id: strawberry.ID
    label: str
    description: str
    question_type: FormQuestionType
    required: bool
    max_length: int | None

    @strawberry.field
    def options(self, info: Info) -> list[FormQuestionOption]:
        return [
            FormQuestionOption(id=option["id"], label=option["label"])
            for option in self.options
        ]


@strawberry.type
class Form:
    id: strawberry.ID
    name: str

    @strawberry.field
    def questions(self, info: Info) -> list[FormQuestion]:
        return self.questions.filter(active=True)
