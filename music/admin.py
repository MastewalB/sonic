from django.contrib import admin
from music.models import Artist, Album, Song
# Register your models here.


admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Song)
