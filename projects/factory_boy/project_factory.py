# projects/factory_boy/project_factory.py
import factory
from factory import fuzzy
import uuid
from projects.models import Project, ProjectAssignment, ProjectApplication
from core.factory_boy.client_factory import ClientProfileFactory
from core.factory_boy.freelancer_factory import FreelancerProfileFactory
from core.factory_boy.helpers.helper import get_random_image_from

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    client = factory.SubFactory(ClientProfileFactory)
    title = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("paragraph", nb_sentences=3)
    status = factory.Iterator([s[0] for s in Project.ProjectStatus.choices])
    budget = fuzzy.FuzzyDecimal(100, 5000, 2)
    image_path = factory.LazyFunction(lambda: get_random_image_from("projects/dummy"))

class ProjectAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectAssignment

    project = factory.SubFactory(ProjectFactory)
    freelancer = factory.SubFactory(FreelancerProfileFactory)
    role = factory.Faker("job")
    agreed_payment = fuzzy.FuzzyDecimal(100, 2000, 2)
    status = factory.Iterator([s[0] for s in ProjectAssignment.ProjectAssignmentStatus.choices])


class ProjectApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectApplication

    project = factory.SubFactory(ProjectFactory)
    freelancer = factory.SubFactory(FreelancerProfileFactory)
    cover_letter = factory.Faker("paragraph", nb_sentences=2)
    proposed_payment = fuzzy.FuzzyDecimal(100, 3000, 2)
    status = factory.Iterator([s[0] for s in ProjectApplication.ApplicationStatus.choices])