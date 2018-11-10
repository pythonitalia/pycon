from graphene_django.forms import mutation


class ContextAwareDjangoModelFormMutation(mutation.DjangoModelFormMutation):
    class Meta:
        abstract = True

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = super().get_form_kwargs(root, info, **input)
        kwargs['context'] = info.context
        return kwargs
