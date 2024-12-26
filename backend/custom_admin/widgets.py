from django.forms import Textarea


class RichEditorWidget(Textarea):
    template_name = "astro/widgets/rich-editor.html"
