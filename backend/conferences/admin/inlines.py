from django.contrib import admin
from django.core import exceptions
from django.forms import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _
from ordered_model.admin import (
    OrderedTabularInline,
)
from sponsors.models import SponsorLevel
from voting.models import IncludedEvent
from conferences.models import (
    Deadline,
    Duration,
)
from .forms import DeadlineForm


def validate_deadlines_form(forms):
    existing_types = set()
    for form in forms:
        if not form.cleaned_data:
            return

        start = form.cleaned_data["start"]
        end = form.cleaned_data["end"]
        delete = form.cleaned_data["DELETE"]

        if start > end:
            raise exceptions.ValidationError(_("Start date cannot be after end"))

        type = form.cleaned_data["type"]

        if type == Deadline.TYPES.custom or delete:
            continue

        if type in existing_types:
            raise exceptions.ValidationError(
                _("You can only have one deadline of type %(type)s") % {"type": type}
            )

        existing_types.add(type)


class DeadlineFormSet(BaseInlineFormSet):
    def clean(self):
        validate_deadlines_form(self.forms)


class DeadlineInline(admin.TabularInline):
    model = Deadline
    form = DeadlineForm
    formset = DeadlineFormSet


class DurationInline(admin.StackedInline):
    model = Duration
    filter_horizontal = ("allowed_submission_types",)


class SponsorLevelInline(OrderedTabularInline):
    model = SponsorLevel
    fields = ("name", "conference", "sponsors", "order", "move_up_down_links")
    readonly_fields = (
        "order",
        "move_up_down_links",
    )
    ordering = ("order",)
    extra = 1


class IncludedEventInline(admin.TabularInline):
    model = IncludedEvent
