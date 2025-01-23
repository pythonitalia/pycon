from django.db import transaction
from custom_admin.audit import (
    create_addition_admin_log_entry,
    create_change_admin_log_entry,
)
from conferences.models.conference_voucher import ConferenceVoucher
from pycon.constants import UTC
from custom_admin.admin import (
    confirm_pending_status,
    reset_pending_status_back_to_status,
    validate_single_conference_selection,
)
from import_export.resources import ModelResource
from datetime import timedelta
from typing import Dict, List, Optional
from countries.filters import CountryFilter
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.utils import timezone
from import_export.admin import ExportMixin
from import_export.fields import Field
from users.admin_mixins import ConferencePermissionMixin
from countries import countries
from grants.tasks import (
    send_grant_reply_approved_email,
    send_grant_reply_waiting_list_email,
    send_grant_reply_waiting_list_update_email,
    send_grant_reply_rejected_email,
)
from schedule.models import ScheduleItem
from submissions.models import Submission
from .models import Grant, GrantConfirmPendingStatusProxy
from django.db.models import Exists, OuterRef, F

from django.contrib.admin import SimpleListFilter
from participants.models import Participant
from django.urls import reverse
from django.utils.safestring import mark_safe

EXPORT_GRANTS_FIELDS = (
    "name",
    "full_name",
    "gender",
    "occupation",
    "grant_type",
    "python_usage",
    "been_to_other_events",
    "needs_funds_for_travel",
    "why",
    "notes",
    "departure_country",
    "conference__code",
    "created",
)


class GrantResource(ModelResource):
    search_field = "user_id"
    age_group = Field()
    email = Field()
    has_sent_submission = Field()
    submission_title = Field()
    submission_tags = Field()
    submission_admin_link = Field()
    submission_pycon_link = Field()
    grant_admin_link = Field()
    USERS_SUBMISSIONS: Dict[int, List[Submission]] = {}

    def dehydrate_email(self, obj: Grant):
        if obj.user_id:
            return obj.user.email

        # old grants have email in the model.
        return obj.email

    def dehydrate_age_group(self, obj: Grant):
        if not obj.age_group:
            return ""

        return Grant.AgeGroup(obj.age_group).label

    def dehydrate_has_sent_submission(self, obj: Grant) -> str:
        return "TRUE" if obj.user_id in self.USERS_SUBMISSIONS else "FALSE"

    def _get_submissions(self, obj: Grant) -> Optional[List[Submission]]:
        if not obj.user_id:
            return

        return self.USERS_SUBMISSIONS.get(obj.user_id)

    def dehydrate_submission_title(self, obj: Grant):
        submissions = self._get_submissions(obj)
        if not submissions:
            return

        return "\n".join([s.title.localize("en") for s in submissions])

    def dehydrate_submission_tags(self, obj: Grant):
        submissions = self._get_submissions(obj)
        if not submissions:
            return

        return "\n".join(
            [
                ", ".join(
                    [
                        f"{r.tag.name}: {r.rank} / {r.total_submissions_per_tag}"
                        for r in s.rankings.all()
                    ]
                )
                for s in submissions
            ]
        )

    def dehydrate_submission_pycon_link(self, obj):
        submissions = self.USERS_SUBMISSIONS.get(obj.user_id)
        if not submissions:
            return
        return "\n".join(
            [f"https://pycon.it/submission/{s.hashid}" for s in submissions]
        )

    def dehydrate_submission_admin_link(self, obj):
        submissions = self.USERS_SUBMISSIONS.get(obj.user_id)
        if not submissions:
            return
        return "\n".join(
            [
                f"https://admin.pycon.it/admin/submissions/submission/{s.id}/change/"
                for s in submissions
            ]
        )

    def dehydrate_grant_admin_link(self, obj: Grant):
        return f"https://admin.pycon.it/admin/grants/grant/?q={'+'.join(obj.full_name.split(' '))}"  # noqa: E501

    def before_export(self, queryset: QuerySet, *args, **kwargs):
        super().before_export(queryset, *args, **kwargs)
        conference_id = queryset.values_list("conference_id").first()

        submissions = Submission.objects.prefetch_related(
            "rankings__tag", "rankings__submission"
        ).filter(
            speaker_id__in=queryset.values_list("user_id", flat=True),
            conference_id=conference_id,
        )

        self.USERS_SUBMISSIONS = {}
        for submission in submissions:
            self.USERS_SUBMISSIONS.setdefault(submission.speaker_id, [])
            self.USERS_SUBMISSIONS[submission.speaker_id].append(submission)

        return queryset

    class Meta:
        model = Grant
        fields = EXPORT_GRANTS_FIELDS
        export_order = EXPORT_GRANTS_FIELDS


def _check_amounts_are_not_empty(grant: Grant, request):
    if grant.total_amount is None:
        messages.error(
            request,
            f"Grant for {grant.name} is missing 'Total Amount'!",
        )
        return False

    if grant.has_approved_accommodation() and grant.accommodation_amount is None:
        messages.error(
            request,
            f"Grant for {grant.name} is missing 'Accommodation Amount'!",
        )
        return False

    if grant.has_approved_travel() and grant.travel_amount is None:
        messages.error(
            request,
            f"Grant for {grant.name} is missing 'Travel Amount'!",
        )
        return False

    return True


@admin.action(description="Send Approved/Waiting List/Rejected reply emails")
@validate_single_conference_selection
def send_reply_emails(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(
            Grant.Status.approved,
            Grant.Status.waiting_list,
            Grant.Status.waiting_list_maybe,
            Grant.Status.rejected,
        ),
    )

    if not queryset:
        messages.add_message(
            request, messages.WARNING, "No grants found in the selection"
        )
        return

    for grant in queryset:
        if grant.status in (Grant.Status.approved,):
            if grant.approved_type is None:
                messages.error(
                    request,
                    f"Grant for {grant.name} is missing 'Grant Approved Type'!",
                )
                return

            if not _check_amounts_are_not_empty(grant, request):
                return

            now = timezone.now()
            grant.applicant_reply_deadline = timezone.datetime(
                now.year, now.month, now.day, 23, 59, 59, tzinfo=UTC
            ) + timedelta(days=14)
            grant.save()
            send_grant_reply_approved_email.delay(grant_id=grant.id, is_reminder=False)

            messages.info(request, f"Sent Approved reply email to {grant.name}")

        if (
            grant.status == Grant.Status.waiting_list
            or grant.status == Grant.Status.waiting_list_maybe
        ):
            send_grant_reply_waiting_list_email.delay(grant_id=grant.id)
            messages.info(request, f"Sent Waiting List reply email to {grant.name}")

        if grant.status == Grant.Status.rejected:
            send_grant_reply_rejected_email.delay(grant_id=grant.id)
            messages.info(request, f"Sent Rejected reply email to {grant.name}")


@admin.action(description="Send reminder to waiting confirmation grants")
@validate_single_conference_selection
def send_grant_reminder_to_waiting_for_confirmation(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(Grant.Status.waiting_for_confirmation,),
    )

    for grant in queryset:
        if not grant.grant_type:
            messages.add_message(
                request,
                messages.ERROR,
                f"Grant for {grant.name} is missing 'Grant Approved Type'!",
            )
            return

        _check_amounts_are_not_empty(grant, request)

        send_grant_reply_approved_email.delay(grant_id=grant.id, is_reminder=True)

        messages.info(request, f"Grant reminder sent to {grant.name}")


@admin.action(description="Send Waiting List update email")
@validate_single_conference_selection
def send_reply_email_waiting_list_update(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(
            Grant.Status.waiting_list,
            Grant.Status.waiting_list_maybe,
        ),
    )

    for grant in queryset:
        send_grant_reply_waiting_list_update_email.delay(grant_id=grant.id)
        messages.info(request, f"Sent Waiting List update reply email to {grant.name}")


@admin.action(description="Create grant vouchers")
@validate_single_conference_selection
@transaction.atomic
def create_grant_vouchers(modeladmin, request, queryset):
    conference = queryset.first().conference
    existing_vouchers_by_user_id = {
        voucher.user_id: voucher
        for voucher in ConferenceVoucher.objects.for_conference(conference).filter(
            user_id__in=queryset.values_list("user_id", flat=True),
        )
    }

    vouchers_to_create = []
    vouchers_to_update = []

    for grant in queryset.order_by("id"):
        if grant.status != Grant.Status.confirmed:
            messages.error(
                request,
                f"Grant for {grant.name} is not confirmed, "
                "we can't generate voucher for it.",
            )
            continue

        existing_voucher = existing_vouchers_by_user_id.get(grant.user_id)

        if not existing_voucher:
            create_addition_admin_log_entry(
                request.user,
                grant,
                change_message="Created voucher for this grant",
            )

            vouchers_to_create.append(
                ConferenceVoucher(
                    conference_id=grant.conference_id,
                    user_id=grant.user_id,
                    voucher_code=ConferenceVoucher.generate_code(),
                    voucher_type=ConferenceVoucher.VoucherType.GRANT,
                )
            )
            continue

        if existing_voucher.voucher_type == ConferenceVoucher.VoucherType.CO_SPEAKER:
            messages.warning(
                request,
                f"Grant for {grant.name} already has a Co-Speaker voucher. Upgrading to a Grant voucher.",
            )
            create_change_admin_log_entry(
                request.user,
                existing_voucher,
                change_message="Upgraded Co-Speaker voucher to Grant voucher",
            )
            create_change_admin_log_entry(
                request.user,
                grant,
                change_message="Updated existing Co-Speaker voucher to grant",
            )
            existing_voucher.voucher_type = ConferenceVoucher.VoucherType.GRANT
            vouchers_to_update.append(existing_voucher)

    ConferenceVoucher.objects.bulk_create(vouchers_to_create, ignore_conflicts=True)
    ConferenceVoucher.objects.bulk_update(vouchers_to_update, ["voucher_type"])

    messages.success(request, "Vouchers created!")


@admin.action(description="Mark grants as Rejected and send email")
@validate_single_conference_selection
def mark_rejected_and_send_email(modeladmin, request, queryset):
    queryset = queryset.filter(
        status__in=(
            Grant.Status.waiting_list,
            Grant.Status.waiting_list_maybe,
        ),
    )

    for grant in queryset:
        grant.status = Grant.Status.rejected
        grant.save()

        send_grant_reply_rejected_email.delay(grant_id=grant.id)
        messages.info(request, f"Sent Rejected reply email to {grant.name}")


class IsProposedSpeakerFilter(SimpleListFilter):
    title = "Is Proposed Speaker"
    parameter_name = "is_proposed_speaker"

    def lookups(self, request, model_admin):
        return (
            (True, "Yes"),
            (False, "No"),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(is_proposed_speaker=self.value())
        return queryset


class IsConfirmedSpeakerFilter(SimpleListFilter):
    title = "Is Confirmed Speaker"
    parameter_name = "is_confirmed_speaker"

    def lookups(self, request, model_admin):
        return (
            (True, "Yes"),
            (False, "No"),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(is_confirmed_speaker=self.value())
        return queryset


@admin.register(Grant)
class GrantAdmin(ExportMixin, ConferencePermissionMixin, admin.ModelAdmin):
    change_list_template = "admin/grants/grant/change_list.html"
    resource_class = GrantResource
    list_display = (
        "user_display_name",
        "country",
        "is_proposed_speaker",
        "is_confirmed_speaker",
        "emoji_gender",
        "conference",
        "status",
        "approved_type",
        "ticket_amount",
        "travel_amount",
        "accommodation_amount",
        "total_amount",
        "country_type",
        "applicant_reply_sent_at",
        "applicant_reply_deadline",
        "voucher_code",
        "voucher_email_sent_at",
        "created",
    )
    list_filter = (
        "conference",
        "status",
        "country_type",
        "occupation",
        "approved_type",
        "needs_funds_for_travel",
        "need_visa",
        "need_accommodation",
        IsProposedSpeakerFilter,
        IsConfirmedSpeakerFilter,
        ("departure_country", CountryFilter),
        "user__gender",
    )
    search_fields = (
        "email",
        "full_name",
        "departure_country",
        "been_to_other_events",
        "why",
        "notes",
    )
    actions = [
        send_reply_emails,
        send_grant_reminder_to_waiting_for_confirmation,
        send_reply_email_waiting_list_update,
        create_grant_vouchers,
        mark_rejected_and_send_email,
        "delete_selected",
    ]
    autocomplete_fields = ("user",)

    fieldsets = (
        (
            "Manage the Grant",
            {
                "fields": (
                    "status",
                    "approved_type",
                    "country_type",
                    "ticket_amount",
                    "travel_amount",
                    "accommodation_amount",
                    "total_amount",
                    "applicant_reply_sent_at",
                    "applicant_reply_deadline",
                    "pretix_voucher_id",
                    "voucher_code",
                    "voucher_email_sent_at",
                    "internal_notes",
                )
            },
        ),
        (
            "About the Applicant",
            {
                "fields": (
                    "name",
                    "full_name",
                    "conference",
                    "user",
                    "age_group",
                    "gender",
                    "occupation",
                )
            },
        ),
        (
            "The Grant",
            {
                "fields": (
                    "grant_type",
                    "needs_funds_for_travel",
                    "need_visa",
                    "need_accommodation",
                    "nationality",
                    "departure_country",
                    "departure_city",
                    "why",
                    "python_usage",
                    "been_to_other_events",
                    "community_contribution",
                    "notes",
                )
            },
        ),
    )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        grant = self.model.objects.get(id=object_id)
        owner_id = grant.user_id
        extra_context["participant"] = Participant.objects.filter(
            user_id=owner_id,
            conference_id=grant.conference_id,
        ).first()

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    @admin.display(description="User", ordering="user__full_name")
    def user_display_name(self, obj):
        if obj.user_id:
            return obj.user.display_name
        return obj.email

    @admin.display(
        description="C",
    )
    def country(self, obj):
        if obj.departure_country:
            country = countries.get(code=obj.departure_country)
            if country:
                return country.emoji

        return ""

    @admin.display(description="✍️")
    def is_proposed_speaker(self, obj):
        if obj.is_proposed_speaker:
            return "✍️"
        return ""

    @admin.display(description="🗣️")
    def is_confirmed_speaker(self, obj):
        if obj.is_confirmed_speaker:
            return "🗣️"
        return ""

    @admin.display(description="⚤")
    def emoji_gender(self, obj):
        gender = obj.user.gender if obj.user else ""
        emoji = {
            "": "",
            "male": "👨🏻‍💻",
            "female": "👩🏼‍💻",
            "other": "🧑🏻‍🎤",
            "not_say": "⛔️",
        }
        return emoji[gender]

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .annotate(
                is_proposed_speaker=Exists(
                    Submission.objects.non_cancelled().filter(
                        conference_id=OuterRef("conference_id"),
                        speaker_id=OuterRef("user_id"),
                    )
                ),
                is_confirmed_speaker=Exists(
                    ScheduleItem.objects.filter(
                        conference_id=OuterRef("conference_id"),
                        submission__speaker_id=OuterRef("user_id"),
                    )
                ),
            )
        )
        return qs

    class Media:
        js = ["admin/js/jquery.init.js"]


@admin.register(GrantConfirmPendingStatusProxy)
class GrantConfirmPendingStatusProxyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "status",
        "to",
        "pending_status",
        "open_grant",
        "conference",
    )
    list_filter = ("status", "pending_status", "conference")
    search_fields = ("full_name", "user__email")
    list_display_links = None
    actions = [
        confirm_pending_status,
        reset_pending_status_back_to_status,
    ]

    def to(self, obj):
        return "➡️"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .exclude(
                pending_status=F("status"),
            )
        )

    def open_grant(self, obj):
        url = reverse("admin:grants_grant_change", args=[obj.id])
        return mark_safe(f'<a href="{url}">Open Grant</a>')
