from rest_framework import serializers
from playlists.models import Playlist, PlaylistItems


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
        fields = ['playlist_title']

        read_only_fields = ['created_by', 'id']


class PlaylistItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaylistItems
        fields = ['playlist_id', 'song_id']
