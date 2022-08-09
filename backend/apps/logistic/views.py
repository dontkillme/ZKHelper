import json
from django.shortcuts import render
from django.http import JsonResponse
from apps.logistic.models import MagazineItem
from apps.bar.models import BarReceiptItem, BarItem
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from generic.views import set_user_by_token


@require_http_methods(["GET",])
@csrf_exempt
def current_magazine_states(request):
    if not request.user.is_authenticated:
        error = set_user_by_token(request)
        if error:
            return error
    if not request.user.has_perms(['bar.add_baraccount']):
        return JsonResponse({"error": "missing permission"}, status=401, safe=False)

    count = {}
    magazine = MagazineItem.objects.select_related("BarItem").all().values_list("baritem_id", "baritem__name", "quantity")
    for item in magazine:
        if not item[0] in count:
            count[item[0]] = {"name": item[1], "magazine": 0, "sell": 0}
        count[item[0]]["magazine"] += item[2]

    baritems = BarReceiptItem.objects.select_related("BarItem").all().values_list("item__id", "item__name", "quantity")

    for item in baritems:
        if not item[0] in count:
            count[item[0]] = {"name": item[1], "magazine": 0, "sell": 0}
        count[item[0]]["sell"] += item[2]

    return render(request, "logi.html", {"count": count.values()})