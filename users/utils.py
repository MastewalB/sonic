from users.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
import datetime
import os


class Utils:

    @staticmethod
    def enconde_token(user):
        payload = {
            'id': user.id,
            'is_staff': user.is_staff
        }
        token = RefreshToken.for_user(user)
        token.payload['TOKEN_TYPE_CLAIM'] = 'access'
        return {
            'refresh': str(token),
            'access': str(token.access_token)
        }

    @staticmethod
    def authenticate_user(request, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return user

        raise serializers.ValidationError("Invalid Email or Password")
