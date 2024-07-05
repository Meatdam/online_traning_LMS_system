import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from base.settings import ENV_PATH
from users.models import User

load_dotenv(ENV_PATH)


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('ADMIN_EMAIL'),
            first_name='Admin',
            last_name='Ilya',
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('POSTGRES_PASSWORD'))
        user.save()
