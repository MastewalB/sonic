from django.db import models
# Create your models here.


class Podcast(models.Model):
    podcastUrl = models.URLField()


class Episode(models.Model):
    episodeUrl = models.URLField()
    podcastUrl = models.URLField()


class PodcastSubscription(models.Model):
    userId = models.CharField(max_length=255)
    podcast = models.ForeignKey('podcast', on_delete=models.CASCADE,)

