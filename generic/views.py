from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from django.contrib.auth.models import User
from generic.serializers import UserSerializer
from rest_framework.decorators import action


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

