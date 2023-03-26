import uuid
from datetime import datetime, date
from django.db import models
from django.utils import timezone, timesince
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def _create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    # TODO - userId field
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'id'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'date_of_birth', 'country']
    objects = UserManager()

    def get_full_name(self):
        return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)

    def get_short_name(self):
        return '{first_name}'.format(first_name=self.first_name)

    def get_age(self):
        today = date.today()
        y = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or today.month == self.date_of_birth.month and today.day < self.date_of_birth.day:
            y -= 1
        return y

    def __str__(self):
        return self.get_full_name()
