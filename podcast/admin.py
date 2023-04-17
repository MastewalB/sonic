from django.contrib import admin
from podcast.models import Podcast, PodcastProvider, PodcastSubscription

# Register your models here.

admin.site.register(Podcast)
admin.site.register(PodcastSubscription)
admin.site.register(PodcastProvider)
