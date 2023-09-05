from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Message


User = get_user_model()


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


class MessageFetchDataWithUserName(serializers.Serializer):
    """
    Serializer for fetch data with username
    """

    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        """
        validate username
        """
        if not value:
            raise serializers.ValidationError("username is required")

        self.users_queryset = User.objects.none()
        try:
            self.user_object = User.objects.get(username=value)
            return value

        except Exception as e:
            raise serializers.ValidationError(e)

    def get_result(self):
        """
        get result of serializer
        """
        username = "user1"
        user_id = 2
        message = {
            "text": "hello world",
            "sender": "3",
            "receiver": "2",
            "quote_to": None,
            "is_read": False,
        }
        data = {
            "username": username,
            "user_id": user_id,
            "message": message,
        }

        return data
