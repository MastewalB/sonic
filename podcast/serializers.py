from rest_framework import serializers
from podcast.models import Podcast, Episode, PodcastSubscription

class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast 
        fields = ['podcastUrl']
    

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode 
        fields = ['episodeUrl', 'podcastUrl']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastSubscription
        fields = ['']