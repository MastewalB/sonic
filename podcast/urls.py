from django.urls import path, include
from podcast.views import SubscriptionView, SubscriptionListView

urlpatterns = [
    path('subscriptions', SubscriptionView.as_view()),
    path('subscriptions/all', SubscriptionListView.as_view())
]
