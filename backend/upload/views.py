from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse

from upload.models import Upload


def file_upload(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    file = request.FILES["file"]
    upload = Upload(file=file)
    upload.save()
    if not settings.USE_AWS_S3:
        url = upload.file.path
    else:
        url = upload.file.name
    return JsonResponse({"url": url})
