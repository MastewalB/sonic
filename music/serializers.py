from rest_framework import serializers
from music.models import Artist, Album, Song

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name', 'picture']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['artist', 'name', 'cover']


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['title', 's_artist', 's_album', 's_url']