from django.urls import path, re_path
from media.views import MediaView


urlpatterns = [
    re_path(r"(?P<path>.*)", MediaView.as_view())
]
