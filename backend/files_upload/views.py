from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.conf import settings
from files_upload.models import File


@csrf_exempt
def local_file_upload(request, file_id):
    if not settings.DEBUG:
        return HttpResponse(status=400)

    uploaded_file = request.FILES["file"]
    file = File.objects.get(id=file_id)
    file.file = uploaded_file
    file.save()

    return HttpResponse(status=204)
