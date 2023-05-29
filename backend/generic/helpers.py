import pytz
import datetime
from rest_framework import serializers, permissions


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return int(value.timestamp())

    def to_internal_value(self, data):
        return datetime.datetime.utcfromtimestamp(data).replace(tzinfo=pytz.utc)


class PermissionForMethod(permissions.BasePermission):
    def has_permission(self, request, view):
        perms_mapping = getattr(view, "method_permissions", {})

        if not perms_mapping:
            return True

        required_perms = perms_mapping.get(request.method, [])
        return request.user.has_perms(required_perms)
