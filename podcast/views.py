from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status 
from rest_framework.pagination import PageNumberPagination
from podcast.models import Podcast, Episode
from podcast.serializers import PodcastSerializer, EpisodeSerializer

# Create your views here.



class PodcastView(APIView):
    def post(self, request):
        serializer = PodcastSerializer(data= request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) 

class SubscriptionView(APIView):
    def get(self, request):
        
        return