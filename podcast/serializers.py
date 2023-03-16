from rest_framework import serializers
from podcast.models import Podcast, Episode, PodcastSubscription


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['id', 'podcastUrl']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['episodeUrl', 'podcastUrl']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastSubscription
        fields = ['user', 'podcast']
