from rest_framework import serializers
from music.models import Artist, Album, Song

class ArtistSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['id', 'name', 'picture', 'albums']

    def get_albums(self, obj):
        albums = Album.objects.filter(artist=obj.id)
        return AlbumInfoSerializer(albums, many=True).data


class AlbumInfoSerializer(serializers.ModelSerializer):
    # artist = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ('id', 'name', 'cover')

    # def get_artist(self, obj):
    #     return ArtistSerializer(obj.artist, context=self.context).data
class AlbumSerializer(serializers.ModelSerializer):
    songs = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()
    class Meta:
        model = Album
        fields = ['id', 'artist', 'name', 'cover', 'songs']

    def get_songs(self, obj):
        songs = Song.objects.filter(s_album=obj.id)
        return SongSerializer(songs, many=True, context=self.context).data
    def get_artist(self, obj):
        return ArtistSerializer(obj.artist, context=self.context).data


class SongSerializer(serializers.ModelSerializer):
    # song_file = serializers.SerializerMethodField()
    s_album = serializers.SerializerMethodField()
    s_artist = serializers.SerializerMethodField()
    class Meta:
        model = Song
        fields = ['id', 'title', 's_artist', 's_album', 'song_file', 'content_type', 'fingerprint']

    def get_s_album(self, obj):
        return AlbumInfoSerializer(obj.s_album, context = self.context).data
    def get_s_artist(self, obj):
        return ArtistSerializer(obj.s_artist, context = self.context).data
    # def get_song_file(self, obj):
