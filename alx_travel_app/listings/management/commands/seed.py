from django.core.management.base import BaseCommand
from django_seed import Seed
from django.utils import timezone
from listings.models import Listing, Booking, Review

import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with sample data for listings, bookings, and reviews.'

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        self.stdout.write("Starting database seeding...")

        self.stdout.write(self.style.SUCCESS('Seeding Listings...'))
        seeder.add_entity(Listing, 20, {
            'host': lambda x: seeder.faker.email(),
            'name': lambda x: seeder.faker.word().capitalize() + ' House',
            'description': lambda x: seeder.faker.paragraph(nb_sentences=3),
            'location': lambda x: seeder.faker.city(),
            'pricepernight': lambda x: random.randint(50, 500),
            'created_at': lambda x: timezone.make_aware(seeder.faker.date_time_between(start_date='-2y', end_date='now')),
            'updated_at': lambda x: timezone.make_aware(seeder.faker.date_time_between(start_date='now', end_date='+2y')),
        })

        self.stdout.write(self.style.SUCCESS('Seeding Bookings...'))
        seeder.add_entity(Booking, 30, {
            'listing_id': lambda x: seeder.faker.random_element(Listing.objects.all()),
            'user': lambda x: seeder.faker.email(),
            'start_date': lambda x: seeder.faker.date_between(start_date='-30d', end_date='today'),
            'end_date': lambda x: seeder.faker.date_between(start_date='today', end_date='+30d'),
            'total_price': lambda x: random.randint(100, 1000),
            'status': lambda x: seeder.faker.random_element(elements=('pending', 'confirmed', 'canceled')),
        })

        self.stdout.write(self.style.SUCCESS('Seeding Reviews...'))
        seeder.add_entity(Review, 40, {
            'listing_id': lambda x: seeder.faker.random_element(Listing.objects.all()),
            'user': lambda x: seeder.faker.email(),
            'rating': lambda x: random.randint(1, 5),
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS('Database seeding completed!'))
