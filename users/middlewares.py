import datetime
from django.core.cache import cache
from django.conf import settings


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):

        current_user = request.user
        if request.user.is_authenticated():
            now = datetime.datetime.now()
            cache.set('' % (current_user.id), now,
                      settings.USER_LASTSEEN_TIMEOUT)
