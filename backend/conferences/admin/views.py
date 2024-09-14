from django.shortcuts import render
from grants.summary import GrantSummary
from django.contrib.admin import site as admin_site


def grants_summary(request, object_id):
    context = GrantSummary().calculate(conference_id=object_id)

    return render(
        request,
        "admin/grants/grant_summary.html",
        {**context, **admin_site.each_context(request)},
    )
