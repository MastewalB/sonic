from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser with custom fields'

    def handle(self, *args, **options):
        UserModel = get_user_model()
        email = input('Enter Email: ')
        username = input('Enter Username: ')
        birthday = input('Enter Birthday(YYYY-MM-DD): ')
        password = input('Enter Password: ')

        try:
            UserModel.objects.create_superuser(
                username=username,
                email=email,
                date_of_birth=birthday,
                password=password
            )
        except Exception as X:
            self.stdout.write(self.style.ERROR(X.__str__()))
            return

        self.stdout.write(self.style.SUCCESS(
            'Superuser created successfully.'))
