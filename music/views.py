from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import SongSerializer, AlbumSerializer, ArtistSerializer
from .models import Song, Album, Artist
from rest_framework import generics, permissions, viewsets
from django.http import StreamingHttpResponse
import acoustid

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    # permission_classes = [permissions.IsAdminUser] 

    def create(self, request, *args, **kwargs):
        print("here")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new song instance
        self.perform_create(serializer)

        # Generate the fingerprint for the new song
        audio_file = serializer.validated_data['song_file']
        # print(audio_file)
        audio_file_path = audio_file.temporary_file_path()  # Get the file path
        duration, fingerprint = acoustid.fingerprint_file(audio_file_path)
        print(duration, fingerprint)

        # Save the fingerprint to the song instance
        song = serializer.instance
        song.fingerprint = fingerprint
        song.save()

        # Perform the sound search
        # self.sound_search(fingerprint)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
    # permission_classes = [permissions.IsAuthenticated]

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
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset
