from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.urls import reverse
from studio.models import StudioPodcast, StudioEpisode


class PodcastFeed(Feed):

    def get_object(self, request, slug):
        return StudioPodcast.objects.get(slug=slug)

    def title(self, podcast):
        return podcast.title

    def author_name(self, podcast):
        return podcast.author.get_full_name()

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

    def item_author_name(self, item):
        return item.podcast.author.get_full_name()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.upload_date

    def item_updateddate(self, item):
        return item.last_modified


class PodcastAtomFeed(PodcastFeed):
    feed_type = Atom1Feed
    subtitle = PodcastFeed.description
