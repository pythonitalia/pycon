from django import forms


class ContextAwareModelForm(forms.ModelForm):
    """A form that allows you to access the request context in `self.context`.

    For example, you can use the Request object to access the logged user in the `save` method.

    Inherit from this class if your mutation uses
    :py:class:`api.mutations.ContextAwareDjangoModelFormMutation` (or subclasses)
    and want to access the request object using `self.context`.
    """
    def __init__(self, *args, **kwargs):  # pylint: disable=return-in-init
        self._context = kwargs.pop('context', None)
        return super().__init__(*args, **kwargs)

    @property
    def context(self):
        if not self._context:
            raise ValueError('Make sure you pass the context when instancing the Form')

        return self._context


class ContextAwareForm(forms.Form):
    """A form that allows you to access the request context in `self.context`.

    For example, you can use the Request object to access the logged user in the `save` method.

    Inherit from this class if your mutation uses
    :py:class:`api.mutations.ContextAwareDjangoFormMutation` (or subclasses)
    and want to access the request object using `self.context`.
    """
    def __init__(self, *args, **kwargs):  # pylint: disable=return-in-init
        self._context = kwargs.pop('context', None)
        return super().__init__(*args, **kwargs)

    @property
    def context(self):
        if not self._context:
            raise ValueError('Make sure you pass the context when instancing the Form')

        return self._context
