from datetime import datetime, date
from django.test import TestCase
from users.models import User


# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username="sonic_user",
            email='sonic_user@sonic.com',
            first_name="First",
            last_name="User",
            date_of_birth=date(2000, 10, 9),
            country='Ethiopia'
        )
        User.objects.create(
            username="sonic_user_again",
            email='sonic_user_again@sonic.com',
            first_name="Second",
            last_name="User",
            date_of_birth=date(1999, 10, 9),
            country='Svalbard'
        )

    def test_user_info(self):
        u = User.objects.get(username='sonic_user')
        v = User.objects.get(username='sonic_user_again')

        self.assertEqual(u.get_age(), 22)
        self.assertEqual(u.date_of_birth, date(
            2000, 10, 9))
