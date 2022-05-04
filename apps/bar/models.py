from django.db import models
from apps.event.models import EventParticipant
from apps.magazine.models import Item


class ItemSell(models.Model):
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    barnote = models.ForeignKey("BarNote", on_delete=models.DO_NOTHING)
    seller = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()


class BarNote(models.Model):
    participant = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING)
    items = models.ManyToManyField(Item, through=ItemSell)


class BarAccount(models.Model):
    participant = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING)
    credits = models.DecimalField(max_digits=6, decimal_places=2)
