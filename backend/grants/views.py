from django.shortcuts import render
from .models import Grant
from collections import defaultdict

# Mapping countries to continents
country_to_continent = {
    "italy": "Europe",
    # ... add other countries and their respective continents
}


def grant_summary_view(request):
    grants = Grant.objects.all()

    # Initialize a dictionary to hold the counts
    summary = defaultdict(lambda: defaultdict(int))

    for grant in grants:
        continent = country_to_continent.get(grant.travelling_from, "")
        summary[continent][grant.status] += 1

    context = {"summary": dict(summary)}
    return render(request, "admin/grants/grant_summary.html", context)
