from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'admin'
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'changeme123')
        email = 'admin@example.com'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write('Superuser created!')
        else:
            self.stdout.write('Superuser already exists.')