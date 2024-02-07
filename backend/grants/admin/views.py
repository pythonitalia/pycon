from django.template.response import TemplateResponse
from django.db.models import Count, Sum
from helpers.constants import GENDERS
from countries import countries
from grants.models import Grant
from conferences.models import Conference


def summary_view(request, object_id, extra_context):
    """
    Custom view for summarizing Grant data in the Django admin.
    Aggregates data by country and status, and applies request filters.
    """
    statuses = Grant.Status.choices
    conference_name = Conference.objects.get(id=object_id).name

    filtered_grants = Grant.objects.filter(conference_id=object_id)

    grants_by_country = filtered_grants.values("travelling_from", "status").annotate(
        total=Count("id")
    )

    (
        country_stats,
        status_totals,
        totals_per_continent,
    ) = _aggregate_data_by_country(grants_by_country, statuses)
    gender_stats = _aggregate_data_by_gender(filtered_grants, statuses)
    financial_summary, total_amount = _aggregate_financial_data_by_status(
        filtered_grants, statuses
    )

    sorted_country_stats = dict(
        sorted(country_stats.items(), key=lambda x: (x[0][0], x[0][2]))
    )

    context = {
        "title": f"{conference_name} - Grant Summary",
        "conference_id": object_id,
        "conference_name": conference_name,
        "country_stats": sorted_country_stats,
        "statuses": statuses,
        "genders": {code: name for code, name in GENDERS},
        "financial_summary": financial_summary,
        "total_amount": total_amount,
        "total_grants": filtered_grants.count(),
        "status_totals": status_totals,
        "totals_per_continent": totals_per_continent,
        "gender_stats": gender_stats,
        **extra_context,
    }
    return TemplateResponse(request, "admin/grants/grant_summary.html", context)


def _aggregate_data_by_country(grants_by_country, statuses):
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


def _aggregate_data_by_gender(filtered_grants, statuses):
    """
    Aggregates grant data by gender and status.
    """
    gender_data = filtered_grants.values("gender", "status").annotate(total=Count("id"))
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


def _aggregate_financial_data_by_status(filtered_grants, statuses):
    """
    Aggregates financial data (total amounts) by grant status.
    """
    financial_data = filtered_grants.values("status").annotate(
        total_amount_sum=Sum("total_amount")
    )
    financial_summary = {status[0]: 0 for status in statuses}
    overall_total = 0

    for data in financial_data:
        status = data["status"]
        total_amount = data["total_amount_sum"] or 0
        financial_summary[status] += total_amount
        overall_total += total_amount

    return financial_summary, overall_total


def _filter_and_format_grants(request):
    """
    Filters the Grant queryset based on request parameters and
    formats the filter keys for display.
    """
    field_lookups = [
        "__exact",
        "__in",
        "__gt",
        "__lt",
        "__contains",
        "__startswith",
        "__endswith",
        "__range",
        "__isnull",
    ]

    filter_mapping = {
        "conference__id": "Conference ID",
        "status": "Status",
        "country_type": "Country Type",
        "occupation": "Occupation",
        "grant_type": "Grant Type",
        "travelling_from": "Country",
    }

    # Construct a set of allowed filters
    allowed_filters = {
        f + lookup for f in filter_mapping.keys() for lookup in field_lookups
    }

    def map_filter_key(key):
        """Helper function to map raw filter keys to user-friendly names"""
        base_key = next(
            (key[: -len(lookup)] for lookup in field_lookups if key.endswith(lookup)),
            key,
        )
        return filter_mapping.get(base_key, base_key.capitalize())

    # Apply filtered parameters and format filter keys for display
    raw_filter_params = {k: v for k, v in request.GET.items() if k in allowed_filters}
    filter_params = {map_filter_key(k): v for k, v in raw_filter_params.items()}

    filtered_grants = Grant.objects.filter(**raw_filter_params)

    return filtered_grants, filter_params
