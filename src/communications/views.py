import json

from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageModelSerializer, MessageFetchDataWithUserName
from .filters import MessageFilterSet

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
    serializer_class = MessageModelSerializer
    filterset_class = MessageFilterSet
    permission_classes = [IsAuthenticated]


class MessageTriggerNotificationAPIView(APIView):
    """
    view for trigger notification when create message base on APIView
    """

    # http method just post is activated
    http_method_names = ["post"]

    serializer = MessageFetchDataWithUserName

    def post(self, request, *args, **kwargs):
        """
        when create message trigger notification for receiver user
        """
        serializer = self.serializer(data={**request.data})
        serializer.is_valid(raise_exception=True)
        result = serializer.get_result()
        self.send_channel_data(result)

        return Response(
            {},
            status=status.HTTP_204_NO_CONTENT,
        )

    def send_channel_data(self, result):
        """
        send data to channel layer
        """

        channel_layer = get_channel_layer()
        group_name = f"group_{result.get('user_id')}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "data": json.dumps(result, ensure_ascii=False),
            },
        )
