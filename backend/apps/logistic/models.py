from django.db import models
from apps.bar.models import BarItem
from apps.event.models import EventParticipant


class MagazineItem(models.Model):
    baritem = models.ForeignKey(BarItem, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0)
    creation_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    adding_user = models.ForeignKey(EventParticipant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.baritem.name
