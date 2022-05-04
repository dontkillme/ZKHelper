from generic.endpoints import register_endpoints
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.routers import SimpleRouter

from apps.event.serializers import QuestSerializer, EventParticipantSerializer, AttractionSerializer, \
    FullEventParticipantSerializer, TShirtSerializer
from apps.event.models import Quest, Attraction, EventParticipant, TShirt

router = SimpleRouter()
router.register(r'tshirt', register_endpoints(TShirt, TShirtSerializer))
router.register(r'quest', register_endpoints(Quest, QuestSerializer))
router.register(r'attraction', register_endpoints(Attraction, AttractionSerializer))
router.register(r'eventparticipant', register_endpoints(EventParticipant, EventParticipantSerializer))
router.register(r'fulleventparticipant', register_endpoints(EventParticipant, FullEventParticipantSerializer,
                                                            view_cls=ReadOnlyModelViewSet))


urlpatterns = router.urls
