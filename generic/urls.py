from django.urls import path
from rest_framework import routers
from generic.views import Logout, UserView, PingView


router = routers.SimpleRouter()
router.register("user", UserView)

urlpatterns = [
    path('logout/', Logout.as_view()),
    path('ping/', PingView.as_view())
] + router.urls
