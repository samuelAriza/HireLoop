import factory
from faker import Faker
import uuid

from payments.models import PaymentMethod, Payment
from .core_factories import UserFactory
from .services_factories import OrderMicroServiceFactory
from .mentorship_factories import MentorShipSessionFactory

fake = Faker()

class PaymentMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentMethod

    id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    pgw_token = factory.LazyFunction(lambda: fake.uuid4())
    last4 = factory.LazyFunction(lambda: str(fake.random_int(min=1000, max=9999)))
    type = factory.Iterator(['CARD', 'PAYPAL', 'STRIPE'])

class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    id = factory.LazyFunction(uuid.uuid4)
    amount = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True, min_value=10, max_value=999)
    currency = 'USD'
    provider = factory.Iterator(['stripe', 'paypal', 'square'])
    transaction_id = factory.LazyFunction(lambda: fake.uuid4())
    state = factory.Iterator(['PENDING', 'AUTHORIZED', 'CAPTURED', 'FAILED', 'REFUNDED'])
    method = factory.SubFactory(PaymentMethodFactory)
