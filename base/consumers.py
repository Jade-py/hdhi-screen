from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ScreenConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("screen", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("screen", self.channel_name)

    async def send_file(self, event):
        file_url = event['file_url']
        await self.send(text_data=json.dumps({
            'file_url': file_url
        }))
