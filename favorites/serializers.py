from rest_framework import serializers
from favorites.models import LikedSongsPlaylist


class LikedSongsPlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikedSongsPlaylist
        fields = ( 'user_id')
