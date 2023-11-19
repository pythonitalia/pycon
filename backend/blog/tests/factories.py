import factory
import factory.fuzzy
from django.utils import timezone
from factory.django import DjangoModelFactory
from pytest_factoryboy import register

from blog.models import Post
from i18n.tests.factories import LanguageFactory
from users.tests.factories import UserFactory


@register
class PostFactory(DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    title = LanguageFactory("sentence")
    slug = LanguageFactory("slug")
    excerpt = LanguageFactory("sentence")
    content = LanguageFactory("sentence")
    published = timezone.now()
    image = factory.django.ImageField()

    class Meta:
        model = Post
