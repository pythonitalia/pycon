import dataclasses
import enum
from typing import Union

import strawberry
from strawberry.utils.str_converters import to_camel_case
from django.forms import ModelForm
from graphql import GraphQLError

from .utils import convert_form_fields_to_fields, create_error_type, create_input_type


def convert_enums_to_values(d) -> dict:
    converted = {}

    for key, value in d.items():
        if isinstance(value, dict):
            converted[key] = convert_enums_to_values(value)
        elif isinstance(value, enum.Enum):
            converted[key] = value.value
        else:
            converted[key] = value

    return converted


class FormMutation:
    @classmethod
    def __init_subclass__(cls):
        name = cls.__name__

        form_class = cls.Meta.form_class
        form = form_class()

        form_fields = form.fields
        graphql_fields = convert_form_fields_to_fields(form_fields)

        input_type = None

        if len(graphql_fields) > 0:
            input_type = create_input_type(name, graphql_fields)

        error_type = create_error_type(name, graphql_fields)

        output_types = (
            cls.Meta.output_types if hasattr(cls.Meta, "output_types") else ()
        )

        output = strawberry.union(
            f"{name}Output", (error_type, *output_types), description="Output"
        )

        def _mutate(root, info, input: input_type) -> output:
            # Add the mutation input in the context so we can access it inside the permissions
            if info:
                setattr(info.context, "input", input)

            # Once we implement the permission in strawberry we can remove this :)
            if hasattr(cls.Meta, "permission_classes") and cls.Meta.permission_classes:
                for permission in cls.Meta.permission_classes:
                    if not permission().has_permission(root, info):
                        raise GraphQLError(permission.message)

            input_as_dict = input

            if dataclasses.is_dataclass(input):
                input_as_dict = dataclasses.asdict(input)

            form_kwargs = cls.get_form_kwargs(root, info, input_as_dict)
            form_kwargs["data"] = convert_enums_to_values(form_kwargs["data"])

            if "instance" in form_kwargs["data"] and issubclass(form_class, ModelForm):
                instance = form_kwargs["data"].pop("instance")
                instance = (
                    form_class.get_instance(instance)
                    if hasattr(form_class, "get_instance")
                    else form_class.Meta.model.objects.get(id=instance)
                )

                form = form_class(instance=instance, **form_kwargs)
                form.fields.pop("instance", None)
            else:
                form = form_class(**form_kwargs)

            error = cls.validate_form(form)

            if error:
                return error

            result = form.save()

            if hasattr(cls, "transform"):
                result = cls.transform(result)

            return result

        if input_type:

            def mutate(root, info, input: input_type) -> output:
                return _mutate(root, info, input)

        else:

            def mutate(root, info) -> output:
                return _mutate(root, info, {})

        # Hack because something changed and now the name contains `Mutation`
        # as the classname, which makes sense but why it didn't happen before? lol
        name = name.replace("Mutation", "")
        mutate = strawberry.mutation(mutate, name=f"{name[0].lower()}{name[1:]}")

        cls.Mutation = mutate
        cls.Meta.error_type = error_type

    @classmethod
    def validate_form(cls, form):
        if form.is_valid():
            return

        error_cls = cls.get_error_type()
        error_instance = error_cls()

        for name, messages in form.errors.items():
            if name == "__all__":
                name = "nonFieldErrors"

            setattr(error_instance, name, messages)

        return error_instance

    @classmethod
    def get_error_type(cls):
        return cls.Meta.error_type

    @classmethod
    def get_form_kwargs(cls, root, info, input):
        kwargs = {"data": input}

        if hasattr(info, "context"):
            kwargs["context"] = info.context

        return kwargs
