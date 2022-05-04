from django.db import models
from apps.event.models import EventParticipant


class ReagentLog(models.Model):
    models.ForeignKey("Reagent", on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    delivered_by = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING)
    private_funds = models.BooleanField(default=False)


class Reagent(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=64)


class ItemReagentThrough(models.Model):
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey("Item", on_delete=models.SET_NULL, blank=True, null=True)
    reagent = models.ForeignKey("Reagent", on_delete=models.SET_NULL, blank=True, null=True)


class ItemType(models.Model):
    name = models.CharField(max_length=128)


class Item(models.Model):
    name = models.CharField(max_length=255)
    reagents = models.ManyToManyField(to=Reagent, through=ItemReagentThrough)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.ForeignKey(ItemType, on_delete=models.SET_NULL, blank=True, null=True)
    