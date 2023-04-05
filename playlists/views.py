from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from playlists.serializers import PlaylistSerializer, PlaylistItemsSerializer
from playlists.models import Playlist, PlaylistItems

# Create your views here.
class PlaylistView(APIView):
    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            # serializer.data['created_by'] = request.user
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        playlist_id = request.query_params['playlist-id']
        items = PlaylistItems.objects.filter(playlist_id=playlist_id)
        serializer = PlaylistItemsSerializer(items, many=True)

        return Response(data=serializer.data)
    
    def delete(self, request):
        serializer = PlaylistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_by = Playlist.objects.get(id=serializer.id).created_by
        if created_by == request.data.created_by:
            playlist = get_object_or_404(Playlist, playlist_id=serializer.data.playlist_id)
            playlist.delete()

            return Response(status= status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

class PlaylistItemsView(APIView):
    def post(self, request):
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