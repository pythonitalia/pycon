from django.contrib import admin

from tickets.models import Ticket, TicketQuestion, TicketQuestionChoices, UserAnswer


class UserAnswersInline(admin.TabularInline):
    model = UserAnswer
    fields = ('question', 'answer_choice')
    readonly_fields = ('question', 'answer_choice')
    can_delete = False

    def question(self, instance):
        return instance.answer.question
    question.short_description = 'Question'

    def answer_choice(self, instance):
        return instance.answer.choice
    answer_choice.short_description = 'Answer'

    def has_add_permission(self, request):
        return False

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_fare_name', 'user_email')
    search_filters = ('user__email', 'conference__code',)
    inlines = [UserAnswersInline, ]

    def ticket_fare_name(self, obj):
        return obj.ticket_fare.name

    def user_email(self, obj):
        return obj.user.email


class TicketQuestionChoicesInline(admin.TabularInline):
    model = TicketQuestionChoices


@admin.register(TicketQuestion)
class TicketQuestionAdmin(admin.ModelAdmin):
    inlines = [TicketQuestionChoicesInline]
