from django.core.management.base import BaseCommand, CommandError
from apps.event.models import EventParticipant, TShirt
from django.contrib.auth.models import User, Group
import random


class Command(BaseCommand):
    help = 'Loads users into db'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(options["file"][0], "r", encoding="utf8") as user_file:
            lines = user_file.readlines()
            count_participants = 0
            count_tshirts = 0
            updated_participants = 0
            for line in lines:
                tmp = line.split(",")
                prt_obj, created = EventParticipant.objects.get_or_create(name=tmp[0], surname=tmp[1], nick=tmp[2])
                prt_obj.phone = tmp[3]
                prt_obj.ice_phone = tmp[4]
                prt_obj.ice_name = tmp[5]
                prt_obj.ice_extra = tmp[6]

                if tmp[7] == '1':
                    user = User.objects.create_user(username=tmp[2]) #nickname
                    db_group = Group.objects.filter(id__in=tmp[8].split(';')) #groups
                    user.groups.add(*db_group)
                    pin = random.randint(1002, 9999)
                    while EventParticipant.objects.filter(pin=pin).first():
                        pin = random.randint(1002, 9999)
                    prt_obj.pin = pin
                    prt_obj.user = user

                    if tmp[9] == "1": #is_staff
                        prt_obj.is_staff = 1
                if tmp[10] and created:
                    tshirts = tmp[10].split(';')
                    extra = tmp[11].strip()
                    for tshirt in tshirts:
                        TShirt.objects.create(event_participant=prt_obj, size=tshirt, extra=extra)
                        count_tshirts += 1
                prt_obj.save()
                if created:
                    count_participants += 1
                else:
                    updated_participants += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported users {count_participants} tshirts {count_tshirts}, participants updated {updated_participants}'))