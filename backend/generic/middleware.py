from django.http import JsonResponse
from django.conf import settings
import logging

log = logging.getLogger(__name__)


class GameErrorMiddleware:
    def __init__(self, get_response):
        self.response = get_response

    def __call__(self, request):
        return self.response(request)

    def process_exception(self, request, exception):
        if settings.DEBUG:
            log.error(exception, exc_info=True)
        return JsonResponse({"error": exception.args[0]}, status=400, safe=False)