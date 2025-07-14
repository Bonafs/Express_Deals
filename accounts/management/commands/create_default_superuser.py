from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates the default superuser from credentials.template.py'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = '527626@waes.ac.uk'
        password = 'Mobolaji'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
