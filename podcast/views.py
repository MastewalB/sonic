from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from podcast.models import Podcast, Episode, PodcastSubscription
from podcast.serializers import PodcastSerializer, EpisodeSerializer, SubscriptionSerializer

# Create your views here.


class PodcastView(APIView):
    def post(self, request):
        serializer = PodcastSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriptionView(APIView):
    def post(self, request):

        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def put(self, request):

        subscription = PodcastSubscription.objects.filter(
            user=request.data['user_id'], podcast=request.data['podcast_id']).first()
        if subscription == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriptionSerializer(subscription, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request):

        try:
            subscription = PodcastSubscription.objects.filter(
                user=request.data['user_id'], podcast=request.data['podcast_id']).first()
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SubscriptionListView(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = PageNumberPagination

    def get(self):
        user_id = self.request.query_params.get('user_id', None)
        queryset = PodcastSubscription.objects.filter(user=user_id)
        return queryset
