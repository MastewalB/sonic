from django.urls import path, include
from follow.views import FollowView, FollowDetailView, FollowDetailListView

urlpatterns = [
    path('', FollowView.as_view()),
    path('list/<str:userId>/', FollowDetailListView.as_view()),
    path('<str:followee_id>', FollowDetailView.as_view()),
]
