from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EmergencyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("hospitals", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("hospitals", self.channel_name)

    async def send_emergency(self, event):
        await self.send(text_data=json.dumps(event["data"]))