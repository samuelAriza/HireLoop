from django.core.management.base import BaseCommand
from core.factory_boy.user_factory import UserFactory
from core.factory_boy.freelancer_factory import FreelancerProfileFactory
from core.factory_boy.client_factory import ClientProfileFactory
from microservices.factory_boy.category_factory import CategoryFactory
from microservices.factory_boy.microservice_factory import MicroServiceFactory
from mentorship_session.factory_boy.mentorship_factory import MentorshipSessionFactory
from projects.factory_boy.project_factory import (
    ProjectFactory,
    ProjectAssignmentFactory,
    ProjectApplicationFactory,
)
from payments.factory_boy.payment_factory import PaymentFactory
from cart.factory_boy.cart_factory import CartItemFactory, WishlistItemFactory

import factory
import random
import itertools


class Command(BaseCommand):
    help = "Populate the database with dummy data using factories"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=5)
        parser.add_argument("--freelancers", type=int, default=3)
        parser.add_argument("--clients", type=int, default=3)
        parser.add_argument("--categories", type=int, default=3)
        parser.add_argument("--microservices", type=int, default=10)
        parser.add_argument("--mentorships", type=int, default=5)
        parser.add_argument("--projects", type=int, default=5)
        parser.add_argument("--assignments", type=int, default=10)
        parser.add_argument("--applications", type=int, default=10)
        parser.add_argument("--payments", type=int, default=10)
        parser.add_argument("--cart_items", type=int, default=10)
        parser.add_argument("--wishlist_items", type=int, default=5)

    def handle(self, *args, **options):
        # --- Freelancers ---
        self.stdout.write("Creating Freelancers...")
        users_for_freelancers = UserFactory.create_batch(options["freelancers"])
        freelancers = [FreelancerProfileFactory(user=user) for user in users_for_freelancers]

        # --- Clients ---
        self.stdout.write("Creating Clients...")
        users_for_clients = UserFactory.create_batch(options["clients"])
        clients = [ClientProfileFactory(user=user) for user in users_for_clients]

        # --- Categories ---
        self.stdout.write("Creating Categories...")
        categories = CategoryFactory.create_batch(options["categories"])

        # --- MicroServices ---
        self.stdout.write("Creating MicroServices...")
        microservices = [
            MicroServiceFactory(
                freelancer=random.choice(freelancers),
                category=random.choice(categories)
            )
            for _ in range(options["microservices"])
        ]

        # --- Mentorship Sessions ---
        self.stdout.write("Creating Mentorship Sessions...")
        mentorships = [
            MentorshipSessionFactory(
                mentor=random.choice(freelancers),
                mentee=random.choice(clients)
            )
            for _ in range(options["mentorships"])
        ]

        # --- Projects ---
        self.stdout.write("Creating Projects...")
        projects = [
            ProjectFactory(client=random.choice(clients))
            for _ in range(options["projects"])
        ]

        # --- Project Assignments ---
        self.stdout.write("Creating Project Assignments...")
        assignments = [
            ProjectAssignmentFactory(
                project=random.choice(projects),
                freelancer=random.choice(freelancers)
            )
            for _ in range(options["assignments"])
        ]

        # --- Project Applications (evitar duplicados) ---
        self.stdout.write("Creating Project Applications...")
        possible_pairs = list(itertools.product(projects, freelancers))
        random.shuffle(possible_pairs)
        num_applications = min(options["applications"], len(possible_pairs))
        applications = [
            ProjectApplicationFactory(project=proj, freelancer=free)
            for proj, free in possible_pairs[:num_applications]
        ]

        # --- Payments ---
        self.stdout.write("Creating Payments...")
        all_users = users_for_freelancers + users_for_clients
        payments = [
            PaymentFactory(user=random.choice(all_users))
            for _ in range(options["payments"])
        ]

        # --- Cart Items (evitar duplicados) ---
        self.stdout.write("Creating Cart Items...")
        content_objects = microservices + mentorships
        possible_cart_pairs = list(itertools.product(all_users, content_objects))
        random.shuffle(possible_cart_pairs)
        num_cart_items = min(options["cart_items"], len(possible_cart_pairs))
        cart_items = [
            CartItemFactory(user=user, content_object=obj)
            for user, obj in possible_cart_pairs[:num_cart_items]
        ]

        # --- Wishlist Items (evitar duplicados) ---
        self.stdout.write("Creating Wishlist Items...")
        possible_wishlist_pairs = list(itertools.product(all_users, content_objects))
        random.shuffle(possible_wishlist_pairs)
        num_wishlist_items = min(options["wishlist_items"], len(possible_wishlist_pairs))
        wishlist_items = [
            WishlistItemFactory(user=user, content_object=obj)
            for user, obj in possible_wishlist_pairs[:num_wishlist_items]
        ]

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))