import json

from asgiref.sync import sync_to_async, async_to_sync

from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def extract_token(self, scope):
        if not scope.get("query_string"):
            return ""
        query_string = str(
            scope.get("query_string", b""), encoding="ascii", errors="ignore"
        )
        splited_query = query_string.split("=")
        token = splited_query[1]
        return token

    def verify_token(self, token):
        from rest_framework_simplejwt.serializers import TokenVerifySerializer

        serializer = TokenVerifySerializer(data={"token": token})
        if serializer.is_valid():
            return True
        return False

    def get_user_id_from_token(self, token):
        from rest_framework_simplejwt.tokens import AccessToken

        if not token:
            return False
        verified = self.verify_token(token)
        if not verified:
            return None
        access_data = AccessToken(token)
        return access_data.get("user_id", None)

    def connect(self):
        # check token
        token = self.extract_token(self.scope)
        user_id = self.get_user_id_from_token(token)
        if not user_id:
            self.close()

        # create room name
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def send_notification(self, event):
        # Send message to WebSocket chanel groups
        self.send(
            text_data=json.dumps(
                {"type": "message", "data": event["data"]}, ensure_ascii=False
            )
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        # Send message to room group
        chat_type = {"type": "message"}
        return_dict = {**chat_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # # Receive message from room group
    # def chat_message(self, event):
    #     text_data_json = event.copy()
    #     text_data_json.pop("type")
    #     message, attachment = (
    #         text_data_json["message"],
    #         text_data_json.get("attachment"),
    #     )

    #     message_object = message.objects.get(id=int(self.room_name))
    #     sender = self.scope["user"]

    #     # Attachment
    #     if attachment:
    #         file_str, file_ext = attachment["data"], attachment["format"]

    #         file_data = ContentFile(
    #             base64.b64decode(file_str),
    #             name=f"{secrets.token_hex(8)}.{file_ext}",
    #         )
    #         _message = Message.objects.create(
    #             sender=sender,
    #             attachment=file_data,
    #             text=message,
    #             conversation_id=conversation,
    #         )
    #     else:
    #         _message = Message.objects.create(
    #             sender=sender,
    #             text=message,
    #             conversation_id=conversation,
    #         )
    #     serializer = MessageSerializer(instance=_message)
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps(serializer.data))
