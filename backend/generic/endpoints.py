from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from generic.helpers import PermissionForMethod
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

def register_endpoints(model, serializer, auth_cls=(TokenAuthentication, SessionAuthentication), view_cls=viewsets.ModelViewSet,
                       mth_perms={}, query=None, with_pagination=False):
    class MainHandler(view_cls):
        queryset = query if query else model.objects.all()
        serializer_class = serializer
        permission_classes = [IsAuthenticated, PermissionForMethod]
        method_permissions = mth_perms
        authentication_classes = auth_cls
        filterset_fields = [f.name for f in model._meta.get_fields()]
        pagination_class = StandardResultsSetPagination if with_pagination else None

    return MainHandler
