from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication


def register_endpoints(model, serializer, auth_cls=(TokenAuthentication,), view_cls=viewsets.ModelViewSet):
    class MainHandler(view_cls):
        queryset = model.objects.all()
        serializer_class = serializer
        authentication_classes = auth_cls
        filterset_fields = [f.name for f in model._meta.get_fields()]

    return MainHandler
