from datetime import timedelta
from uuid import uuid4

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.template.response import TemplateResponse

from conferences.models import Conference
from conferences.tasks import send_conference_voucher_email
from conferences.workflows import CLONE_CONFERENCE
from custom_admin.admin import validate_single_conference_selection
from pretix import create_voucher
from pycon.resonate_app import start_workflow


@admin.action(description="Send voucher via email")
@validate_single_conference_selection
def send_voucher_via_email(modeladmin, request, queryset):
    count = 0
    for conference_voucher in queryset.filter(pretix_voucher_id__isnull=False):
        send_conference_voucher_email.delay(conference_voucher_id=conference_voucher.id)
        count = count + 1

    messages.success(request, f"{count} Voucher emails scheduled!")


@admin.action(description="Create vouchers on Pretix")
@validate_single_conference_selection
def create_conference_vouchers_on_pretix(modeladmin, request, queryset):
    conference = queryset.only("conference_id").first().conference

    if not conference.pretix_conference_voucher_quota_id:
        messages.error(
            request,
            "Please configure the conference voucher quota ID in the conference settings",
        )
        return

    count = 0

    for conference_voucher in queryset.filter(pretix_voucher_id__isnull=True):
        price_mode, value = conference_voucher.get_voucher_configuration()

        pretix_voucher = create_voucher(
            conference=conference_voucher.conference,
            code=conference_voucher.voucher_code,
            comment=f"Voucher for user_id={conference_voucher.user_id}",
            tag=conference_voucher.voucher_type,
            quota_id=conference_voucher.conference.pretix_conference_voucher_quota_id,
            price_mode=price_mode,
            value=value,
        )

        pretix_voucher_id = pretix_voucher["id"]
        conference_voucher.pretix_voucher_id = pretix_voucher_id
        conference_voucher.save()
        count = count + 1

    messages.success(request, f"{count} Vouchers created on Pretix!")


class CloneConferenceForm(forms.Form):
    """What the new conference overrides; everything else comes from the base one."""

    code = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    hostname = forms.CharField(max_length=255)
    start = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())
    end = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())

    def clean_code(self):
        code = self.cleaned_data["code"]

        if Conference.objects.filter(code=code).exists():
            raise ValidationError(f"Conference {code} already exists")

        return code

    def clean_hostname(self):
        hostname = self.cleaned_data["hostname"]

        if Conference.objects.filter(hostname=hostname).exists():
            raise ValidationError(f"Hostname {hostname} is already used")

        return hostname

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")

        if start and end and start > end:
            raise ValidationError("Start date cannot be after end")

        return cleaned_data


def next_edition_defaults(conference: Conference) -> dict:
    """Prefill the form with the next edition: same values, one year later."""
    year = conference.start.year if conference.start else None

    def bump_year(value: str) -> str:
        if not year or str(year) not in value:
            return value

        return value.replace(str(year), str(year + 1), 1)

    def next_year(value):
        if not value:
            return value

        try:
            return value.replace(year=value.year + 1)
        except ValueError:
            # 29th of February: the next edition has no such day.
            return value + timedelta(days=365)

    return {
        "code": bump_year(conference.code),
        "name": bump_year(str(conference.name)),
        "hostname": bump_year(conference.hostname),
        "start": next_year(conference.start),
        "end": next_year(conference.end),
    }


@admin.action(description="Create new conference using this one as base")
def clone_conference(modeladmin, request, queryset):
    if queryset.count() != 1:
        messages.error(request, "Select the single conference to use as base")
        return None

    source = queryset.get()

    if request.POST.get("apply"):
        form = CloneConferenceForm(request.POST)

        if form.is_valid():
            return start_clone_conference(request, source, form.cleaned_data)
    else:
        form = CloneConferenceForm(initial=next_edition_defaults(source))

    return TemplateResponse(
        request,
        "admin/conferences/clone_conference.html",
        {
            **modeladmin.admin_site.each_context(request),
            "title": f"New conference based on {source.code}",
            "opts": modeladmin.model._meta,
            "media": modeladmin.media + form.media,
            "source": source,
            "form": form,
            "action_name": "clone_conference",
            "selected": [str(source.pk)],
        },
    )


def start_clone_conference(request, source: Conference, data: dict) -> None:
    # A fresh id per submission, so a run that failed for good can be started
    # again. Double submits are harmless anyway: every step of the workflow
    # only creates what is not there yet.
    workflow_id = f"clone-conference-{data['code']}-{uuid4().hex[:8]}"

    start_workflow(
        CLONE_CONFERENCE,
        workflow_id,
        source_code=source.code,
        new_code=data["code"],
        new_name=data["name"],
        new_start=data["start"].isoformat(),
        new_end=data["end"].isoformat(),
        new_hostname=data["hostname"],
    )

    messages.success(
        request,
        f"Creating {data['code']} based on {source.code}. "
        f"Follow the progress in Resonate (workflow {workflow_id}).",
    )

    return None
