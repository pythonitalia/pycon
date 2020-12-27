from django.core.serializers.json import Deserializer as JSONDeserializer
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.json import Serializer as JSONSerializer

from .strings import LazyI18nString


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, LazyI18nString):
            return obj.data

        return super(CustomJSONEncoder, self).default(obj)


class Serializer(JSONSerializer):
    internal_use_only = False

    def serialize(self, *args, **kwargs):
        kwargs["cls"] = CustomJSONEncoder

        return super().serialize(*args, **kwargs)


Deserializer = JSONDeserializer
