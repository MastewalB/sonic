from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from playlists.serializers import PlaylistSerializer, PlaylistItemsSerializer, CreatePlaylistSerializer, PlaylistDetailSerializer
from playlists.models import Playlist, PlaylistItems
from music.models import Song
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

# Create your views here.


class CreatePlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePlaylistSerializer(data=request.data)
        serializer.context['created_by'] = request.user
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserPlaylistView(APIView):
    def get(self, request, user_id):
        items = Playlist.objects.filter(created_by=user_id)
        serializer = PlaylistDetailSerializer(items, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, playlist_id):
        item = get_object_or_404(Playlist, id=playlist_id)
        serializer = PlaylistDetailSerializer(item)
        serializer.context['request'] = request

        return Response(data=serializer.data)

    def delete(self, request, playlist_id):
        playlist = None
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if playlist.created_by.id == request.user.id:
            playlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PlaylistItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PlaylistItemsSerializer(data=request.data)

        if serializer.is_valid():
            playlist = None
            try:
                playlist = serializer.validated_data['playlist_id']
                song = serializer.validated_data['song_id']
            except (Playlist.DoesNotExist, Song.DoesNotExist) as error:
                return Response(status=status.HTTP_404_NOT_FOUND)

            if request.user.id != playlist.created_by.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = PlaylistItemsSerializer(data=request.data)
        playlist_item = None
        if serializer.is_valid():
            playlist_item = PlaylistItems.objects.get(
                playlist_id=serializer.validated_data['playlist_id'], song_id=serializer.validated_data['song_id'])

            if request.user.id != serializer.validated_data['playlist_id'].created_by.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            playlist_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
