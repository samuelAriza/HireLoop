import factory
from factory import fuzzy
from ..models import MicroService
from core.factory_boy.freelancer_factory import FreelancerProfileFactory
from .category_factory import CategoryFactory
from core.factory_boy.helpers.helper import get_random_image_from

class MicroServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MicroService

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph", nb_sentences=3)
    price = fuzzy.FuzzyDecimal(10.0, 500.0, 2)
    delivery_time = fuzzy.FuzzyInteger(1, 30)
    is_active = True
    image_path = factory.LazyFunction(lambda: get_random_image_from("microservices/dummy"))
    freelancer = factory.SubFactory(FreelancerProfileFactory)
    category = factory.SubFactory(CategoryFactory)
