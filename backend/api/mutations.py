from graphql import GraphQLError

from graphene_django.forms import mutation


class ContextAwareDjangoModelFormMutation(mutation.DjangoModelFormMutation):
    """Allows the Form to access the Request object by passing it
    in the Form constructor.

    See also:

    - :py:class:`api.forms.ContextAwareModelForm`
    """
    class Meta:
        abstract = True

    @classmethod
    def get_form_kwargs(cls, root, info, **input_):
        kwargs = super().get_form_kwargs(root, info, **input_)
        kwargs['context'] = info.context
        return kwargs


class AuthOnlyDjangoModelFormMutation(ContextAwareDjangoModelFormMutation):
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


class ContextAwareDjangoMutation(mutation.DjangoFormMutation):
    """Allows the Form to access the Request object by passing it
    in the Form constructor.

    See also:

    - :py:class:`api.forms.ContextAwareModelForm`
    """
    class Meta:
        abstract = True

    @classmethod
    def perform_mutate(cls, form, info):
        # TODO: Why graphene ignores the form.save output?
        # how are we supposed to return something to the client?
        output = form.save()
        import pdb; pdb.set_trace()
        return output
        return cls(**output, errors=[])

    @classmethod
    def get_form_kwargs(cls, root, info, **input_):
        kwargs = super().get_form_kwargs(root, info, **input_)
        kwargs['context'] = info.context
        return kwargs


class AuthOnlyDjangoFormMutation(ContextAwareDjangoMutation):
    """Before executing the mutation, checks if the Request object has an authenticated
    user, if not a `GraphQLError` is thrown.

    Inherits from ContextAwareDjangoMutation to allow the
    mutation to access the Request object.

    See also:

    - :py:class:`api.mutations.ContextAwareDjangoMutation`
    """
    class Meta:
        abstract = True

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input_):
        if not info.context.user.is_authenticated:
            raise GraphQLError('User not logged in')

        return super().mutate_and_get_payload(root, info, **input_)
