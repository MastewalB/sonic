from django.contrib import admin
from favorites.models import LikedAlbums, LikedSongsPlaylist
# Register your models here.

admin.site.register(LikedSongsPlaylist)
admin.site.register(LikedAlbums)
