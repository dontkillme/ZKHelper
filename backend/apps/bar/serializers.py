from generic.serializers import create_generic_serializer
from apps.bar.models import BarAccount, BarReceipt, BarItem, BarReceiptItem, BarItemCategory
from rest_framework import serializers
from django.db import transaction


# informacja o braku krechy - 460 nie ma krechy, 404 jak nie ma w ogole uczestnika
# Dodac flage "staff_price" do rachunku (info)
# dodatkowo crud dla wszystkich modeli barowych w admin panelu, krechy itd
# potykacz jesli jest ponizej -10


BarItemCategorySerializer = create_generic_serializer(BarItemCategory)


class BarItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        model = BarItem
        fields = ("id", "name", "price", "staff_price", "category_id", "modify_date", "available")


class BarReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarReceiptItem
        fields = ("id", "item_name", "quantity", "price", "item_id")


class BarReceiptsSerializer(serializers.ModelSerializer):
    bar_items = BarReceiptItemSerializer(many=True, read_only=True)

    class Meta:
        model = BarReceipt
        fields = ("id", "seller", "account", "bar_items", "created_at", "modify_at", "modify_by", "sum")

    def is_valid(self, raise_exception=False):
        self.items = self.initial_data.pop("items")
        self.staff_price = int(self.initial_data.pop("staff_price", "0"))
        if not self.items:
            raise Exception("Missing item list")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        with transaction.atomic():
            receipt_items = self.items
            items_to_create = []
            items = self._get_items_instances()
            receipt_sum = self._calc_receipt_sum(items, receipt_items, self.staff_price)
            bar_receipt = BarReceipt.objects.create(**validated_data)
            for receipt_item in receipt_items:
                item = items[receipt_item["item_id"]]
                price = item.staff_price if self.staff_price else item.price
                filled_receipt_item = {
                    **receipt_item,
                    "item_name": item.name,
                    "price": price
                }
                items_to_create.append(BarReceiptItem(**filled_receipt_item, bar_receipt=bar_receipt))
            BarReceiptItem.objects.bulk_create(items_to_create)
            #to rewrite this
            bar_receipt.price_mode = self.staff_price
            bar_receipt.sum = receipt_sum
            bar_receipt.save()
            return bar_receipt

    def _get_items_instances(self):
        if not self.items:
            return
        items = [x['item_id'] for x in self.items]
        items = BarItem.objects.filter(id__in=items)
        items = {x.id: x for x in items}
        return items

    @staticmethod
    def _calc_receipt_sum(items, receipt_items, staff_price):
        sum = 0
        for receipt_item in receipt_items:
            price = items[receipt_item["item_id"]].staff_price if staff_price else items[receipt_item["item_id"]].price
            sum += price * receipt_item["quantity"]
        return sum


class BarAccountBaseSerializer(serializers.ModelSerializer):

    def get_balance(self, obj):
        current_credits = sum(obj.receipts.all().values_list("sum", flat=True))
        return format(obj.credits - current_credits, ".2f")


class BarAccountSerializer(BarAccountBaseSerializer):
    nick = serializers.CharField(source="participant.nick", read_only=True)
    receipts = BarReceiptsSerializer(many=True, read_only=True)
    balance = serializers.SerializerMethodField()
    participant_id = serializers.IntegerField()

    class Meta:
        model = BarAccount
        fields = ("participant_id", "nick", "receipts", "balance", "credits", "created_at")


class BarAccountBasicInfoSerializer(BarAccountBaseSerializer):
    nick = serializers.CharField(source="participant.nick", read_only=True)
    is_staff = serializers.BooleanField(source="participant.is_staff")
    balance = serializers.SerializerMethodField()
    participant_id = serializers.IntegerField()

    class Meta:
        model = BarAccount
        fields = ("balance", "is_staff", "participant_id", "credits", "nick")


class BarAccountStackSerializer(BarAccountBaseSerializer):
    nick = serializers.CharField(source="participant.nick", read_only=True)
    balance = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    participant_id = serializers.IntegerField()

    class Meta:
        model = BarAccount
        fields = ("participant_id", "nick", "balance", "credits", "created_at", "products")

    def get_products(self, obj):
        items = obj.receipts.all().values_list("bar_items__item_id", "bar_items__price", "bar_items__quantity")
        output = {}
        for item, price, quantity in items:
            if not item: #rewrite this
                continue
            key = (item, price)
            if key not in output:
                output[key] = {
                    "item_id": item,
                    "price": price,
                    "quantity": 0
                }
            output[key]["quantity"] += quantity

        return output.values()