from django.db.models import Count, Sum
from conferences.models.conference import Conference
from helpers.constants import GENDERS
from countries import countries
from .models import Grant


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
            "travelling_from", "status"
        ).annotate(total=Count("id"))

        (
            country_stats,
            status_totals,
            totals_per_continent,
        ) = self._aggregate_data_by_country(grants_by_country, statuses)
        gender_stats = self._aggregate_data_by_gender(filtered_grants, statuses)
        financial_summary, total_amount = self._aggregate_financial_data_by_status(
            filtered_grants, statuses
        )

        sorted_country_stats = dict(
            sorted(country_stats.items(), key=lambda x: (x[0][0], x[0][2]))
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
        )

    def _aggregate_data_by_country(self, grants_by_country, statuses):
        """
        Aggregates grant data by country and status.
        """

        summary = {}
        status_totals = {status[0]: 0 for status in statuses}
        totals_per_continent = {}

        for data in grants_by_country:
            country = countries.get(code=data["travelling_from"])
            continent = country.continent.name if country else "Unknown"
            country_name = f"{country.name} {country.emoji}" if country else "Unknown"
            country_code = country.code if country else "Unknown"
            key = (continent, country_name, country_code)

            if key not in summary:
                summary[key] = {status[0]: 0 for status in statuses}

            summary[key][data["status"]] += data["total"]
            status_totals[data["status"]] += data["total"]

            # Update continent totals
            if continent not in totals_per_continent:
                totals_per_continent[continent] = {status[0]: 0 for status in statuses}
            totals_per_continent[continent][data["status"]] += data["total"]

        return summary, status_totals, totals_per_continent

    def _aggregate_data_by_gender(self, filtered_grants, statuses):
        """
        Aggregates grant data by gender and status.
        """
        gender_data = filtered_grants.values("gender", "status").annotate(
            total=Count("id")
        )
        gender_summary = {
            gender: {status[0]: 0 for status in statuses} for gender, _ in GENDERS
        }
        gender_summary[""] = {
            status[0]: 0 for status in statuses
        }  # For unspecified genders

        for data in gender_data:
            gender = data["gender"] if data["gender"] else ""
            status = data["status"]
            total = data["total"]
            gender_summary[gender][status] += total

        return gender_summary

    def _aggregate_financial_data_by_status(self, filtered_grants, statuses):
        """
        Aggregates financial data (total amounts) by grant status.
        """
        financial_data = filtered_grants.values("status").annotate(
            total_amount_sum=Sum("total_amount")
        )
        print(financial_data)
        financial_summary = {status[0]: 0 for status in statuses}
        overall_total = 0

        for data in financial_data:
            status = data["status"]
            total_amount = data["total_amount_sum"] or 0
            financial_summary[status] += total_amount
            if status in self.BUDGET_STATUSES:
                overall_total += total_amount

        return financial_summary, overall_total
