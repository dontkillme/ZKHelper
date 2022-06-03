from rest_framework import serializers
from generic.serializers import create_generic_serializer
from apps.event.models import EventParticipant, Quest, Attraction, TShirt
from django.contrib.auth.models import User, Group

TShirtSerializer = create_generic_serializer(TShirt)
QuestSerializer = create_generic_serializer(Quest)
AttractionSerializer = create_generic_serializer(Attraction)
EventParticipantSerializer = create_generic_serializer(EventParticipant)


class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = "__all__"
        extra_kwargs = {
            "pin": {"write_only": True, "required": False, "allow_null": True}
        }

    def is_valid(self, raise_exception=False):
        self.new_user = None
        if "user" in self.initial_data and self.initial_data["user"] == -1:
            self.new_user = self.initial_data.pop("user")
        if "groups" in self.initial_data:
            self.user_groups = self.initial_data.pop("groups")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        if self.new_user:
            user = User.objects.create_user(username=validated_data["nick"], first_name=validated_data["name"],
                                            last_name=validated_data["surname"])
            validated_data["user"] = user
            validated_data["is_staff"] = True
            if self.user_groups:
                db_group = Group.objects.filter(id__in=self.user_groups)
                user.groups.add(*db_group)
        return super().create(validated_data)


class FullEventParticipantSerializer(serializers.ModelSerializer):
    tshirt = TShirtSerializer(many=True, read_only=True)

    class Meta:
        model = EventParticipant
        fields = [field.name for field in EventParticipant._meta.fields if field.name != "pin"] + ["tshirt",]