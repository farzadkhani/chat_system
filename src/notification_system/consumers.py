import json

from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
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

    async def connect(self):
        # check token
        token = self.extract_token(self.scope)
        user_id = self.get_user_id_from_token(token)
        if not user_id:
            self.close()

        # create room name
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def send_notification(self, event):
        # Send message to WebSocket chanel groups
        self.send(
            text_data=json.dumps(
                {"type": "message", "data": event["data"]}, ensure_ascii=False
            )
        )
