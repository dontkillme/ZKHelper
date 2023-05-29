from django.urls import path
from rest_framework import routers
from generic.views import Logout, UserView, PingView, pin_login, MyAuth, login_basic_pin, login_page, get_info_point_view, get_dashboard
from apps.logistic.views import current_magazine_states, current_sum_state

router = routers.SimpleRouter()
router.register("user", UserView)

urlpatterns = [
    path('auth/', MyAuth.as_view()),
    path('logout/', Logout.as_view()),
    path('pin/', pin_login),
    path('ping/', PingView.as_view()),
    path('basic/', login_page),
    path('basic/login/', login_basic_pin),
    path('basic/infopoint/', get_info_point_view),
    path('basic/dashboard/', get_dashboard),
    path('logistic/', current_magazine_states),
    path('sum/', current_sum_state)

] + router.urls
