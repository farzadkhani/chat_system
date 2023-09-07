from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import CreateMessageModelSerializer, GetMessageModelSerializer
from .filters import MessageFilterSet
from communications.utils.notif_message import trigger_message_noification

# Create your views here.
User = get_user_model()


class MessageModelViewSet(ModelViewSet):
    """
    view for Message model base on ModelViewSet class and
    MessageModelSerializer and MessageFilterSet classes
    """

    # http mehtod delete is deactivated
    http_method_names = [
        "get",
        "post",
        "patch",
        # "delete",
    ]

    # queryset is order by id desc
    queryset = Message.objects.all().order_by("-id")
    # serializer_class = MessageModelSerializer
    filterset_class = MessageFilterSet
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        define witch serializer class use for each http method
        """
        if self.action == "create":
            return CreateMessageModelSerializer
        return GetMessageModelSerializer

    def create(self, request, *args, **kwargs):
        # TODO: use transaction.atomic() for revert all changes if any error in notif
        try:
            trigger_message_noification(request.data)
        except Exception as e:
            raise e

        return super().create(request, *args, **kwargs)
