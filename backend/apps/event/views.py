import json
from django.http import JsonResponse
from apps.event.models import TShirt, EventParticipant
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from generic.views import set_user_by_token


@require_http_methods(["POST",])
@csrf_exempt
def change_tshirt_status(request, uid=None):
    error = set_user_by_token(request)
    if error:
        return error
    if not request.user.has_perms(['event.change_tshirt']):
        return JsonResponse({"error": "missing permission"}, status=401, safe=False)
    state = request.POST.get("given_out", json.loads(request.body).get("given_out"))
    state = int(state)
    participant_id = request.POST.get("participant_id", json.loads(request.body).get("participant_id"))

    if not participant_id and not uid:
        return JsonResponse({"error": "missing tshirt"}, status=400, safe=False)

    if not uid and participant_id:
        tshirt = TShirt.objects.filter(event_participant_id=participant_id).first()
    else:
        tshirt = TShirt.objects.get(id=uid)
    tshirt.given_out = state
    tshirt.save()
    return JsonResponse({"id": tshirt.id, "state": state}, safe=False)


@require_http_methods(["POST",])
@csrf_exempt
def change_accredited_status(request, uid):
    error = set_user_by_token(request)
    if error:
        return error
    if not request.user.has_perms(['event.change_eventparticipant']):
        return JsonResponse({"error": "missing permission"}, status=401, safe=False)
    state = request.POST.get("accredited", json.loads(request.body).get("accredited"))
    state = int(state)
    EventParticipant.objects.filter(id=uid).update(accredited=state)
    return JsonResponse({"id": uid, "state": state}, safe=False)