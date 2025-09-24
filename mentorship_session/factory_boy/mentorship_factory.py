import factory
from factory import fuzzy
from datetime import datetime, timedelta
from core.factory_boy.freelancer_factory import FreelancerProfileFactory
from core.factory_boy.client_factory import ClientProfileFactory
from ..models import MentorshipSession
from core.factory_boy.helpers.helper import get_random_image_from

class MentorshipSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MentorshipSession

    topic = factory.Faker("sentence", nb_words=4)
    start_time = factory.LazyFunction(lambda: datetime.now() + timedelta(days=1))
    duration_minutes = fuzzy.FuzzyInteger(15, 120)
    mentor = factory.SubFactory(FreelancerProfileFactory)
    mentee = factory.SubFactory(ClientProfileFactory)
    status = fuzzy.FuzzyChoice(
        [MentorshipSession.MentorshipStatus.SCHEDULED,
         MentorshipSession.MentorshipStatus.COMPLETED,
         MentorshipSession.MentorshipStatus.CANCELED,
         MentorshipSession.MentorshipStatus.NO_SHOW]
    )
    image_path = factory.LazyFunction(lambda: get_random_image_from("mentorships/dummy"))
