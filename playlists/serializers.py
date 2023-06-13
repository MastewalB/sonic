from rest_framework import serializers
from playlists.models import Playlist, PlaylistItems
from music.models import Song
from music.serializers import SongSerializer
from users.serializers import UserPublicSerializer


class CreatePlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['created_by', 'playlist_title', 'id']
        read_only_fields = ['created_by', 'id']

    def create(self, validated_data):
        playlist = Playlist(
            created_by=self.context['created_by'],
            playlist_title=validated_data['playlist_title']
        )

        playlist.save()
        return playlist


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['playlist_title', 'created_by', 'id']

        read_only_fields = ['created_by', 'id']


class PlaylistItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaylistItems
        fields = ['playlist_id', 'song_id']


class PlaylistDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id', 'playlist_title', 'created_by', 'items')
        read_only_fields = ['created_by', 'id']
        depth = 2

    def get_items(self, obj):
        items = PlaylistItems.objects.filter(playlist_id=obj.id)
        songs = []
        for item in items:
            songs.append(item.song_id)
        return SongSerializer(songs, many=True, context=self.context).data

    def get_created_by(self, obj):
        return UserPublicSerializer(obj.created_by, context=self.context).data
