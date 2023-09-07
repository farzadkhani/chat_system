from django.urls import path
from rest_framework import routers

from .views import NotificationModelViewSet, notifhome

router = routers.SimpleRouter()

router.register(r"notifications", NotificationModelViewSet, basename="notifications")

urlpatterns = [path("notiftest/", notifhome)] + router.urls
