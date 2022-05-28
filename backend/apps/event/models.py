from django.db import models
from django.contrib.auth.models import User


class EventParticipant(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    nick = models.CharField(max_length=255)
    phone = models.CharField(max_length=128, blank=True, null=True)
    ice_phone = models.CharField(max_length=128, blank=True, null=True)
    ice_name = models.CharField(max_length=256, blank=True, null=True)
    ice_extra = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    accredited = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


class Quest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    reward = models.IntegerField(default=10)


class Attraction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    reward = models.IntegerField(default=10)
    start_time = models.DateTimeField()
    game_master = models.ForeignKey("EventParticipant", on_delete=models.SET_NULL, blank=True, null=True)
    duration_time = models.IntegerField(default=60)


class TShirt(models.Model):
    event_participant = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING, related_name="tshirt")
    size = models.CharField(max_length=16)
    given_out = models.BooleanField(default=False)
    extra = models.TextField(blank=True, null=True)