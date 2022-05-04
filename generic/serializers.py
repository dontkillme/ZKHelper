from rest_framework import serializers
from django.contrib.auth.models import User


def create_generic_serializer(model_cls):
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_cls
            fields = "__all__"
    return GenericSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]
