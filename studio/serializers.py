from rest_framework import fields, serializers
from studio.models import *
from users.serializers import UserPublicSerializer


class GenreSerializer(serializers.ModelSerializer):
    pass


class StudioEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioEpisode
        fields = ('id', 'index', 'title', 'description',
                  'podcast', 'upload_date', 'file')
        read_only_fields = [
            'id', 'index'
        ]

    def create(self, validated_data):
        episode = StudioEpisode(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            podcast=self.validated_data['podcast'],
            file=self.validated_data['file'],
        )

        episode.save()
        return episode

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class StudioPodcastSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = StudioPodcast
        fields = '__all__'
        read_only_fields = [
            'id', 'author', 'episodes', 'number_of_episodes'
        ]
        depth = 1

    def get_episodes(self, obj):
        episodes = StudioEpisode.objects.filter(
            podcast=obj.id)
        return StudioEpisodeSerializer(episodes, many=True).data

    def get_author(self, obj):
        return UserPublicSerializer(obj.author).data

    def create(self, validated_data):
        podcast = StudioPodcast(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            author=self.context['author'],
            genre=self.validated_data['genre']
        )
        podcast.save()
        return podcast

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class DeleteStudioItemSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
