from api.forms import ContextAwareModelForm
from upload.models import File


class UploadFileForm(ContextAwareModelForm):
    class Meta:
        model = File
        fields = ("file",)
