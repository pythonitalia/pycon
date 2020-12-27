from django import forms


class FormWithContext(forms.Form):
    def __init__(self, *args, **kwargs):  # pylint: disable=return-in-init
        self._context = kwargs.pop("context", None)
        return super().__init__(*args, **kwargs)

    @property
    def context(self):
        if not self._context:
            raise ValueError("Make sure you pass the context when instancing the Form")

        return self._context
