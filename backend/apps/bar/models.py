from django.db import models
from apps.event.models import EventParticipant
from simple_history.models import HistoricalRecords


class BarItemCategory(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class BarItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    staff_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    category = models.ForeignKey(BarItemCategory, on_delete=models.PROTECT)
    modify_date = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    position = models.IntegerField(default=0)

    def __str__(self):
        return "[{}] {}".format(self.id, self.name)


class BarReceiptItem(models.Model):
    bar_receipt = models.ForeignKey("BarReceipt", on_delete=models.DO_NOTHING, related_name="bar_items")
    item = models.ForeignKey(BarItem, on_delete=models.DO_NOTHING, related_name="bar_item", to_field="id")
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.item_name


class BarAccount(models.Model):

    STATE_NOT_CREATED = 0
    STATE_ACTIVE = 1
    STATE_CLOSED = 2

    participant = models.OneToOneField(EventParticipant, on_delete=models.DO_NOTHING, primary_key=True)
    credits = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(default=STATE_NOT_CREATED)
    history = HistoricalRecords()

    def __str__(self):
        return "[{}] {} {} {}".format(self.participant.id, self.participant.name, self.participant.surname, self.participant.nick)


class BarAccountLog(models.Model):
    bar_account = models.ForeignKey(BarAccount, on_delete=models.DO_NOTHING)
    change_by = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING)
    value = models.TextField()
    action = models.TextField()
    change_date = models.DateTimeField(auto_now_add=True)


class BarReceipt(models.Model):
    account = models.ForeignKey(BarAccount, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="receipts")
    seller = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)
    modify_by = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING, null=True, blank=True,
                                  related_name="receipt_modify_by")
    items = models.ManyToManyField(BarItem, through=BarReceiptItem, related_name="bar_items")
    sum = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    price_mode = models.IntegerField(default=0)
    history = HistoricalRecords()

    def __str__(self):
        return "[{}] {} {} {}".format(self.account_id, self.id, self.created_at, self.sum)


