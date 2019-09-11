from django import forms


class ContextAwareModelForm(forms.ModelForm):
    """A form that allows you to access the request context in `self.context`.

    For example, you can use the Request object to access
    the logged user in the `save` method.

    Inherit from this class if your mutation uses
    :py:class:`api.mutations.ContextAwareDjangoModelFormMutation` (or subclasses)
    and want to access the request object using `self.context`.
    """

    def __init__(self, *args, **kwargs):  # pylint: disable=return-in-init
        self.context = kwargs.pop("context", None)
        return super().__init__(*args, **kwargs)
