from django.contrib import admin
from studio.models import StudioEpisode, StudioPodcast, Genre
# Register your models here.

admin.site.register(StudioEpisode)
admin.site.register(StudioPodcast)
admin.site.register(Genre)
