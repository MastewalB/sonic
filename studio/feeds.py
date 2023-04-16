from django.contrib.syndication.views import Feed
from django.urls import reverse
from studio.models import StudioPodcast, StudioEpisode


class PodcastFeed(Feed):

    def get_object(self, request, slug):
        return StudioPodcast.objects.get(slug=slug)

    def items(self, podcast):
        items = StudioEpisode.objects.filter(
            podcast=podcast).order_by("-upload_date")
        return items

    def link(self, podcast):
        return "/studio/pocasts/{0}".format(podcast.id)

    def description(self, podcast):
        return podcast.description

    def item_link(self, item):
        return "{0}".format(item.file.url)
