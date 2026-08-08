from django import forms
from django.utils.text import slugify

from generic_forms.models import FormQuestion


class OptionsField(forms.Field):
    """Edit select/multi-select options as one option per line, either as
    "id | label" or just "label" (the id is slugified from the label).
    Stored as the usual [{"id": ..., "label": ...}] JSON.
    """

    widget = forms.Textarea(attrs={"rows": 4, "placeholder": "vegan | Vegan\nVeggie"})

    def prepare_value(self, value):
        if isinstance(value, list):
            return "\n".join(f"{option['id']} | {option['label']}" for option in value)
        return value

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value

        options = []
        for line in value.splitlines():
            line = line.strip()
            if not line:
                continue
            if "|" in line:
                option_id, _, label = line.partition("|")
                options.append({"id": option_id.strip(), "label": label.strip()})
            else:
                options.append({"id": slugify(line), "label": line})
        return options


class FormQuestionInlineForm(forms.ModelForm):
    options = OptionsField(
        required=False,
        help_text='One option per line: "id | label", or just "label" to '
        "derive the id from it. Only for select/multi select questions.",
    )

    class Meta:
        model = FormQuestion
        fields = "__all__"
