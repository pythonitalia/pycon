from graphql import GraphQLError

from graphene_django.forms import mutation


class ContextAwareDjangoModelFormMutation(mutation.DjangoModelFormMutation):
    """Allows the Form to access the Request object by passing it
    in the Form constructor.

    See also:

    - :py:class:`api.forms.ContextAwareForm`
    """
    class Meta:
        abstract = True

    @classmethod
    def get_form_kwargs(cls, root, info, **input_):
        kwargs = super().get_form_kwargs(root, info, **input_)
        kwargs['context'] = info.context
        return kwargs


class AuthOnlyDjangoFormMutation(ContextAwareDjangoModelFormMutation):
    """Before executing the mutation, checks if the Request object has an authenticated
    user, if not a `GraphQLError` is thrown.

    Inherits from ContextAwareDjangoModelFormMutation to allow the
    mutation to access the Request object.

    See also:

    - :py:class:`api.mutations.ContextAwareDjangoModelFormMutation`
    """
    class Meta:
        abstract = True

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input_):
        if not info.context.user.is_authenticated:
            raise GraphQLError('User not logged in')

        return super().mutate_and_get_payload(root, info, **input_)
