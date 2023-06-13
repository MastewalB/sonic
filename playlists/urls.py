from django.urls import path
from .views import PlaylistItemsView, PlaylistView, CreatePlaylistView, UserPlaylistView

urlpatterns = [
    path('create/', CreatePlaylistView.as_view()),
    path('add/', PlaylistItemsView.as_view()),
    path('remove/', PlaylistItemsView.as_view()),
    path('delete/<str:playlist_id>/', PlaylistView.as_view()),
    path('<str:playlist_id>/', PlaylistView.as_view()),
    path('user_playlist/<str:user_id>/', UserPlaylistView.as_view()),
]
