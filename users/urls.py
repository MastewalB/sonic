from django.urls import path
from users.views import SignupView, LoginView, UpdateProfileView, activate


urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('update/<str:id>', UpdateProfileView.as_view(), name='update')
]
