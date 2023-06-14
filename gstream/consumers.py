from channels.generic.websocket import AsyncWebsocketConsumer
import json


class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        owner = data_json['OWNER']
        sender = data_json['SENDER']
        msg_type = data_json['MSG_TYPE']
        operation = data_json['OPERATION']
        url = data_json['DATA']['URL']
        play = data_json['DATA']['PLAY']
        seek = data_json['DATA']['SEEK']

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'group_stream',
                'OWNER': owner,
                'SENDER': sender,
                'MSG_TYPE': msg_type,
                'OPERATION': operation,
                'DATA': {
                    'URL': url,
                    'PLAY': play,
                    'SEEK': seek
                }
            }
        )

    async def group_stream(self, event):

        owner = event['OWNER']
        sender = event['SENDER']
        msg_type = event['MSG_TYPE']
        operation = event['OPERATION']
        url = event['DATA']['URL']
        play = event['DATA']['PLAY']
        seek = event['DATA']['SEEK']

        await self.send(
            text_data=json.dumps({
                'type': 'group_stream',
                'OWNER': owner,
                'SENDER': sender,
                'MSG_TYPE': msg_type,
                'OPERATION': operation,
                'DATA': {
                    'URL': url,
                    'PLAY': play,
                    'SEEK': seek
                }
            })
        )
