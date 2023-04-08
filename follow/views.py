from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from follow.serializers import FollowSerializer, FollowerListSerializer
from follow.models import Follow

# Create your views here.


class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.context['follower'] = request.user
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


    def delete(self, request):
        try:
            follower = request.user
            follow = Follow.objects.filter(
                follower=follower,
                followee=request.data['followee_id'])
            follow.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class FollowDetailView(APIView):
    def get(self, request, followee_id):
        try:
            queryset = Follow.objects.filter(followee=followee_id)
            followers = FollowSerializer(data=queryset, many=True)
            return Response(
                followers.data,
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class FollowDetailListView(ListAPIView):
    serializer_class = FollowerListSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        followee_id = self.request.data['followee_id']
        queryset = Follow.objects.filter(followee=followee_id)
        return queryset
