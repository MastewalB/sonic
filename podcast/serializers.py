from rest_framework import serializers
from podcast.models import Podcast, Episode, PodcastSubscription, PodcastProvider


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['podcast_id', 'provider', 'podcastUrl']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['episodeUrl', 'podcastUrl']


class CreateSubscriptionSerializer(serializers.Serializer):
    podcast_provider = serializers.CharField(required=True)
    podcast_id = serializers.CharField(required=True)
    podcast_url = serializers.URLField(required=True)
    episodes_listened = serializers.IntegerField(default=0)


class SubscriptionSerializer(serializers.ModelSerializer):
    podcast = PodcastSerializer(
        read_only=True
    )

    class Meta:
        model = PodcastSubscription
        fields = ['id', 'podcast', 'episodes_listened']
        read_only_fields = ['id', 'user']
        depth = 1


class UpdateSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PodcastSubscription
        fields = ['id', 'episodes_listened']
        read_only_fields = ['user']


class PodcastProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastProvider
        fields = ['name']
