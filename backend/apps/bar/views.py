from django.http.response import JsonResponse
from apps.event.models import EventParticipant
from rest_framework import viewsets, response
from django.http import Http404
from generic.views import set_user_by_token
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from apps.bar.models import BarItem, BarReceiptItem, BarAccount

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
    error = set_user_by_token(request)
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


@require_http_methods(["GET",])
@csrf_exempt
def show_final_results(request):
    data = {"items": BarItem.objects.all(),
            "accounts": [],
            "total": 0}
    bar_accounts = BarAccount.objects.all()
    items_ids = [i.id for i in data["items"]]
    items_ids.sort()
    for acc in bar_accounts:
        tmp = {
                 "id": acc.participant.id,
                 "name": acc.participant.name,
                 "surname": acc.participant.surname,
                 "nick": acc.participant.nick,
                 "items": {k: 0 for k in items_ids},
                 "inbound": float(acc.credits) if acc.credits != 1 else 0,
                 "outbound": 0,
                 "recalc": 0,
                 "staff": acc.participant.is_staff
               }
        for receipt in acc.receipts.all():
            for item in receipt.bar_items.all():
                tmp["items"][item.item.id] += item.quantity
                if acc.participant.is_staff:
                    tmp["outbound"] += item.item.staff_price * item.quantity
                else:
                    tmp["outbound"] += item.item.price * item.quantity
        tmp["items"] = sorted(tmp["items"].items())
        tmp["recalc"] = tmp["inbound"] - float(tmp["outbound"])
        if tmp["recalc"] != 0:
            data["accounts"].append(tmp)
            data["total"] += tmp["recalc"]
    return render(request, "recalc.html", data)

