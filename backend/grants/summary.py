from collections import defaultdict

from django.db.models import Count, Exists, OuterRef, Sum

from conferences.models.conference import Conference
from countries import countries
from helpers.constants import GENDERS
from schedule.models import ScheduleItem
from submissions.models import Submission

from .models import Grant, GrantReimbursement


class GrantSummary:
    # Set of grant statuses included in the total budget calculation.
    BUDGET_STATUSES = [
        Grant.Status.approved.value,
        Grant.Status.waiting_for_confirmation.value,
        Grant.Status.confirmed.value,
    ]

    def calculate(self, conference_id):
        """
        Custom view for summarizing Grant data in the Django admin.
        Aggregates data by country and status, and applies request filters.
        """
        statuses = Grant.Status.choices
        conference = Conference.objects.get(id=conference_id)
        filtered_grants = Grant.objects.for_conference(conference)

        grants_by_country = filtered_grants.values(
            "departure_country", "pending_status"
        ).annotate(total=Count("id"))

        (
            country_stats,
            status_totals,
            totals_per_continent,
        ) = self._aggregate_data_by_country(grants_by_country, statuses)
        sorted_country_stats = dict(
            sorted(country_stats.items(), key=lambda x: (x[0][0], x[0][2]))
        )
        country_type_summary = self._aggregate_data_by_country_type(
            filtered_grants, statuses
        )
        gender_stats = self._aggregate_data_by_gender(filtered_grants, statuses)
        financial_summary, total_amount = self._aggregate_financial_data_by_status_new(
            filtered_grants, statuses
        )
        grant_type_summary = self._aggregate_data_by_grant_type(
            filtered_grants, statuses
        )
        speaker_status_summary = self._aggregate_data_by_speaker_status(
            filtered_grants, statuses
        )
        requested_needs_summary = self._aggregate_data_by_requested_needs_summary(
            filtered_grants, statuses
        )
        country_types = {
            country_type.value: country_type.label for country_type in Grant.CountryType
        }
        occupation_summary = self._aggregate_data_by_occupation(
            filtered_grants, statuses
        )

        reimbursement_category_summary = self._aggregate_data_by_reimbursement_category(
            filtered_grants, statuses
        )

        return dict(
            conference_id=conference_id,
            conference_repr=str(conference),
            country_stats=sorted_country_stats,
            statuses=statuses,
            genders={code: name for code, name in GENDERS},
            financial_summary=financial_summary,
            total_amount=total_amount,
            total_grants=filtered_grants.count(),
            status_totals=status_totals,
            totals_per_continent=totals_per_continent,
            gender_stats=gender_stats,
            preselected_statuses=["approved", "confirmed"],
            grant_type_summary=grant_type_summary,
            speaker_status_summary=speaker_status_summary,
            reimbursement_category_summary=reimbursement_category_summary,
            requested_needs_summary=requested_needs_summary,
            country_type_summary=country_type_summary,
            country_types=country_types,
            occupation_summary=occupation_summary,
        )

    def _aggregate_data_by_country(self, grants_by_country, statuses):
        """
        Aggregates grant data by country and status.
        """

        summary = {}
        status_totals = {status[0]: 0 for status in statuses}
        totals_per_continent = {}

        for data in grants_by_country:
            country = countries.get(code=data["departure_country"])
            continent = country.continent.name if country else "Unknown"
            country_name = f"{country.name} {country.emoji}" if country else "Unknown"
            country_code = country.code if country else "Unknown"
            key = (continent, country_name, country_code)

            if key not in summary:
                summary[key] = {status[0]: 0 for status in statuses}

            summary[key][data["pending_status"]] += data["total"]
            status_totals[data["pending_status"]] += data["total"]

            # Update continent totals
            if continent not in totals_per_continent:
                totals_per_continent[continent] = {status[0]: 0 for status in statuses}
            totals_per_continent[continent][data["pending_status"]] += data["total"]

        return summary, status_totals, totals_per_continent

    def _aggregate_data_by_country_type(self, filtered_grants, statuses):
        """
        Aggregates grant data by country type and status.
        """
        country_type_data = filtered_grants.values(
            "country_type", "pending_status"
        ).annotate(total=Count("id"))
        country_type_summary = defaultdict(
            lambda: {status[0]: 0 for status in statuses}
        )

        for data in country_type_data:
            country_type = data["country_type"]
            pending_status = data["pending_status"]
            total = data["total"]
            country_type_summary[country_type][pending_status] += total

        return dict(country_type_summary)

    def _aggregate_data_by_gender(self, filtered_grants, statuses):
        """
        Aggregates grant data by gender and status.
        """
        gender_data = filtered_grants.values("gender", "pending_status").annotate(
            total=Count("id")
        )
        gender_summary = defaultdict(lambda: {status[0]: 0 for status in statuses})

        for data in gender_data:
            gender = data["gender"] if data["gender"] else ""
            pending_status = data["pending_status"]
            total = data["total"]
            gender_summary[gender][pending_status] += total

        return dict(gender_summary)

    def _aggregate_financial_data_by_status(self, filtered_grants, statuses):
        """
        Aggregates financial data (total amounts) by grant status.
        """
        financial_summary = {status[0]: 0 for status in statuses}
        overall_total = 0

        for status in statuses:
            grants_for_status = filtered_grants.filter(pending_status=status[0])
            reimbursements = GrantReimbursement.objects.filter(
                grant__in=grants_for_status
            )
            total = reimbursements.aggregate(total=Sum("granted_amount"))["total"] or 0
            financial_summary[status[0]] = total
            if status[0] in self.BUDGET_STATUSES:
                overall_total += total

        return financial_summary, overall_total

    def _aggregate_data_by_reimbursement_category(self, filtered_grants, statuses):
        """
        Aggregates grant data by reimbursement category and status.
        """
        category_summary = defaultdict(lambda: {status[0]: 0 for status in statuses})
        reimbursements = GrantReimbursement.objects.filter(grant__in=filtered_grants)
        for r in reimbursements:
            category = r.category.category
            status = r.grant.pending_status
            category_summary[category][status] += 1
        return dict(category_summary)

    def _aggregate_data_by_grant_type(self, filtered_grants, statuses):
        """
        Aggregates grant data by grant_type and status.
        """
        grant_type_data = filtered_grants.values(
            "grant_type", "pending_status"
        ).annotate(total=Count("id"))
        grant_type_summary = defaultdict(lambda: {status[0]: 0 for status in statuses})

        for data in grant_type_data:
            grant_types = data["grant_type"]
            pending_status = data["pending_status"]
            total = data["total"]
            for grant_type in grant_types:
                grant_type_summary[grant_type][pending_status] += total

        return dict(grant_type_summary)

    def _aggregate_data_by_speaker_status(self, filtered_grants, statuses):
        """
        Aggregates grant data by speaker status (proposed and confirmed) and grant status.
        """
        filtered_grants = filtered_grants.annotate(
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

        proposed_speaker_data = (
            filtered_grants.filter(is_proposed_speaker=True)
            .values("pending_status")
            .annotate(total=Count("id"))
        )

        confirmed_speaker_data = (
            filtered_grants.filter(is_confirmed_speaker=True)
            .values("pending_status")
            .annotate(total=Count("id"))
        )

        speaker_status_summary = defaultdict(
            lambda: {status[0]: 0 for status in statuses}
        )

        for data in proposed_speaker_data:
            pending_status = data["pending_status"]
            total = data["total"]
            speaker_status_summary["proposed_speaker"][pending_status] += total

        for data in confirmed_speaker_data:
            pending_status = data["pending_status"]
            total = data["total"]
            speaker_status_summary["confirmed_speaker"][pending_status] += total

        return dict(speaker_status_summary)

    def _aggregate_data_by_requested_needs_summary(self, filtered_grants, statuses):
        """
        Aggregates grant data by boolean fields (needs_funds_for_travel, need_visa, need_accommodation) and status.
        """
        requested_needs_summary = {
            "needs_funds_for_travel": {status[0]: 0 for status in statuses},
            "need_visa": {status[0]: 0 for status in statuses},
            "need_accommodation": {status[0]: 0 for status in statuses},
        }

        for field in requested_needs_summary.keys():
            field_data = (
                filtered_grants.filter(**{field: True})
                .values("pending_status")
                .annotate(total=Count("id"))
            )
            for data in field_data:
                pending_status = data["pending_status"]
                total = data["total"]
                requested_needs_summary[field][pending_status] += total

        return requested_needs_summary

    def _aggregate_data_by_occupation(self, filtered_grants, statuses):
        """
        Aggregates grant data by occupation and status.
        """
        occupation_data = filtered_grants.values(
            "occupation", "pending_status"
        ).annotate(total=Count("id"))
        occupation_summary = defaultdict(lambda: {status[0]: 0 for status in statuses})

        for data in occupation_data:
            occupation = data["occupation"]
            pending_status = data["pending_status"]
            total = data["total"]
            occupation_summary[occupation][pending_status] += total

        return dict(occupation_summary)
