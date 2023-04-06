from django.urls import path
from users.views import SignupView, LoginView, UpdateProfileView, activate,my_template_view,forgot_password_view


urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('my-template/', my_template_view, name='my_template_view'),
    path('forgot-password/', forgot_password_view, name='forgot_password_view'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('update/<str:id>', UpdateProfileView.as_view(), name='update')
]
