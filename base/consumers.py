from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ScreenConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("screen", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("screen", self.channel_name)

    async def send_action(self, event):
        await self.send(text_data=json.dumps({
            "type": event["type"],
            "action": event["action"],
            "data": event.get("data", None),
        }))