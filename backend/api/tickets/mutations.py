import strawberry
from strawberry_forms.mutations import FormMutation

from .forms import SendQuestionAnswerForm
from .types import UserAnswer


class SendQuestionAnswer(FormMutation):
    @classmethod
    def transform(cls, result):
        return UserAnswer(question=result.question, answer=result.answer)

    class Meta:
        form_class = SendQuestionAnswerForm
        output_types = (UserAnswer,)


@strawberry.type
class TicketsMutations:
    send_question_answer = SendQuestionAnswer.Mutation
