from rest_framework import fields, serializers
from studio.models import *
from users.serializers import UserPublicSerializer


class GenreSerializer(serializers.ModelSerializer):
    pass


class StudioPodcastInfoSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = StudioPodcast
        fields = ('id', 'title', 'author', 'description',
                  'genre', 'number_of_episodes')

    def get_author(self, obj):
        return UserPublicSerializer(obj.author, context=self.context).data


class StudioEpisodeSerializer(serializers.ModelSerializer):
    podcast_id = serializers.CharField()
    podcast = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = StudioEpisode
        fields = ('id', 'index', 'title', 'description', 'podcast',
                  'upload_date', 'file', 'podcast_id')
        read_only_fields = [
            'id', 'index', 'podcast', 'upload_date'
        ]
        depth = 2

    def create(self, validated_data):
        episode = StudioEpisode(
            title=self.validated_data['title'],
            description=self.validated_data['description'],
            podcast=self.context['podcast'],
            file=self.validated_data['file'],
        )

        episode.save()
        return episode

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_podcast(self, obj):
        return StudioPodcastInfoSerializer(obj.podcast, context=self.context).data

    def get_file(self, obj):
        request = self.context.get('request')
        file_url = obj.file.url
        if request is not None:
            return request.build_absolute_uri(file_url)
        return file_url


class StudioPodcastSerializer(serializers.ModelSerializer):
    episodes = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = StudioPodcast
        fields = '__all__'
        read_only_fields = [
            'id', 'author', 'episodes', 'number_of_episodes'
        ]
        depth = 2

    def get_episodes(self, obj):
        episodes = StudioEpisode.objects.filter(
            podcast=obj.id)
        return StudioEpisodeSerializer(episodes, many=True, context=self.context).data

    def get_author(self, obj):
        return UserPublicSerializer(obj.author, context=self.context).data

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
