from django.urls import path
from .views import PlaylistItemsView, PlaylistView

urlpatterns = [
    path('<id>/', PlaylistView.as_view()),
    path('<id>/item/', PlaylistItemsView.as_view()),
]