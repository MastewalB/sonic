from django.core import serializers as d_serializers
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from podcast.models import Podcast, Episode, PodcastSubscription, PodcastProvider
from podcast.serializers import PodcastSerializer, EpisodeSerializer, SubscriptionSerializer, CreateSubscriptionSerializer, UpdateSubscriptionSerializer

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


class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateSubscriptionSerializer(data=request.data)
        if serializer.is_valid():

            podcast_url = serializer.validated_data['podcast_url']

            podcast_provider = PodcastProvider.objects.get_or_create(
                name=serializer.validated_data['podcast_provider'])[0]

            podcast = Podcast.objects.get_or_create(
                provider=podcast_provider, podcast_id=serializer.validated_data['podcast_id'], podcastUrl=podcast_url)[0]
            episodes_listened = serializer.validated_data['episodes_listened']

            subscription = PodcastSubscription.objects.get_or_create(
                podcast=podcast, user=request.user)[0]
            # subscription = subscription.
            subscription = d_serializers.serialize('python', [subscription])[0]

            return Response(
                subscription['fields'],
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'message': 'Please provide all fields.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):

        serializer = UpdateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            subscription = PodcastSubscription.objects.get(
                id=request.data['id'])
            if subscription.user != request.user:
                return Response(
                    {
                        "message": "Unauthorized Access"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        except PodcastSubscription.DoesNotExist:
            return Response(
                {
                    "message": "No Such Subscription"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer.update(subscription, serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        serializer = UpdateSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            subscription = PodcastSubscription.objects.get(
                id=request.data['id'])
            if subscription.user != request.user:
                return Response(
                    {
                        "message": "Unauthorized Access"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        except PodcastSubscription.DoesNotExist:
            return Response(
                {
                    "message": "No Such Subscription"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        subscription.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = SubscriptionSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = PodcastSubscription.objects.filter(user=user_id)
        return queryset
