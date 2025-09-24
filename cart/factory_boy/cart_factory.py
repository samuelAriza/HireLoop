import factory
import random
from django.contrib.contenttypes.models import ContentType
from cart.models import CartItem, WishlistItem
from core.factory_boy.user_factory import UserFactory
from microservices.factory_boy.microservice_factory import MicroServiceFactory
from mentorship_session.factory_boy.mentorship_factory import MentorshipSessionFactory

COMPARABLE_MODELS = [MicroServiceFactory._meta.model, MentorshipSessionFactory._meta.model]

class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    user = factory.SubFactory(UserFactory)
    quantity = factory.Faker("random_int", min=1, max=5)

    @factory.lazy_attribute
    def content_type(self):
        model_class = random.choice(COMPARABLE_MODELS)
        return ContentType.objects.get_for_model(model_class)

    @factory.lazy_attribute
    def object_id(self):
        model_class = self.content_type.model_class()
        instance = model_class.objects.first() or model_class.objects.create()
        return instance.id


class WishlistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishlistItem

    user = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def content_type(self):
        model_class = random.choice(COMPARABLE_MODELS)
        return ContentType.objects.get_for_model(model_class)

    @factory.lazy_attribute
    def object_id(self):
        model_class = self.content_type.model_class()
        instance = model_class.objects.first() or model_class.objects.create()
        return instance.id