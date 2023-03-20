from django.urls import path
from .views import PlaylistItemsView, PlaylistView

urlpatterns = [
    path('playlist/', PlaylistView.as_view()),
    path('playlist-item/', PlaylistItemsView.as_view()),
]