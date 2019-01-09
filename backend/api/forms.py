from django import forms


class GrapheneModelForm(forms.ModelForm):
    """Inherit from this class if your mutation uses
    :py:class:`api.mutations.ContextAwareDjangoModelFormMutation` (or subclasses)
    and want to access the request object using `self.context`.

    For example, you can use the Request object to access the logged user in the `save` method.
    """
    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', None)
        return super().__init__(*args, **kwargs)
