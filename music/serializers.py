from rest_framework import serializers
from music.models import Artist, Album, Song


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'picture']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'artist', 'name', 'cover']


class SongSerializer(serializers.ModelSerializer):
    song_file = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ['id', 'title', 's_artist',
                  's_album', 'song_file', 'content_type']

    def get_song_file(self, obj):
        request = self.context.get('request')
        file_url = obj.song_file.url
        if request is not None:
            return request.build_absolute_uri(file_url)
        return file_url
