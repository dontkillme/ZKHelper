from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from django.contrib.auth.models import User
from generic.serializers import UserSerializer
from rest_framework.decorators import action
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from apps.event.models import EventParticipant
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
import json


class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['get'])
    def current(self, request):
        return JsonResponse(UserSerializer(request.user).data, safe=False)


class Logout(ObtainAuthToken):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return JsonResponse({"logout": True}, safe=False)


class PingView(ObtainAuthToken):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get(self, request):
        return JsonResponse({"success": True}, safe=False)


@require_http_methods(["POST",])
@csrf_exempt
def pin_login(request):
    pin = request.POST.get("pin", json.loads(request.body).get("pin"))
    if not pin: #rewrite
        return JsonResponse({"login": "missing_pin"}, status=401, safe=False)

    try:
        participant = EventParticipant.objects.get(pin=str(pin), user__isnull=False)
    except EventParticipant.DoesNotExist as e:
        return JsonResponse({"login": "unauthorized"}, status=401, safe=False)

    login(request, participant.user)
    token, created = Token.objects.get_or_create(user=request.user)
    return JsonResponse(
        {
            "participant_id": participant.id,
            "participant_nick": participant.nick,
            "token": token.key,
            "login": "success",
            "permissions": list(request.user.get_all_permissions()),
            "groups": list(request.user.groups.all().values_list("name", flat=True))
        },
        status=200,
        safe=False
    )
