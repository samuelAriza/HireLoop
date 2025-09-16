import factory
from faker import Faker
from datetime import datetime, timedelta
from django.utils import timezone
import uuid

from mentorship.models import MentorShipSession
from .core_factories import UserFactory

fake = Faker()

class MentorShipSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MentorShipSession

    id = factory.LazyFunction(uuid.uuid4)
    topic = factory.Iterator([
        'Career Transition to Tech', 'Django Development Best Practices',
        'React Frontend Architecture', 'Database Design Patterns',
        'System Design Interview Prep', 'Leadership in Tech Teams',
        'Freelancing Success Strategies', 'Product Management Fundamentals',
        'DevOps Implementation', 'Data Science Career Path'
    ])
    start_time = factory.LazyFunction(
        lambda: timezone.make_aware(fake.date_time_between(start_date='-30d', end_date='+30d'))
    )
    duration = factory.LazyFunction(
        lambda: timedelta(hours=fake.random_int(min=1, max=3))
    )
    state = factory.Iterator(['SCHEDULED', 'COMPLETED', 'CANCELED', 'NO_SHOW'])
    mentor = factory.SubFactory(UserFactory)
    mentee = factory.SubFactory(UserFactory)
