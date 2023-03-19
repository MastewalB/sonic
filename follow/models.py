from django.db import models
from users.models import User

# Create your models here.


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followee = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followee'])
        ]
