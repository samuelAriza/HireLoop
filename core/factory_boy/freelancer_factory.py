import factory
from .user_factory import UserFactory
from core.models import FreelancerProfile

class FreelancerProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FreelancerProfile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker('text')
    skills = factory.Faker('words', nb=5, ext_word_list=None)