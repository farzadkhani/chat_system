import json

from django.contrib.auth import get_user_model

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


User = get_user_model()


def create_message_notification_data(request_data):
    """
    create data for message notification system base on message class instance
    """
    try:
        receiver_user = User.objects.get(id=request_data.get("receiver"))

        username = receiver_user.username
        user_id = receiver_user.id
        message = {
            "text": request_data.get("text"),
            "sender": request_data.get("sender"),
            "receiver": request_data.get("receiver"),
            "quote_to": request_data.get("receiver", None),
            "is_read": request_data.get("is_read", False),
        }
        data = {
            "username": username,
            "user_id": user_id,
            "message": message,
        }

        return data

    except Exception as e:
        raise e


def trigger_message_noification(request_data):
    """
    trigger websocket channel for push notification to user
    """
    data = create_message_notification_data(request_data)
    username = data.get("username", None)
    user_id = data.get("user_id", None)

    if username and user_id:
        channel_layer = get_channel_layer()
        group_name = f"group_{user_id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "data": json.dumps(data, ensure_ascii=False),
            },
        )
    else:
        raise Exception("username or user_id is None")
