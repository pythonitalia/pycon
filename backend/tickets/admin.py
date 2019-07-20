from django.contrib import admin

from tickets import QUESTION_TYPE_TEXT, QUESTION_TYPE_CHOICE
from tickets.models import Ticket, TicketQuestion, TicketQuestionChoices, UserAnswer


class UserAnswersInline(admin.TabularInline):
    model = UserAnswer
    fields = ("question", "user_answer")
    readonly_fields = ("question", "user_answer")

    can_delete = False

    def question(self, instance):
        return instance.answer.question

    question.short_description = "Question"

    def user_answer(self, instance):
        q_type = instance.question.question_type
        if q_type == QUESTION_TYPE_TEXT:
            return instance.answer_text
        if q_type == QUESTION_TYPE_CHOICE:
            return instance.answer_choice.choice
        else:
            return "Error: malformed answer"

    user_answer.short_description = "Answer"

    def has_add_permission(self, request):
        return False


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_fare_name", "user_email")
    search_filters = ("user__email", "conference__code")
    inlines = [UserAnswersInline]

    def ticket_fare_name(self, obj):
        return obj.ticket_fare.name

    def user_email(self, obj):
        return obj.user.email


class TicketQuestionChoicesInline(admin.TabularInline):
    model = TicketQuestionChoices


@admin.register(TicketQuestion)
class TicketQuestionAdmin(admin.ModelAdmin):
    inlines = [TicketQuestionChoicesInline]
