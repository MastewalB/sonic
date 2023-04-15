from django.urls import path
from studio.views import GetStudioEpisodeView, GetStudioPodcastView, StudioEpisodeListView, StudioPodcastListView, StudioPodcastView, StudioEpisodeView, GenreView

urlpatterns = [
    path("podcasts/", StudioPodcastView.as_view()),
    path("podcasts/view/<str:podcast_id>", GetStudioPodcastView.as_view()),
    path("podcasts/list/<str:user_id>", StudioPodcastListView.as_view()),
    path("episodes/", StudioEpisodeView.as_view()),
    path("episodes/view/<str:episode_id>", GetStudioEpisodeView.as_view()),
    path("episdodes/list/<str:user_id>", StudioEpisodeListView.as_view()),

    path("genres/all", GenreView.as_view())
]
