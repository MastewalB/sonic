from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from playlists.serializers import PlaylistSerialier
from playlists.models import Playlist

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
        serialize = PlaylistSerialier(playlist)

        return Response(serialize.data)
    
    def delete(self, playlist_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        playlist.delete()

        return Response(status= status.HTTP_204_NO_CONTENT)