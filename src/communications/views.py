from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import MessageModelSerializer
from .filters import MessageFilterSet

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
