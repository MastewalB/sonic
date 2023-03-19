from rest_framework import serializers
from playlists.models import Playlist, PlaylistItems

class PlaylistSerialier(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['created_by', 'playlist_id', 'playlist_title']

class PlaylistItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistItems
        fields = ['playlist_id', 'song_id']