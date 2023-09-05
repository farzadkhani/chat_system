from django.urls import path
from rest_framework import routers

from .views import MessageModelViewSet

router = routers.SimpleRouter()

router.register("messages", MessageModelViewSet, basename="messages")

urlpatterns = [] + router.urls
