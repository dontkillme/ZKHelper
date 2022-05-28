from rest_framework import serializers
from generic.serializers import create_generic_serializer
from apps.event.models import EventParticipant, Quest, Attraction, TShirt

TShirtSerializer = create_generic_serializer(TShirt)
QuestSerializer = create_generic_serializer(Quest)
AttractionSerializer = create_generic_serializer(Attraction)
EventParticipantSerializer = create_generic_serializer(EventParticipant)


class FullEventParticipantSerializer(serializers.ModelSerializer):
    tshirt = TShirtSerializer(many=True, read_only=True)

    class Meta:
        model = EventParticipant
        fields = [field.name for field in EventParticipant._meta.fields] + ["tshirt",]
