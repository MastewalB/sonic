from django.db import models
# Create your models here.


class Podcast(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    podcastUrl = models.URLField()


class Episode(models.Model):
    episodeUrl = models.URLField()
    podcastUrl = models.URLField()


class PodcastSubscription(models.Model):
    user = models.CharField(max_length=255)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE,)
