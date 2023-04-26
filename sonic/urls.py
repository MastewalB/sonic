"""sonic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
import users.views
from django.urls import path, include
from users.forms import AdminLoginForm
from users.views import login

admin.autodiscover()
admin.site.login_form = AdminLoginForm
admin.site.login_template = 'login.html'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('storage/', include('media.urls')),
    path('api/v1/accounts/', include('users.urls')),

    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/follow/', include('follow.urls')),
    path('api/v1/music/', include('music.urls')),
    path('api/v1/search/', include('search.urls')),
    path('api/v1/playlist/', include('playlists.urls')),
    path('api/v1/studio/', include('studio.urls')),
    path('api/v1/podcasts/', include('podcast.urls'))
]
