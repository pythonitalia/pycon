from django.http import HttpResponse


def disabled_view(request):
    return HttpResponse("This view is disabled. Use the main Django admin.", status=200)
