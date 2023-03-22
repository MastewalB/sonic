from rest_framework import serializers
from playlists.models import Playlist, PlaylistItems

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['playlist_title']

        read_only_fields = ['created_by', 'id']

class PlaylistItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistItems
        fields = ['playlist_id', 'song_id']