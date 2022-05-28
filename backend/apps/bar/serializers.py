from generic.serializers import create_generic_serializer
from apps.bar.models import BarAccount, BarReceipt, BarItem, BarReceiptItem, BarItemCategory
from rest_framework import serializers
from django.db import transaction


BarItemCategorySerializer = create_generic_serializer(BarItemCategory)
BarItemSerializer = create_generic_serializer(BarItem)


class BarReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarReceiptItem
        fields = ("id", "item_name", "quantity", "price", "item")


class BarReceiptsSerializer(serializers.ModelSerializer):
    bar_items = BarReceiptItemSerializer(many=True, read_only=True)

    class Meta:
        model = BarReceipt
        fields = ("id", "seller", "account", "bar_items", "created_at", "modify_at", "modify_by", "sum")

    def is_valid(self, raise_exception=False):
        self.items = self.initial_data.pop("items")
        if not self.items:
            raise Exception("Missing item list")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        with transaction.atomic():
            receipt_items = self.items
            items_to_create = []
            items = [x['item_id'] for x in receipt_items]
            items = BarItem.objects.filter(id__in=items)
            items = {x.id: x for x in items}
            sum = 0 # this will require recalc on each change
            bar_receipt = BarReceipt.objects.create(**validated_data)
            for receipt_item in receipt_items:
                item = items[receipt_item['item_id']]
                filled_receipt_item = { # catch exception
                    **receipt_item,
                    "item_name": item.name,
                    "price": item.price
                }
                sum += item.price * receipt_item["quantity"]
                items_to_create.append(BarReceiptItem(**filled_receipt_item, bar_receipt=bar_receipt))
            BarReceiptItem.objects.bulk_create(items_to_create)
            #to rewrite this
            bar_receipt.sum = sum
            bar_receipt.save()
            return bar_receipt


class BarAccountSerializer(serializers.ModelSerializer):
    nick = serializers.CharField(source="participant.nick", read_only=True)
    receipts = BarReceiptsSerializer(many=True, read_only=True)
    current_credits = serializers.SerializerMethodField()

    class Meta:
        model = BarAccount
        fields = "__all__"

    def get_current_credits(self, obj):
        current_credits = sum(obj.receipts.all().values_list("sum", flat=True))
        return obj.credits - current_credits