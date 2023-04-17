from django.urls import path
from studio.views import GetStudioEpisodeView, GetStudioPodcastView, StudioEpisodeListView, StudioPodcastListView, StudioPodcastView, StudioEpisodeView, GenreView
from studio.feeds import PodcastFeed, PodcastAtomFeed

urlpatterns = [
    path("podcasts/", StudioPodcastView.as_view()),
    path("podcasts/view/<str:podcast_id>", GetStudioPodcastView.as_view()),
    path("podcasts/list/<str:user_id>", StudioPodcastListView.as_view()),
    path("podcasts/feed/rss/<str:slug>", PodcastFeed()),
    path("podcasts/feed/atom/<str:slug>", PodcastAtomFeed()),
    path("episodes/", StudioEpisodeView.as_view()),
    path("episodes/view/<str:episode_id>", GetStudioEpisodeView.as_view()),
    path("episodes/list/<str:podcast_id>", StudioEpisodeListView.as_view()),

    path("genres/all", GenreView.as_view())
]
