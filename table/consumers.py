from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TableConsumer(AsyncJsonWebsocketConsumer):
    table = None

    async def connect(self):
        self.table = 'table_{}'.format(self.scope['url_route']['kwargs']['table_id'])
        # Join room group
        await self.channel_layer.group_add(self.table, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.table, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        # Send message to room group
        await self.channel_layer.group_send(self.table, {'type': 'message', 'message': content})

    # Receive message from room group
    async def message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send_json(message)