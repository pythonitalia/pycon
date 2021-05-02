import factory
import factory.fuzzy
from django.utils import timezone
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from blog.models import Post
from i18n.tests.factories import LanguageFactory


@register
class PostFactory(DjangoModelFactory):
    author_id = factory.Faker("pyint", min_value=1)
    title = LanguageFactory("sentence")
    slug = LanguageFactory("slug")
    excerpt = LanguageFactory("sentence")
    content = LanguageFactory("sentence")
    published = timezone.now()
    image = factory.django.ImageField()

    class Meta:
        model = Post
