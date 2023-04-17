import uuid
from django.db import models
from users.models import User
# Create your models here.


class PodcastProvider(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True)

    def __str__(self):
        return self.name


class Podcast(models.Model):
    podcast_id = models.CharField(max_length=200)
    provider = models.ForeignKey(PodcastProvider, on_delete=models.CASCADE)
    podcastUrl = models.URLField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['podcast_id', 'provider'], name='unique_podcast')
        ]

    def __str__(self):
        return "{0} from {1}".format(self.podcast_id, self.provider)


class Episode(models.Model):
    episodeUrl = models.URLField()
    podcastUrl = models.URLField()


class PodcastSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    episodes_listened = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'podcast'], name='unique_subscription')
        ]

    def __str__(self):
        return "{0}'s Subscription to the {1} podcast".format(self.user, self.podcast)
