from rest_framework import serializers
from music.models import Artist, Album, Song

class ArtistSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['id', 'name', 'picture']

    def get_albums(self, obj):
        albums = Album.objects.filter(artist=obj.id)
        return AlbumSerializer(albums, many=True).data


class AlbumSerializer(serializers.ModelSerializer):
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'artist', 'name', 'cover', 'songs']

    def get_songs(self, obj):
        songs = Song.objects.filter(s_album=obj.id)
        return SongSerializer(songs, many=True).data


class SongSerializer(serializers.ModelSerializer):
    # song_file = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ['id', 'title', 's_artist', 's_album', 'song_file', 'content_type', 'fingerprint']

    # def get_song_file(self, obj):
