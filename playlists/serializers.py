from rest_framework import serializers
from playlists.models import Playlist

class PlaylistSerialier(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['created_by', 'songItem', 'podcast_item', 'playlist_title']
        