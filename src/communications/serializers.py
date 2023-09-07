from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Message


User = get_user_model()


class CreateMessageModelSerializer(serializers.ModelSerializer):
    """
    Serializer for create Message model base on ModelSerilizer
    and all fields of model except is_soft_deleted and created_at fields
    """

    class Meta:
        model = Message
        # fields = "__all__"
        exclude = [
            "is_read",
            "is_soft_deleted",
            "created_at",
        ]


class GetMessageModelSerializer(serializers.ModelSerializer):
    """
    Serializer for get Message model base on ModelSerilizer
    and all fields of model except is_soft_deleted and created_at fields
    """

    class Meta:
        model = Message
        # fields = "__all__"
        exclude = [
            "is_soft_deleted",
            "created_at",
        ]
