import factory
from factory import fuzzy
from faker import Faker
from datetime import timedelta
from decimal import Decimal
import uuid

from services.models import (
    Category, Microservice, Cart, CartItem, WishList, WishListItem,
    OrderMicroService, Review
)
from .core_factories import UserFactory, ClientProfileFactory, FreelancerProfileFactory

fake = Faker()

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Iterator([
        'Web Development', 'Mobile Development', 'Data Science', 'Machine Learning',
        'UI/UX Design', 'Digital Marketing', 'Content Writing', 'Translation',
        'Video Editing', 'Graphic Design', 'SEO Services', 'Social Media Management',
        'DevOps & Cloud', 'Cybersecurity', 'Blockchain Development'
    ])
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-').replace('&', 'and') + f"-{fake.random_int(min=1, max=999)}")

class MicroserviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Microservice

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.LazyFunction(lambda: fake.catch_phrase() + " Service")
    description = factory.Faker('paragraph', nb_sentences=4)
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True, min_value=25, max_value=999)
    delivery_time = factory.LazyFunction(lambda: timedelta(days=fake.random_int(min=1, max=30)))
    active = True
    category = factory.SubFactory(CategoryFactory)
    freelancer = factory.SubFactory(FreelancerProfileFactory)

class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)

class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    micro_service = factory.SubFactory(MicroserviceFactory)
    quantity = factory.Faker('random_int', min=1, max=3)

class WishListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishList

    user = factory.SubFactory(UserFactory)

class WishListItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishListItem

    wish_list = factory.SubFactory(WishListFactory)
    micro_service = factory.SubFactory(MicroserviceFactory)

class OrderMicroServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderMicroService

    id = factory.LazyFunction(uuid.uuid4)
    client = factory.SubFactory(ClientProfileFactory)
    micro_service = factory.SubFactory(MicroserviceFactory)
    freelancer = factory.LazyAttribute(lambda obj: obj.micro_service.freelancer)
    agreed_price = factory.LazyAttribute(lambda obj: obj.micro_service.price)
    state = factory.Iterator(['CREATED', 'PAID', 'IN_PROGRESS', 'DELIVERED', 'CANCELED'])

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    order = factory.SubFactory(OrderMicroServiceFactory)
    rating = factory.Faker('random_int', min=1, max=5)
    comment = factory.Faker('paragraph', nb_sentences=2)
    moderated = factory.Faker('boolean', chance_of_getting_true=80)
