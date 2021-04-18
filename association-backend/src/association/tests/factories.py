import asyncio
import inspect

import ormar
from factory.base import Factory, FactoryOptions, OptionDefault


class Options(FactoryOptions):
    def _build_default_options(self):
        return super()._build_default_options() + [
            OptionDefault("get_or_create", (), inherit=True),
        ]


class ModelFactory(Factory):
    class Meta:
        abstract = True

    _options_class = Options

    @classmethod
    def _generate(cls, strategy, params):
        # Original params are used in _get_or_create if it cannot build an
        # object initially due to an IntegrityError being raised
        cls._original_params = params
        return super()._generate(strategy, params)

    @classmethod
    async def _get_or_create(cls, model_class, *args, **kwargs):
        """Create an instance of the model through objects.get_or_create."""
        manager = model_class.objects

        assert "defaults" not in cls._meta.get_or_create, (
            "'defaults' is a reserved keyword for get_or_create "
            "(in %s._meta.get_or_create=%r)" % (cls, cls._meta.get_or_create)
        )

        key_fields = {}
        for field in cls._meta.get_or_create:
            if field not in kwargs:
                raise ValueError(
                    "get_or_create - "
                    "Unable to find initialization value for '%s' in factory %s"
                    % (field, cls.__name__)
                )
            key_fields[field] = kwargs.pop(field)
        key_fields["defaults"] = kwargs

        try:
            instance, _created = await manager.get_or_create(*args, **key_fields)
        except Exception as e:
            # TODO fix
            get_or_create_params = {
                lookup: value
                for lookup, value in cls._original_params.items()
                if lookup in cls._meta.get_or_create
            }
            if get_or_create_params:
                try:
                    instance = await manager.get(**get_or_create_params)
                except ormar.NoMatch:
                    # Original params are not a valid lookup and triggered a create(),
                    # that resulted in an IntegrityError. Follow Django’s behavior.
                    raise e
            else:
                raise e

        return instance

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            for key, value in kwargs.items():
                if inspect.isawaitable(value):
                    kwargs[key] = await value

            if cls._meta.get_or_create:
                return await cls._get_or_create(model_class, *args, **kwargs)

            return await model_class.objects.create(*args, **kwargs)

        return asyncio.create_task(maker_coroutine())
