from generic.serializers import create_generic_serializer
from apps.bar.models import BarAccount, BarReceipt, BarItem, BarReceiptItem, BarItemCategory, BarAccountLog
from rest_framework import serializers
from django.db import transaction
from apps.bar.utils import add_account_change_log

# dodatkowo crud dla wszystkich modeli barowych w admin panelu, krechy itd


BarItemCategorySerializer = create_generic_serializer(BarItemCategory)


class BarItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()

    class Meta:
        ordering = ["-position",]
        model = BarItem
        fields = ("id", "name", "price", "staff_price", "category_id", "modify_date", "available", "position")


class BarReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarReceiptItem
        fields = ("id", "item_name", "quantity", "price", "item_id")


class BarReceiptsSerializer(serializers.ModelSerializer):
    bar_items = BarReceiptItemSerializer(many=True, read_only=True)

    class Meta:
        model = BarReceipt
        fields = ("id", "seller", "account", "bar_items", "created_at", "modify_at", "modify_by", "sum",
                  "price_mode")

    def is_valid(self, raise_exception=False):
        self.items = self.initial_data.pop("items")
        self.staff_price = int(self.initial_data.pop("price_mode", "0"))
        if not self.items:
            raise Exception("Missing item list")
        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.bar_items.all().delete()
            output = self._create_or_update_receipt(validated_data, instance)
            return output 

    def create(self, validated_data):
        with transaction.atomic():
            return self._create_or_update_receipt(validated_data)

    def _create_or_update_receipt(self, validated_data, bar_receipt=None):
        receipt_items = self.items
        items_to_create = []
        items = self._get_items_instances()
        receipt_sum = self._calc_receipt_sum(items, receipt_items, self.staff_price)
        if bar_receipt and bar_receipt.account_id and 'account' not in validated_data:
            bar_receipt.account = None
        elif bar_receipt and 'account' in validated_data and bar_receipt.account_id != validated_data.get('account', -1):
            bar_receipt.account = validated_data['account']
        if not bar_receipt:
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
        # to rewrite this
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
    inferring = serializers.IntegerField(write_only=True)
    state = serializers.IntegerField(read_only=True)

    class Meta:
        model = BarAccount
        fields = ("participant_id", "nick", "receipts", "balance", "credits", "created_at", "inferring", "state")

    def create(self, validated_data):
        try:
            bar_account = BarAccount.objects.get(participant_id=validated_data["participant_id"])
            bar_account.credits += validated_data['credits']
            add_account_change_log("balance change", validated_data['credits'], bar_account, validated_data['inferring'])
            if bar_account.state != BarAccount.STATE_ACTIVE:
                bar_account.state = BarAccount.STATE_ACTIVE
                add_account_change_log("opening account during insert", validated_data['credits'], bar_account,
                                       validated_data['inferring'])
            bar_account.save()
        except BarAccount.DoesNotExist:
            inferring = validated_data.pop("inferring")
            bar_account = BarAccount.objects.create(state=BarAccount.STATE_ACTIVE, **validated_data)
            add_account_change_log("opening with input", validated_data['credits'], bar_account, inferring)
        bar_account.save()
        return bar_account

    def update(self, instance, validated_data):
        instance.credits += validated_data['credits']
        add_account_change_log("balance change", validated_data['credits'], instance, validated_data['inferring'])
        instance.save()
        return instance


class BarAccountBasicInfoSerializer(BarAccountBaseSerializer):
    nick = serializers.CharField(source="participant.nick", read_only=True)
    is_staff = serializers.BooleanField(source="participant.is_staff")
    balance = serializers.SerializerMethodField()
    participant_id = serializers.IntegerField()
    state = serializers.IntegerField()

    class Meta:
        model = BarAccount
        fields = ("balance", "is_staff", "participant_id", "credits", "nick", "state")


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

