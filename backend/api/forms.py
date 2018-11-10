from django import forms


class GrapheneModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', None)
        return super().__init__(*args, **kwargs)
