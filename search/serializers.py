from rest_framework import serializers
from music.serializers import AlbumSerializer, ArtistSerializer, SongSerializer
from users.serializers import UserPublicSerializer
from .models import Search


class SearchSerializer(serializers.Serializer):
    type = serializers.CharField()
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        if obj['type'] == 'album':
            serializer = AlbumSerializer(obj['data'], context = self.context)
        elif obj['type'] == 'artist':
            serializer = ArtistSerializer(obj['data'], context = self.context)
        elif obj['type'] == 'song':
            serializer = SongSerializer(obj['data'], context = self.context)
        elif obj['type'] == 'user':
            serializer = UserPublicSerializer(obj['data'], context = self.context)
        else:
            raise ValueError(f"Invalid type: {obj['type']}")

        return serializer.data
