from django.shortcuts import render
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from follow.models import Follow
from gstream.models import Stream
from users.serializers import UserPublicSerializer

# Create your views here.


class StreamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            stream, created = Stream.objects.get_or_create(
                user_id=request.user)
            return Response({"status": stream.is_active}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:

            stream, created = Stream.objects.get_or_create(
                user_id=request.user)
            stream.is_active = True
            stream.save()

            return Response(
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        try:
            stream, created = Stream.objects.get_or_create(
                user_id=request.user)

            stream.is_active = False
            stream.save()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:

            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class StreamingFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = Follow.objects.filter(
            Q(follower=request.user) | Q(followee=request.user))

        streaming_users = set()
        for friend in friends.iterator():
            if friend.followee != request.user:
                friend_stream, _ = Stream.objects.get_or_create(
                    user_id=friend.followee)
                if friend_stream.is_active:
                    streaming_users.add(friend.followee)
            elif friend.follower != request.user:
                friend_stream, _ = Stream.objects.get_or_create(
                    user_id=friend.follower)
                if friend_stream.is_active:
                    streaming_users.add(friend.follower)

        serializer = UserPublicSerializer(streaming_users, many=True)

        serializer.context['request'] = request
        # serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
