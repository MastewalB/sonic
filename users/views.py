from threading import Thread
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.core.mail import send_mail, EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from rest_framework import serializers, status
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
        # TODO Successfully activated please login on the app
    else:
        # TODO - handle invalid activation token
        return


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
    def put(self, request, id):
        user = User.objects.get(id=id)
        data = request.data.dict()
        serializer = UserSerializer(user, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# class ResetPasswordView(APIView)
# class ForgotPasswordView(APIView)
