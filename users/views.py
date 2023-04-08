from django.contrib.auth.forms import AuthenticationForm
from threading import Thread
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.core.mail import send_mail, EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer, LoginSerializer
from users.utils import Utils
from users.models import User
from django.http import HttpResponse
from django.template import loader
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from users.forms import AdminLoginForm

# Create your views here.


class SignupView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        data = request.data
        email = data['email']

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            
            serializer.save()
            user = User.objects.get(email=email)
            token = Utils.encode_token(user)
            if activateEmail(request, user, user.email):
                return Response(
                    {
                        'data': serializer.data,
                        'token': token
                    }
                )

                # t = Thread(target=send_mail, args=(
                #     mail_subject, message, settings.EMAIL_HOST_USER, to_email
                # ))
                # t.start()

        # user = User.objects.get(email=email)

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'message': "Invalid Registration Credential"
            }
        )


def activateEmail(request, user, to_email):
    mail_subject = "Email Confirmation"
    message = render_to_string('template_account_activate.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_b64encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    if email.send():
        print("dfjhskjfhdljfhweiufhieusjhfieu")
        return True
    return False


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_b64decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        context = {
            'title': 'Welcome to Sonic',
            'body': ''
        }
        return render(request, 'activation_template.html', context)
    else:
        return render(request, 'template_activation_error.html')


class LoginView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            user = Utils.authenticate_user(serializer.validated_data)
            serialized_user = UserSerializer(user)
            token = Utils.enconde_token(user)

            return Response(
                {
                    "data": serialized_user.data,
                    "token": token
                }
            )
        except serializers.ValidationError:
            return Response(
                {
                    "message": "Invalid Email or Password"
                }
            )


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = None
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )
        data = request.data
        serializer = UserSerializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

from django.shortcuts import render

def my_template_view(request):
    context = {
        'title': 'My Page Title',
        'body': 'Hello World'
    }
    return render(request, 'activation_template.html', context)

def forgot_password_view(request):
    
    return render(request, 'password_template.html')

# class ResetPasswordView(APIView)
# class ForgotPasswordView(APIView)
