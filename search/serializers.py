from rest_framework import serializers
from music.serializers import AlbumSerializer, ArtistSerializer, SongSerializer
from .models import Search


class SearchSerializer(serializers.Serializer):
    type = serializers.CharField()
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        if obj['type'] == 'album':
            serializer = AlbumSerializer(obj['data'])
        elif obj['type'] == 'artist':
            serializer = ArtistSerializer(obj['data'])
        elif obj['type'] == 'song':
            serializer = SongSerializer(obj['data'])
        else:
            raise ValueError(f"Invalid type: {obj['type']}")

        return serializer.data
