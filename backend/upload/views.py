from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse

from upload.models import File


def file_upload(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    file = request.FILES["file"]
    upload = File(file=file)
    upload.save()
    url = upload.file.url
    if not settings.USE_AWS_S3:
        import os

        url = os.path.dirname(settings.MEDIA_ROOT) + url
    return JsonResponse({"url": url})
