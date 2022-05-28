from generic.endpoints import register_endpoints
from rest_framework.routers import SimpleRouter

from apps.bar.serializers import BarReceiptsSerializer, BarItemSerializer, BarItemCategorySerializer, BarAccountSerializer
from apps.bar.models import BarAccount, BarReceipt, BarItem, BarItemCategory

router = SimpleRouter()
router.register(r'item', register_endpoints(BarItem, BarItemSerializer))
router.register(r'item_category', register_endpoints(BarItemCategory, BarItemCategorySerializer))
router.register(r'receipt', register_endpoints(BarReceipt, BarReceiptsSerializer))
router.register(r'bar_account', register_endpoints(BarAccount, BarAccountSerializer))


urlpatterns = router.urls
