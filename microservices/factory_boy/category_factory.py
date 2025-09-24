import factory
from ..models import Category
from factory import fuzzy
from django.utils.text import slugify

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
