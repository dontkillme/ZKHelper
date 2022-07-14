from generic.endpoints import register_endpoints
from rest_framework.routers import SimpleRouter
from rest_framework import viewsets
from django.urls import path

from apps.bar.serializers import BarReceiptsSerializer, BarItemSerializer, BarItemCategorySerializer, \
    BarAccountSerializer, BarAccountBasicInfoSerializer, BarAccountStackSerializer
from apps.bar.models import BarAccount, BarReceipt, BarItem, BarItemCategory
from apps.bar.views import find_participant_by_nick, BarAccountView, BarFullAccountView

router = SimpleRouter()
router.register(
    r'item',
    register_endpoints(
        BarItem,
        BarItemSerializer,
        mth_perms={
            "GET": ["bar.view_baritem"],
            "POST": ["bar.add_baritem",],
            "PUT": ["bar.change_baritem",],
            "PATCH": ["bar.change_baritem",],
            "DELETE": ["bar.delete_baritem",]
        }
    )
)
router.register(
    r'item_category',
    register_endpoints(
        BarItemCategory,
        BarItemCategorySerializer,
        mth_perms={
            "GET": ["bar.view_baritemcategory"],
            "POST": ["bar.add_baritemcategory",],
            "PUT": ["bar.change_baritemcategory",],
            "PATCH": ["bar.change_baritemcategory",],
            "DELETE": ["bar.delete_baritemcategory",]
        }
    )
)
router.register(
    r'receipt',
    register_endpoints(
        BarReceipt,
        BarReceiptsSerializer,
        mth_perms={
            "GET": ["bar.view_barreceipt"],
            "POST": ["bar.add_barreceipt", ],
            "PUT": ["bar.change_barreceipt", ],
            "PATCH": ["bar.change_barreceipt", ],
            "DELETE": ["bar.delete_barreceipt", ]
        },
        query=BarReceipt.objects.all().order_by("-created_at")
    )
)
router.register(
    r'bar_account',
    register_endpoints(
        BarAccount,
        BarAccountSerializer,
        mth_perms={
            "GET": ["bar.view_baraccount"],
            "POST": ["bar.add_baraccount", ],
            "PUT": ["bar.change_baraccount", ],
            "PATCH": ["bar.change_baraccount", ],
            "DELETE": ["bar.delete_baraccount", ]
        },
        view_cls=BarFullAccountView
    )
)
router.register(
    r'account_basics',
    register_endpoints(
        BarAccount,
        BarAccountBasicInfoSerializer,
        mth_perms={
            "GET": ["bar.view_baraccount"]
        },
        view_cls=BarAccountView
    )
)
router.register(
    r'account_stack',
    register_endpoints(
        BarAccount,
        BarAccountStackSerializer,
        mth_perms={
            "GET": ["bar.view_baraccount"]
        },
        view_cls=BarAccountView
    )
)


urlpatterns = [
  path('search/', find_participant_by_nick),
] + router.urls
