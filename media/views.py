import mimetypes
import os
from urllib.parse import unquote

from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class MediaView(APIView):

    def get(self, request, path):

        if not os.path.exists(f"{settings.MEDIA_ROOT}/{path}"):
            return Response("No such file", status=404)

        mimetype, encoding = mimetypes.guess_type(path, strict=True)
        if not mimetype:
            mimetype = "text/html"
        file_path = unquote(os.path.join(
            settings.MEDIA_ROOT, path)).encode("utf-8")
        if os.path.isdir(file_path):
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )
        return FileResponse(open(file_path, "rb"), content_type=mimetype)
