from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from studio.models import StudioEpisode, StudioPodcast, Genre
from studio.serializers import StudioPodcastSerializer, StudioEpisodeSerializer, GenreSerializer, DeleteStudioItemSerializer

# Create your views here.


class GenreView(APIView):

    def get(self, request):
        genre_items = Genre.objects.all()
        serializer = GenreSerializer(genre_items, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetStudioPodcastView(APIView):
    """
    Show detail info for a single Podcast
    """
    permission_classes = [AllowAny]

    def get(self, request, podcast_id):
        podcast = get_object_or_404(StudioPodcast, id=podcast_id)
        episodes = StudioEpisode.objects.filter(podcast=podcast)

        podcast_serializer = StudioPodcastSerializer(podcast)

        protocol = "https" if request.is_secure() else "http"
        return Response(
            {
                "podcast": podcast_serializer.data,
                "rss_feed_url": "{0}://{1}/api/v1/studio/podcasts/feed/rss/{2}".format(protocol, get_current_site(request).domain, podcast.slug),
                "atom_feed_url": "{0}://{1}/api/v1/studio/podcasts/feed/atom/{2}".format(protocol, get_current_site(request).domain, podcast.slug)
            },
            status=status.HTTP_200_OK
        )


class StudioPodcastView(APIView):
    """
    Create, Update, Delete
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StudioPodcastSerializer(data=request.data)
        serializer.context['author'] = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):

        if 'id' not in request.data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        podcast = get_object_or_404(StudioPodcast, id=request.data['id'])
        if podcast.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StudioPodcastSerializer(podcast, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.context['author'] = request.user
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        serializer = DeleteStudioPodcastSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        podcast = get_object_or_404(
            StudioPodcast, id=serializer.validated_data['id'])
        if podcast.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )

        podcast.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class GetStudioEpisodeView(APIView):
    """
    Show detail info for a single Episode
    """
    permission_classes = [AllowAny]

    def get(self, request, episode_id):
        episode = get_object_or_404(StudioEpisode, id=episode_id)
        episode_serializer = StudioEpisodeSerializer(episode)

        return Response(
            episode_serializer.data,
            status=status.HTTP_200_OK
        )


class StudioEpisodeView(APIView):
    """
    Create, Update, Delete
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StudioEpisodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['podcast'].author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request):
        if 'id' not in request.data:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        episode = get_object_or_404(StudioEpisode, id=request.data['id'])
        serializer = StudioEpisodeSerializer(episode, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        serializer = DeleteStudioItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        episode = get_object_or_404(
            StudioEpisode, id=serializer.validated_data['id'])
        if episode.podcast.author != request.user:
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )

        episode.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class StudioPodcastListView(ListAPIView):
    serializer_class = StudioPodcastSerializer
    queryset = StudioPodcast.objects.all()

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = self.queryset.filter(author=user_id)
        return queryset


class StudioEpisodeListView(ListAPIView):
    serializer_class = StudioEpisodeSerializer

    def get_queryset(self):
        podcast_id = self.kwargs['podcast_id']
        queryset = StudioEpisode.objects.filter(podcast=podcast_id)
        return queryset
