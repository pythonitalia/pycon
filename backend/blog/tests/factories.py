import factory
import factory.fuzzy
from blog.models import Post
from django.utils import timezone
from factory.django import DjangoModelFactory
from i18n.helpers.tests import LanguageFactory
from pytest_factoryboy import register
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
