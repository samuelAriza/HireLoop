import factory
from faker import Faker
import uuid
from django.contrib.auth import get_user_model
from .helpers.helper import get_random_image_from
fake = Faker()
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid.uuid4)
    username = factory.LazyAttribute(lambda x: fake.user_name())
    email = factory.LazyAttribute(lambda x: fake.unique.email())
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    profile_image = factory.LazyFunction(lambda: get_random_image_from("profiles/dummy"))