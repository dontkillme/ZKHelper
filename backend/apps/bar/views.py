from django.http.response import JsonResponse
from apps.event.models import EventParticipant
from rest_framework import viewsets, response
from django.http import Http404

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
    if search.isnumeric():
        participants = EventParticipant.objects.filter(id=search).values("nick", "baraccount", "id")
    else:
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


class BarAccountRetrieverMixin:
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404 as exc:
            participant = EventParticipant.objects.filter(id=kwargs['pk']).first()
            if not participant:
                raise exc
            else:
                return response.Response({"error": "missing bar account"}, status=460)
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class BarFullAccountView(BarAccountRetrieverMixin, viewsets.ModelViewSet):
    pass


class BarAccountView(BarAccountRetrieverMixin, viewsets.ReadOnlyModelViewSet):
    pass
