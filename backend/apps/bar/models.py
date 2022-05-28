from django.db import models
from apps.event.models import EventParticipant
from simple_history.models import HistoricalRecords


class BarItemCategory(models.Model):
    name = models.CharField(max_length=128)


class BarItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    staff_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    category = models.ForeignKey(BarItemCategory, on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)


class BarReceiptItem(models.Model):
    bar_receipt = models.ForeignKey("BarReceipt", on_delete=models.DO_NOTHING, related_name="bar_items")
    item = models.ForeignKey(BarItem, on_delete=models.DO_NOTHING, related_name="bar_item", to_field="id")
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class BarAccount(models.Model):
    participant = models.OneToOneField(EventParticipant, on_delete=models.DO_NOTHING, primary_key=True)
    credits = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()


class BarReceipt(models.Model):
    account = models.ForeignKey(BarAccount, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="receipts")
    seller = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    modify_by = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING, null=True, blank=True,
                                  related_name="receipt_modify_by")
    items = models.ManyToManyField(BarItem, through=BarReceiptItem, related_name="bar_items")
    sum = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)


