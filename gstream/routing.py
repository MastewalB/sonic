# from django.conf.urls import url
from django.urls import re_path, path
from gstream.consumers import StreamConsumer

websocket_urlpatterns = [
    path('ws/stream/<str:user_id>/', StreamConsumer.as_asgi())
]
