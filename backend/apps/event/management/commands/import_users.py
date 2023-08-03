from django.core.management.base import BaseCommand, CommandError
from apps.event.models import EventParticipant, TShirt
from django.contrib.auth.models import User, Group
from django.db import transaction
import random
#0        1      2    3   4   5        6          7                  8     9
#imie,nazwisko,ksywa,tel,ice,ice name,ice extra,create_system_user,group,is_staff

class Command(BaseCommand):
    help = 'Loads users into db'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)
        parser.add_argument('tshirts', nargs='+', type=str)

    def _load_tshirts(self, filename):
        output = {}
        with open(filename, "r", encoding="utf8") as f:
            lines = f.readlines()
            for line in lines:
                tmp = line.split(",")
                if tmp[5]:
                    key = (tmp[0].strip(), tmp[1].strip(), tmp[2].strip())
                    output[key] = [tmp[5], tmp[6]]
        return output

    def handle(self, *args, **options):
        with transaction.atomic():
            tshirts_list = {}
            if "tshirts" in options:
                tshirts_list = self._load_tshirts(options["tshirts"][0])
            with open(options["file"][0], "r", encoding="utf8") as user_file:
                lines = user_file.readlines()
                count_participants = 0
                count_tshirts = 0
                updated_participants = 0
                for line in lines:
                    tmp = line.split(",")
                    prt_obj, created = EventParticipant.objects.get_or_create(name=tmp[0].strip(), surname=tmp[1].strip(), nick=tmp[2].strip())
                    prt_obj.phone = tmp[3]
                    prt_obj.ice_phone = tmp[4]
                    prt_obj.ice_name = tmp[5]
                    prt_obj.ice_extra = tmp[6]

                    if tmp[7] == '1':
                        user = User.objects.create_user(username=tmp[2]) #nickname
                        if tmp[8]:
                            db_group = Group.objects.filter(id__in=tmp[8].split(';')) #groups
                            user.groups.add(*db_group)
                        pin = random.randint(1002, 9999)
                        while EventParticipant.objects.filter(pin=pin).first():
                            pin = random.randint(1002, 9999)
                        prt_obj.pin = pin
                        prt_obj.user = user

                    if tmp[9] == "1": #is_staff
                        prt_obj.is_staff = 1
                    key = (tmp[0].strip(), tmp[1].strip(), tmp[2].strip())
                    if key in tshirts_list and created:
                        tshirts = tshirts_list[key]
                        for tshirt in tshirts[0].split(";"):
                            TShirt.objects.create(event_participant=prt_obj, size=tshirt, extra=tshirts[1])
                            count_tshirts += 1
                    prt_obj.save()
                    if created:
                        count_participants += 1
                    else:
                        updated_participants += 1
                self.stdout.write(self.style.SUCCESS(f'Successfully imported users {count_participants} tshirts {count_tshirts}, participants updated {updated_participants}'))