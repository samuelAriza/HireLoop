import factory
from .user_factory import UserFactory
from core.models import ClientProfile

class ClientProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClientProfile

    # Vincula automáticamente un User usando SubFactory
    user = factory.SubFactory(UserFactory)

    # Campos dummy
    company = factory.Faker("company")
    billing_address = factory.Faker("address")
    billing_email = factory.LazyAttribute(lambda obj: obj.user.email)
