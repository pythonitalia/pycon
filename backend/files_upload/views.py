from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from files_upload.models import File


@csrf_exempt
def local_file_upload(request, file_id):
    uploaded_file = request.FILES["file"]
    file = File.objects.get(id=file_id)
    file.file = uploaded_file
    file.save()

    return HttpResponse(status=204)
