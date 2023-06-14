# endpoint for the recommend view
from django.urls import path
from .views import SongRecommender

urlpatterns = [
    path('recommend/<str:song_id>/', SongRecommender.as_view(), name='recommend'),
]
