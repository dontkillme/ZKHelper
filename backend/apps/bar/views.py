from django.http.response import JsonResponse
from apps.event.models import EventParticipant
from rest_framework import viewsets, response
from django.http import Http404
from rest_framework.authtoken.models import Token

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


def _set_user_by_token(request):
    #this is a lazy hack, there is a similar thing but i cant remember where, ill rewrite this to middleware
    token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[-1]
    if not token:
        return JsonResponse({"error": "unauthorized user"}, status=401)
    try:
        token = Token.objects.get(key=token)
    except Token.DoesNotExist:
        return JsonResponse({"error": "unauthorized user"}, status=401)
    request.user = token.user


def find_participant_by_nick(request):
    error = _set_user_by_token(request)
    if error:
        return error
    search = request.GET.get("search")
    if not request.user.has_perms(['bar.view_baraccount']):
        return JsonResponse({"error": "Missing permissions for this action"}, status=403)
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
