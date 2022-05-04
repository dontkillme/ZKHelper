from generic.serializers import create_generic_serializer
from apps.magazine.models import Item, ItemType, Reagent, ReagentLog, ItemReagentThrough
from rest_framework import serializers

ItemTypeSerializer = create_generic_serializer(ItemType)
ReagentSerializer = create_generic_serializer(Reagent)
ReagentLogSerializer = create_generic_serializer(ReagentLog)


class ItemReagentThroughSerializer(serializers.ModelSerializer):
    reagent = ReagentSerializer(Many=False)

    class Meta:
        model = ItemReagentThrough
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    reagents = ItemReagentThroughSerializer(many=True)

    class Meta:
        model = Item
        fields = "__all__"
