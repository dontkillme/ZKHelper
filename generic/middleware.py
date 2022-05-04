from generic.exceptions import GameLendException
from django.http import JsonResponse


class GameErrorMiddleware:
    def __init__(self, get_response):
        self.response = get_response

    def __call__(self, request):
        return self.response(request)

    def process_exception(self, request, exception):
        return JsonResponse({"error": exception.args[0]}, status=400, safe=False)