from rest_framework import serializers

from .models import Message


class MessageModelSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model base on ModelSerilizer
    and all fields of model except is_soft_deleted and created_at fields
    """

    class Meta:
        model = Message
        # fields = "__all__"
        exclude = [
            "is_soft_deleted",
            "created_at",
        ]
