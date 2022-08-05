from django.core.management.base import BaseCommand, CommandError
from apps.event.models import Quest


class Command(BaseCommand):
    help = 'Loads users into db'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(options["file"][0], "r", encoding="utf8") as user_file:
            lines = user_file.readlines()
            count_quests = 0
            for line in lines:
                tmp = line.split(',')
                quest, created = Quest.objects.get_or_create(name=tmp[0], description=tmp[1], reward=int(tmp[2]))
                if created:
                    count_quests += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported quests {count_quests}'))