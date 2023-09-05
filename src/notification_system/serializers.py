from rest_framework import serializers

from .models import Notification
from main_app.serializers import ReadOnlyModelSerializer
from communications.serializers import MessageModelSerializer


class NotificationReadOnlyModelSerializer(ReadOnlyModelSerializer):
    """
    serializer for Notification model base on ModelSerializer and

    """

    # TODO: create read only serializer for User model
    message = MessageModelSerializer(read_only=True)

    class Meta:
        model = Notification
        exclude = [
            "is_soft_deleted",
            "created_at",
        ]
        read_only_fields = ("id", "created_at")


class NotificationIsReadSerializer(serializers.Serializer):
    notification_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Notification.objects.filter(is_read=False),
    )

    def read_notifications(self):
        validated_data = self.validated_data
        notification_objects = validated_data.get("notification_ids")
        for notification in notification_objects:
            notification.is_read = True
            notification.save()
        return NotificationReadOnlyModelSerializer(notification_objects, many=True)
