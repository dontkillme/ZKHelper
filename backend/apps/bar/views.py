from django.http.response import JsonResponse
from apps.event.models import EventParticipant


CHAR_MAP = {
    "a": "[aą]",
    "c": "[cć]",
    "ę": "[eę]",
    "l": "[lł]",
    "n": "[nń]",
    "o": "[oó]",
    "s": "[sś]",
    "z": "[zżź]"
}


def find_participant_by_nick(request):
    search = request.GET.get("search")
    search = _build_regex(search)
    participants = EventParticipant.objects.filter(nick__iregex=search).values("nick", "baraccount", "id")
    return JsonResponse(list(participants), safe=False)


def _build_regex(value):
    regex = ""
    for char in value:
        if char in CHAR_MAP:
            regex += CHAR_MAP[char]
        else:
            regex += char
    return regex
