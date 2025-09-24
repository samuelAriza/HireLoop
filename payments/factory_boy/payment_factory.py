import factory
from factory import fuzzy
from django.conf import settings
from ..models import Payment
from core.factory_boy.user_factory import UserFactory
import uuid

class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory(UserFactory)
    stripe_session_id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    stripe_payment_intent = factory.LazyFunction(lambda: str(uuid.uuid4()))
    amount = fuzzy.FuzzyDecimal(5.0, 1000.0, 2)
    currency = "usd"
    status = factory.Iterator(["pending", "succeeded", "failed", "canceled"])
