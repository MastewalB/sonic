from django.contrib import admin
from playlists.models import Playlist, PlaylistItems
# Register your models here.

admin.site.register(Playlist)
admin.site.register(PlaylistItems)
