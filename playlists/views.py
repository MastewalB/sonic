from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from playlists.serializers import PlaylistSerializer, PlaylistItemsSerializer, CreatePlaylistSerializer
from playlists.models import Playlist, PlaylistItems

# Create your views here.
class CreatePlaylistView(APIView):
    def post(self, request):
        serializer = CreatePlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserPlaylistView(APIView):
    def get(self, request, user_id):
        items = Playlist.objects.filter(created_by=user_id)
        serializer = PlaylistSerializer(items, many=True)

        return Response(data=serializer.data)

class PlaylistView(APIView):
    def get(self, request, playlist_id):
        items = PlaylistItems.objects.filter(playlist_id=playlist_id)
        serializer = PlaylistItemsSerializer(items, many=True)

        return Response(data=serializer.data)
    
    def delete(self, request, playlist_id):
        created_by = Playlist.objects.get(pk=playlist_id)
        if created_by == request.data.created_by:
            playlist = get_object_or_404(Playlist, pk=playlist_id)
            playlist.delete()

            return Response(status= status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

class PlaylistItemsView(APIView):
    def post(self, request, pk):
        print("here")
        serializer = PlaylistItemsSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = PlaylistItemsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        playlist_item = PlaylistItems.objects.get(playlist_id=serializer.playlist_id, song_id=serializer.song_id)
        created_by = Playlist.objects.get(id=playlist_item.playlist_id).created_by
        if created_by == request.user.id:
            playlistItem = get_object_or_404(PlaylistItems, playlist_id=serializer.data.playlist_id, song_id=serializer.data.song_id)
            playlistItem.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)