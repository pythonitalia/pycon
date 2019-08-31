from django.http import HttpResponseForbidden, JsonResponse
from upload.forms import UploadFileForm


def file_upload(request):
    if request.method != "POST":
        return HttpResponseForbidden()

    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({"url": form.instance.file.path})
