import factory
from pytest_factoryboy import register
from voting.models import RankRequest


@register
class RankRequestFactory(factory.DjangoModelFactory):
    class Meta:
        model = RankRequest
