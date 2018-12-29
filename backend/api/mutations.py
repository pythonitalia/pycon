from graphql import GraphQLError

from graphene_django.forms import mutation


class ContextAwareDjangoModelFormMutation(mutation.DjangoModelFormMutation):
    class Meta:
        abstract = True

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        kwargs = super().get_form_kwargs(root, info, **input)
        kwargs['context'] = info.context
        return kwargs


class AuthOnlyDjangoFormMutation(ContextAwareDjangoModelFormMutation):
    class Meta:
        abstract = True

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if not info.context.user.is_authenticated:
            raise GraphQLError('User not logged in')

        return super().mutate_and_get_payload(root, info, **input)
