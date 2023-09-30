from asgiref.sync import async_to_sync
from django.conf import settings
from django.http import JsonResponse
from pythonit_toolkit.service_client import ServiceClient

SEARCH_USERS = """query SearchUsers($query: String!) {
    searchUsers(query: $query) {
        id
        displayName
    }
}
"""


def users_autocomplete(request):
    raise ValueError("Check usages")
    term = request.GET.get("term", "")
    client = ServiceClient(
        url=f"{settings.USERS_SERVICE_URL}/internal-api",
        service_name="users-backend",
        caller="pycon-backend",
        jwt_secret=settings.SERVICE_TO_SERVICE_SECRET,
    )
    client_execute = async_to_sync(client.execute)
    search_result = client_execute(SEARCH_USERS, {"query": term})
    search_data = search_result.data

    return JsonResponse(
        {
            "results": [
                {"id": result["id"], "text": result["displayName"]}
                for result in search_data["searchUsers"]
            ],
            "pagination": {"more": False},
        }
    )
