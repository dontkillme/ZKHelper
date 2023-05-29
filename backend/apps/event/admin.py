from django.contrib import admin
from apps.event.models import EventParticipant, ParticipantQuests, TShirt, Quest, Attraction


class AdminView(admin.ModelAdmin):
    pass


admin.site.register(EventParticipant, AdminView)
admin.site.register(ParticipantQuests, AdminView)
admin.site.register(TShirt, AdminView)
admin.site.register(Quest, AdminView)
admin.site.register(Attraction, AdminView)