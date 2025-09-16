import factory
from factory import fuzzy
from django.contrib.auth import get_user_model
from faker import Faker
from core.models import User, ClientProfile, FreelancerProfile, PortfolioItem
import uuid

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    password = factory.PostGenerationMethodCall('set_password', 'defaultpass123')

class ClientProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientProfile

    id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    company = factory.Faker('company')
    billing_email = factory.LazyAttribute(lambda obj: obj.user.email)

class FreelancerProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FreelancerProfile

    id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    skills = factory.LazyFunction(lambda: fake.random_elements(
        elements=['Python', 'Django', 'React', 'JavaScript', 'Node.js', 'PostgreSQL', 
                 'Docker', 'AWS', 'Machine Learning', 'Data Analysis', 'UI/UX Design',
                 'Mobile Development', 'DevOps', 'Cybersecurity', 'Blockchain'],
        length=fake.random_int(min=2, max=6),
        unique=True
    ))
    bio = factory.Faker('paragraph', nb_sentences=5)
    rating = factory.Faker('pyfloat', left_digits=1, right_digits=1, positive=True, min_value=3.0, max_value=5.0)

class PortfolioItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PortfolioItem

    id = factory.LazyFunction(uuid.uuid4)
    freelancer = factory.SubFactory(FreelancerProfileFactory)
    title = factory.Faker('catch_phrase')
    description = factory.Faker('paragraph', nb_sentences=3)
    demo_url = factory.Faker('url')
