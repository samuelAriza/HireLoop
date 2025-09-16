import factory
from faker import Faker
import uuid

from projects.models import Project, ProjectAssignment
from .core_factories import ClientProfileFactory, FreelancerProfileFactory

fake = Faker()

class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.LazyFunction(lambda: fake.catch_phrase() + " Project")
    description = factory.Faker('paragraph', nb_sentences=5)
    state = factory.Iterator(['CREATED', 'PAID', 'IN_PROGRESS', 'DELIVERED', 'CANCELED'])
    client = factory.SubFactory(ClientProfileFactory)

class ProjectAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectAssignment

    id = factory.LazyFunction(uuid.uuid4)
    project = factory.SubFactory(ProjectFactory)
    freelancer = factory.SubFactory(FreelancerProfileFactory)
    role = factory.Iterator([
        'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
        'UI/UX Designer', 'Project Manager', 'DevOps Engineer', 'QA Tester',
        'Data Scientist', 'Mobile Developer', 'Technical Writer'
    ])
    agreed_payment = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True, min_value=500, max_value=9999)
    state = factory.Iterator(['INVITED', 'ACCEPTED', 'REJECTED', 'REMOVED'])
