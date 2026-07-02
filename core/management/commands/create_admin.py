from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from core.models import BloodInventory

        User = get_user_model()
        username = 'admin'
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'changeme123')
        email = 'admin@example.com'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write('Superuser created!')
        else:
            self.stdout.write('Superuser already exists.')

        blood_types = [
            {'blood_type': 'A+', 'units_available': 45, 'minimum_threshold': 15},
            {'blood_type': 'A-', 'units_available': 12, 'minimum_threshold': 10},
            {'blood_type': 'B+', 'units_available': 30, 'minimum_threshold': 15},
            {'blood_type': 'B-', 'units_available': 8, 'minimum_threshold': 10},
            {'blood_type': 'AB+', 'units_available': 18, 'minimum_threshold': 8},
            {'blood_type': 'AB-', 'units_available': 5, 'minimum_threshold': 8},
            {'blood_type': 'O+', 'units_available': 60, 'minimum_threshold': 20},
            {'blood_type': 'O-', 'units_available': 14, 'minimum_threshold': 15},
        ]

        for item in blood_types:
            if not BloodInventory.objects.filter(blood_type=item['blood_type']).exists():
                BloodInventory.objects.create(**item)
                self.stdout.write('Added ' + item['blood_type'])
            else:
                self.stdout.write(item['blood_type'] + ' already exists.')