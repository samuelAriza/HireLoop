from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from faker import Faker
import random
from factories.core_factories import UserFactory, ClientProfileFactory, FreelancerProfileFactory, PortfolioItemFactory
from factories.services_factories import (
    CategoryFactory, MicroserviceFactory, CartFactory, CartItemFactory,
    WishListFactory, WishListItemFactory, OrderMicroServiceFactory, ReviewFactory
)
from factories.projects_factories import ProjectFactory, ProjectAssignmentFactory
from factories.mentorship_factories import MentorShipSessionFactory
from factories.payments_factories import PaymentMethodFactory, PaymentFactory

# Import models
from services.models import Category

fake = Faker()

class Command(BaseCommand):
    help = 'Generate dummy data for testing the application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=20,
            help='Number of users to create',
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=10,
            help='Number of categories to create',
        )
        parser.add_argument(
            '--services',
            type=int,
            default=50,
            help='Number of microservices to create',
        )
        parser.add_argument(
            '--projects',
            type=int,
            default=15,
            help='Number of projects to create',
        )
        parser.add_argument(
            '--mentorship',
            type=int,
            default=25,
            help='Number of mentorship sessions to create',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()
            
        self.stdout.write(self.style.SUCCESS('Starting data generation...'))
        
        # Generate basic data
        users = self.generate_users(options['users'])
        categories = self.generate_categories(options['categories'])
        
        # Generate services and related data
        services = self.generate_services(options['services'], categories)
        self.generate_service_related_data(services, users)
        
        # Generate projects
        projects = self.generate_projects(options['projects'])
        
        # Generate mentorship sessions
        self.generate_mentorship_sessions(options['mentorship'])
        
        # Generate payments
        self.generate_payments()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated dummy data:\n'
                f'- {options["users"]} users (clients & freelancers)\n'
                f'- {options["categories"]} categories\n'
                f'- {options["services"]} microservices\n'
                f'- {options["projects"]} projects\n'
                f'- {options["mentorship"]} mentorship sessions\n'
                f'- Various related data (orders, reviews, payments, etc.)'
            )
        )

    def clear_data(self):
        """Clear existing data"""
        from core.models import User
        from services.models import Category, Microservice, Cart, WishList, OrderMicroService, Review
        from projects.models import Project, ProjectAssignment
        from mentorship.models import MentorShipSession
        from payments.models import Payment, PaymentMethod
        
        # Clear in reverse dependency order
        Payment.objects.all().delete()
        PaymentMethod.objects.all().delete()
        Review.objects.all().delete()
        OrderMicroService.objects.all().delete()
        ProjectAssignment.objects.all().delete()
        Project.objects.all().delete()
        MentorShipSession.objects.all().delete()
        Cart.objects.all().delete()
        WishList.objects.all().delete()
        Microservice.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(self.style.SUCCESS('Data cleared successfully'))

    def generate_users(self, count):
        """Generate users with profiles"""
        self.stdout.write(f'Generating {count} users...')
        
        users = []
        for i in range(count):
            user = UserFactory()
            users.append(user)
            
            # Randomly create client or freelancer profiles (or both)
            if random.choice([True, False]):
                ClientProfileFactory(user=user)
            
            if random.choice([True, False]):
                freelancer = FreelancerProfileFactory(user=user)
                # Add some portfolio items
                for _ in range(random.randint(1, 4)):
                    PortfolioItemFactory(freelancer=freelancer)
        
        return users

    def generate_categories(self, count):
        """Generate service categories"""
        self.stdout.write(f'Generating {count} categories...')
        
        # Predefined categories to ensure uniqueness
        category_data = [
            ('Web Development', 'web-development'),
            ('Mobile Development', 'mobile-development'),
            ('Data Science', 'data-science'),
            ('Machine Learning', 'machine-learning'),
            ('UI/UX Design', 'ui-ux-design'),
            ('Digital Marketing', 'digital-marketing'),
            ('Content Writing', 'content-writing'),
            ('Translation', 'translation'),
            ('Video Editing', 'video-editing'),
            ('Graphic Design', 'graphic-design'),
            ('SEO Services', 'seo-services'),
            ('Social Media Management', 'social-media-management'),
            ('DevOps & Cloud', 'devops-and-cloud'),
            ('Cybersecurity', 'cybersecurity'),
            ('Blockchain Development', 'blockchain-development')
        ]
        
        categories = []
        for i, (name, slug) in enumerate(category_data[:count]):
            category = Category.objects.create(
                name=name,
                slug=slug
            )
            categories.append(category)
        
        return categories

    def generate_services(self, count, categories):
        """Generate microservices"""
        self.stdout.write(f'Generating {count} microservices...')
        
        services = []
        for _ in range(count):
            service = MicroserviceFactory(category=random.choice(categories))
            services.append(service)
        
        return services

    def generate_service_related_data(self, services, users):
        """Generate orders, reviews, carts, wishlists"""
        self.stdout.write('Generating service-related data...')
        
        # Generate orders and reviews
        for _ in range(random.randint(20, 50)):
            order = OrderMicroServiceFactory(
                micro_service=random.choice(services)
            )
            
            # 70% chance of having a review for delivered orders
            if order.state == 'DELIVERED' and random.random() < 0.7:
                ReviewFactory(order=order)
        
        # Generate carts and cart items for some users
        for user in random.sample(users, min(len(users), 10)):
            if hasattr(user, 'cart'):
                continue
            cart = CartFactory(user=user)
            selected_services = random.sample(services, min(len(services), random.randint(1, 5)))
            for service in selected_services:
                try:
                    CartItemFactory(
                        cart=cart,
                        micro_service=service
                    )
                except Exception:
                    # Skip if already exists
                    continue
        
        # Generate wishlists for some users
        for user in random.sample(users, min(len(users), 15)):
            if hasattr(user, 'wishlist'):
                continue
            wishlist = WishListFactory(user=user)
            selected_services = random.sample(services, min(len(services), random.randint(1, 8)))
            for service in selected_services:
                try:
                    WishListItemFactory(
                        wish_list=wishlist,
                        micro_service=service
                    )
                except Exception:
                    # Skip if already exists
                    continue

    def generate_projects(self, count):
        """Generate projects and assignments"""
        self.stdout.write(f'Generating {count} projects...')
        
        projects = []
        for _ in range(count):
            project = ProjectFactory()
            projects.append(project)
            
            # Add some project assignments
            for _ in range(random.randint(1, 5)):
                ProjectAssignmentFactory(project=project)
        
        return projects

    def generate_mentorship_sessions(self, count):
        """Generate mentorship sessions"""
        self.stdout.write(f'Generating {count} mentorship sessions...')
        
        for _ in range(count):
            MentorShipSessionFactory()

    def generate_payments(self):
        """Generate payment methods and payments"""
        self.stdout.write('Generating payment data...')
        
        # Generate payment methods for random users
        User = get_user_model()
        users = User.objects.all()
        
        for user in random.sample(list(users), min(len(users), 15)):
            for _ in range(random.randint(1, 3)):
                PaymentMethodFactory(user=user)
        
        # Generate some simple payments without complex relationships
        for _ in range(random.randint(10, 30)):
            try:
                payment = PaymentFactory.build()
                # Don't use the post_generation method that causes issues
                payment.save()
            except Exception:
                # Skip on error
                continue