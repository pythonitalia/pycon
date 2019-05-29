import graphene

from collections import OrderedDict

from graphene import Mutation, String, Argument
from graphene.types.union import Union
from graphene.types.field import Field
from graphene.types.mutation import MutationOptions

from .utils import create_errors_type, convert_form_fields_to_fields, create_input_type


class FormMutationOptions(MutationOptions):
    form_class = None
    error_type = None


class FormMutation(Mutation):
    @classmethod
    def __init_subclass_with_meta__(cls, form_class, name=None, output_types=(), **options):
        cls_name = name or cls.__name__
        form = form_class()

        form_fields = form.fields

        graphql_fields = convert_form_fields_to_fields(form_fields)

        input_type = create_input_type(cls_name, graphql_fields)
        error_type = create_errors_type(cls_name, graphql_fields)

        cls.Arguments = type(
            f'{cls_name}Arguments',
            (),
            OrderedDict(
                input=Argument(input_type)
            ),
        )

        class OutputUnion(Union):
            class Meta:
                types = (error_type, ) + output_types
                name = f'{cls_name}Output'

        cls.Output = OutputUnion

        _meta = FormMutationOptions(cls)
        _meta.form_class = form_class
        _meta.error_type = error_type

        super().__init_subclass_with_meta__(
            _meta=_meta,
            **options
        )

    @classmethod
    def mutate(cls, root, info, input):
        form = cls.get_form(root, info, input)

        if not form.is_valid():
            error_cls = cls.get_error_type()
            error_instance = error_cls()

            for name, messages in form.errors.items():
                if name == '__all__':
                    name = 'nonFieldErrors'

                setattr(error_instance, name, messages)

            return error_instance

        output = form.save()
        return output

    @classmethod
    def get_form(cls, root, info, input):
        form_kwargs = cls.get_form_kwargs(root, info, input)
        return cls._meta.form_class(**form_kwargs)

    @classmethod
    def get_form_kwargs(cls, root, info, input):
        kwargs = {'data': input}

        if hasattr(info, 'context'):
            kwargs['context'] = info.context

        return kwargs

    @classmethod
    def get_error_type(cls):
        return cls._meta.error_type
