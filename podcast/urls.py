from django.urls import path, include
from podcast.views import SubscriptionView, SubscriptionListView, CreateSubscriptionView

urlpatterns = [
    path('subscriptions/', SubscriptionView.as_view()),
    path('subscriptions/all/', SubscriptionListView.as_view()),
    path('subscriptions/create/', CreateSubscriptionView.as_view())
]
