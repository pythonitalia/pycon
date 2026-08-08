from django.contrib import admin

from generic_forms.models import Form, FormAnswer, FormQuestion


class FormQuestionInline(admin.TabularInline):
    model = FormQuestion
    extra = 1
    fields = (
        "label",
        "description",
        "question_type",
        "options",
        "required",
        "max_length",
        "order",
        "active",
    )

    # Freezing of question_type/options/required on answered forms is
    # enforced by FormQuestion.clean(), which surfaces as a normal form
    # error here. Inline-level readonly would also freeze NEW rows, and
    # adding questions to an answered form must stay possible.

    def has_delete_permission(self, request, obj=None):
        if obj and obj.answers.exists():
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", "purpose")
    list_filter = ("conference", "purpose")
    search_fields = ("name",)
    inlines = [FormQuestionInline]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.answers.exists():
            return ("conference", "purpose")
        return ()


@admin.register(FormAnswer)
class FormAnswerAdmin(admin.ModelAdmin):
    list_display = ("form", "user", "created")
    list_filter = ("form__conference", "form__purpose")
    # Form.__str__ renders the conference name
    list_select_related = ("form__conference", "user")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        # deleting answers would unfreeze the form's questions and silently
        # destroy an applicant's submission
        return False
