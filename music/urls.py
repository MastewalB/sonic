from django.urls import path, include
from rest_framework import routers
from .views import (
    AlbumViewSet,
    AlbumGetViewSet,
    ArtistViewSet,
    ArtistGetViewSet,
    SongViewSet,
    SongGetViewSet
)

router = routers.DefaultRouter()
# router.register(r'albums', AlbumViewSet, basename='albums')
# router.register(r'artists', ArtistViewSet, basename='artists')
router.register(r'songs', SongViewSet, basename='songs')
router.register(r'albums', AlbumGetViewSet, basename='albums')
router.register(r'artists', ArtistGetViewSet, basename='artists')
# router.register(r'songs', SongGetViewSet, basename='songs')

urlpatterns = [
    path('albums/<int:pk>/', AlbumGetViewSet.as_view({'get': 'retrieve'}), name='album-get'),
    path('artists/<int:pk>/', ArtistGetViewSet.as_view({'get': 'retrieve'}), name='artist-get'),
    path('songs/<int:pk>/', SongGetViewSet.as_view({'get': 'retrieve'}), name='song-get'),
    path('', include(router.urls)),
]
