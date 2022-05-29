from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from generic.helpers import PermissionForMethod


def register_endpoints(model, serializer, auth_cls=(TokenAuthentication,), view_cls=viewsets.ModelViewSet,
                       mth_perms={}):
    class MainHandler(view_cls):
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = [IsAuthenticated, PermissionForMethod]
        method_permissions = mth_perms
        authentication_classes = auth_cls
        filterset_fields = [f.name for f in model._meta.get_fields()]

    return MainHandler
