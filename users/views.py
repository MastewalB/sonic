from django.shortcuts import render, get_object_or_404
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer, LoginSerializer
from users.utils import Utils
from users.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

# Create your views here.


class SignupView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        data = request.data
        email = data['email']

        serializer = UserSerializer(data=data)

        serializer.save()

        user = User.objects.get(email=email)
        token = Utils.enconde_token(user)
        return Response(
            {
                'data': serializer.data,
                'token': token
            }
        )


class LoginView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = Utils.authenticate_user(serializer.validated_data)
        serialized_user = UserSerializer(user)
        token = Utils.enconde_token(user)

        return Response(
            {
                "data": serialized_user.data,
                "token": token
            }
        )


# class UpdateProfile(APIView)
