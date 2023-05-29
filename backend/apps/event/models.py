from django.db import models
from django.contrib.auth.models import User


# system questow taki ze wpisujemy user i quest oraz czy wypelniony.


class EventParticipant(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    nick = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)
    ice_phone = models.CharField(max_length=128, blank=True, null=True)
    ice_name = models.CharField(max_length=256, blank=True, null=True)
    ice_extra = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    accredited = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    pin = models.CharField(max_length=255, blank=True, null=True, unique=True) ## think to make hash from it

    def __str__(self):
        return "[{}] {} {} {}".format(self.id, self.name, self.surname, self.nick)


class Quest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    reward = models.IntegerField(default=10)

    def __str__(self):
        return self.id + " " + self.name + " " + self.reward


class ParticipantQuests(models.Model):
    quest_id = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name="quest_participant_id")
    participant_id = models.ForeignKey(EventParticipant, on_delete=models.CASCADE, related_name="participant_quest_id")
    done = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "[{}] {}".format(self.participant_id, self.quest_id)


class Attraction(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    reward = models.IntegerField(default=10)
    start_time = models.DateTimeField()
    game_master = models.ForeignKey("EventParticipant", on_delete=models.SET_NULL, blank=True, null=True)
    duration_time = models.IntegerField(default=60)

    def __str__(self):
        return self.name


class TShirt(models.Model):
    event_participant = models.ForeignKey(EventParticipant, on_delete=models.DO_NOTHING, related_name="tshirt")
    size = models.CharField(max_length=16)
    given_out = models.BooleanField(default=False)
    extra = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.event_participant.name