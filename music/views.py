from django.shortcuts import render
from .serializers import SongSerializer, AlbumSerializer, ArtistSerializer
from .models import Song, Album, Artist
from rest_framework import generics, permissions, viewsets
from django.http import StreamingHttpResponse

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAdminUser]

class SongGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        song = self.get_object()
        response = StreamingHttpResponse(song.song_file, content_type=song.content_type)
        response['Content-Disposition'] = f'attachment; filename="{song.title}.mp3"'
        return response

#####  Album   #####

class AlbumGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAdminUser]

#####  Artist  ######
class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAdminUser]

class ArtistGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset
