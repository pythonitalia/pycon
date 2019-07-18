from django.contrib import admin
from tickets.models import Ticket, TicketQuestion, TicketQuestionChoice, UserAnswer
from tickets.graphs import render_graph

class UserAnswersInline(admin.TabularInline):
    model = UserAnswer
    fields = ("question", "answer")
    readonly_fields = ("question", "answer")

    can_delete = False

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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['some_var'] = 'This is what I want to show'
        js, resources, tag = render_graph()
        extra_context['js'] = js
        extra_context['resources'] = resources
        extra_context['tag'] = tag
        return super(TicketAdmin, self).changelist_view(request,
                                                        extra_context=extra_context)


class TicketQuestionChoiceInline(admin.TabularInline):
    model = TicketQuestionChoice


@admin.register(TicketQuestion)
class TicketQuestionAdmin(admin.ModelAdmin):
    inlines = [TicketQuestionChoiceInline]
