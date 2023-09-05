from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .models import Notification
from .serializers import (
    NotificationIsReadSerializer,
    NotificationReadOnlyModelSerializer,
)


# Create your views here.
class NotificationModelViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationReadOnlyModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        # if user.is_superuser:
        #     return queryset
        return queryset.filter(user=user)

    @action(
        detail=False,
        methods=["POST"],
        url_path="read-notifications-in-list-of-ids",
    )
    def read_notifications_in_list_of_ids(self, request, *args, **kwargs):
        serializer = NotificationIsReadSerializer(data={**request.data})
        serializer.is_valid(raise_exception=True)
        readed_notifications = serializer.read_notifications()
        return Response(
            readed_notifications.data,
            status=status.HTTP_202_ACCEPTED,
        )


def notifhome(request):
    return render(request, "show_sended_notife.html")
