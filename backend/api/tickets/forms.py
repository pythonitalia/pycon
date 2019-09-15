from api.forms import ContextAwareModelForm
from conferences.models import TicketFareQuestion
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _
from tickets.models import Ticket, UserAnswer


class SendQuestionAnswerForm(ContextAwareModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context:
            self.fields["ticket"].queryset = Ticket.objects.filter(
                user=self.context["request"].user
            )

    def _get_validation_exclusions(self):
        # We manually make sure we do not create duplicates
        # of the same answer by updating the one that already
        # exists.

        return super()._get_validation_exclusions() + ["ticket"]

    def clean(self):
        cleaned_data = super().clean()

        question = cleaned_data.get("question")
        ticket = cleaned_data.get("ticket")

        if not ticket:
            return cleaned_data

        try:
            question_info = ticket.ticket_fare.questions.get(question_id=question.id)
        except TicketFareQuestion.DoesNotExist:
            raise ValidationError({"question": _("Question not allowed")})

        answer = cleaned_data.get("answer")

        if not answer and question_info.is_required:
            raise ValidationError({"answer": _("This question cannot be left blank")})

        return cleaned_data

    def save(self, commit=True):
        question = self.cleaned_data.get("question")
        ticket = self.cleaned_data.get("ticket")

        try:
            self.instance = UserAnswer.objects.get(ticket=ticket, question=question)
        except UserAnswer.DoesNotExist:
            pass

        self.instance.user = self.context["request"].user
        self.instance.answer = self.cleaned_data["answer"]
        return super().save(commit=commit)

    class Meta:
        model = UserAnswer
        fields = ("ticket", "question", "answer")
