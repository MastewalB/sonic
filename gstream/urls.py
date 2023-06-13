from django.urls import path, include
from gstream.views import StreamingFriendsView, StreamView

urlpatterns = [
    path('', StreamView.as_view()),
    path('list/', StreamingFriendsView.as_view())
]
