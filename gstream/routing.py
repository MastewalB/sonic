from django.urls import re_path
from gstream.consumers import StreamConsumer

websocket_urlpatterns = [
    re_path(r'ws/stream/<str:user_id>', StreamConsumer.as_asgi())
]
