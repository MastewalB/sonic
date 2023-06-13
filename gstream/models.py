import uuid
from django.db import models
from users.models import User

# Create your models here.


class Stream(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '{name}\'s Stream'.format(name=self.user_id.username)
