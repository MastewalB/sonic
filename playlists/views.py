from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from playlists.serializers import PlaylistSerialier, PlaylistItemsSerializer
from playlists.models import Playlist, PlaylistItems

# Create your views here.
class PlaylistView(APIView):
    def post(self, request):
        serializer = PlaylistSerialier(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, playlist_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        serialize = PlaylistItemsSerializer(playlist)

        return Response(serialize.data)
    
    def delete(self, playlist_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        playlist.delete()

        return Response(status= status.HTTP_204_NO_CONTENT)

class PlaylistItemsView(APIView):
    def post(self, request):
        serializer = PlaylistItemsSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)        

    def get(self, playlist_id, song_id):
        playlist = get_object_or_404(PlaylistItems, pk=playlist_id)
        serialize = PlaylistItemsSerializer(playlist)

        return Response(serialize.data)
