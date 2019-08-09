import factory
import factory.fuzzy

from pytest_factoryboy import register
from factory.django import DjangoModelFactory
from django.utils import timezone

from blog.models import Post
from tests.users.factories import UserFactory


@register
class PostFactory(DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    slug = factory.Faker('slug')
    excerpt = factory.Faker('sentence')
    content = factory.Faker('sentence')
    published = timezone.now()
    image = factory.django.ImageField()
    

    class Meta:
        model = Post
        # django_get_or_create = ('email',)
