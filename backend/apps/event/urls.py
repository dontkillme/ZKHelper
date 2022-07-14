from generic.endpoints import register_endpoints
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.routers import SimpleRouter

from apps.event.serializers import QuestSerializer, EventParticipantSerializer, AttractionSerializer, \
    FullEventParticipantSerializer, TShirtSerializer, QuestParticipantSerializer
from apps.event.models import Quest, Attraction, EventParticipant, TShirt, ParticipantQuests

router = SimpleRouter()
router.register(
    r'tshirt',
    register_endpoints(
        TShirt,
        TShirtSerializer,
        mth_perms={
            "GET": ["event.view_tshirt"],
            "POST": ["event.add_tshirt", ],
            "PUT": ["event.change_tshirt", ],
            "PATCH": ["event.change_tshirt", ],
            "DELETE": ["event.delete_tshirt", ]
        }
    )
)
router.register(
    r'quest',
    register_endpoints(
        Quest,
        QuestSerializer,
        mth_perms={
            "GET": ["event.view_quest"],
            "POST": ["event.add_quest", ],
            "PUT": ["event.change_quest", ],
            "PATCH": ["event.change_quest", ],
            "DELETE": ["event.delete_quest", ]
        }
    )
)
router.register(
    r'attraction',
    register_endpoints(
        Attraction,
        AttractionSerializer,
        mth_perms={
            "GET": ["event.view_attraction"],
            "POST": ["event.add_attraction", ],
            "PUT": ["event.change_attraction", ],
            "PATCH": ["event.change_attraction", ],
            "DELETE": ["event.delete_attraction", ]
        }
    )
)
router.register(
    r'eventparticipant',
    register_endpoints(
        EventParticipant,
        EventParticipantSerializer,
        mth_perms={
            "GET": ["event.view_eventparticipant"],
            "POST": ["event.add_eventparticipant", ],
            "PUT": ["event.change_eventparticipant", ],
            "PATCH": ["event.change_eventparticipant", ],
            "DELETE": ["event.delete_eventparticipant", ]
        }
    )
)
router.register(
    r'fulleventparticipant',
    register_endpoints(
        EventParticipant,
        FullEventParticipantSerializer,
        mth_perms={
            "GET": ["event.view_eventparticipant"],
        },
        view_cls=ReadOnlyModelViewSet)
)
router.register(
    r'participant_quest',
    register_endpoints(
        ParticipantQuests,
        QuestParticipantSerializer,
        mth_perms={
            "GET": ["event.view_participantquests"],
            "POST": ["event.add_participantquests", ],
            "PUT": ["event.change_participantquests", ],
            "PATCH": ["event.change_participantquests", ],
            "DELETE": ["event.delete_participantquests", ]
        }
    )
)

urlpatterns = router.urls
