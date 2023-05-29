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
from django.shortcuts import render, redirect
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


class MyAuth(ObtainAuthToken):
    authentication_classes = []


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


#####

@require_http_methods(["GET",])
@csrf_exempt
def login_page(request):
    return render(request, "index.html")


@require_http_methods(["POST",])
def login_basic_pin(request):
    pin = request.POST.get("pin")
    if not pin:
        return JsonResponse({"login": "missing_pin"}, status=401, safe=False)
    try:
        participant = EventParticipant.objects.get(pin=str(pin), user__isnull=False)
    except EventParticipant.DoesNotExist as e:
        return JsonResponse({"login": "unauthorized"}, status=401, safe=False)
    if not participant.user.has_perms(["event.change_eventparticipant"]):
        return JsonResponse({"login": "missing permissions"}, status=401, safe=False)
    login(request, participant.user)
    return redirect("/basic/dashboard/")


@require_http_methods(["GET",])
@login_required
def get_dashboard(request):
    return render(request, "dashboard.html")


@require_http_methods(["GET",])
@login_required
def get_info_point_view(request):
    data = EventParticipant.objects.all().values("id", "name", "surname", "nick")
    return JsonResponse({"view": render(request, "infopoint.html", {"participants": data}).content.decode(), "data": {}}, safe=False)


def set_user_by_token(request):
    #this is a lazy hack, there is a similar thing but i cant remember where, ill rewrite this to middleware
    token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[-1]
    if not token:
        return JsonResponse({"error": "unauthorized user"}, status=401)
    try:
        token = Token.objects.get(key=token)
    except Token.DoesNotExist:
        return JsonResponse({"error": "unauthorized user"}, status=401)
    request.user = token.user