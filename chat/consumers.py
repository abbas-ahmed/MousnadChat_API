import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # انضمام إلى مجموعة الغرفة
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # إرسال رسائل غير مقروءة عند الاتصال
        await self.send_unread_messages()

    async def disconnect(self, close_code):
        # مغادرة المجموعة
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')

        if message_type == 'message':
            message = text_data_json['message']
            voice = text_data_json['voice']
            sender_id = text_data_json['sender_id']
            receiver_id = text_data_json['receiver_id']

            # حفظ الرسالة في قاعدة البيانات
            saved_message = await self.save_message(sender_id, receiver_id, message)

            # إرسال الرسالة للمجموعة
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'voice':voice ,
                    'sender_id': sender_id,
                    'receiver_id': receiver_id,
                    'timestamp': saved_message['timestamp'],
                    'message_id': saved_message['id']
                }
            )

            # تحديث حالة القراءة
            await self.mark_messages_as_read(sender_id, receiver_id)

        elif message_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user_id': text_data_json['user_id'],
                    'is_typing': text_data_json['is_typing']
                }
            )

        elif message_type == 'read_receipt':
            await self.mark_messages_as_read(
                text_data_json['sender_id'],
                text_data_json['receiver_id']
            )

    async def chat_message(self, event):
        # إرسال الرسالة إلى WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'voice':event['voice'] ,
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id']
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'is_typing': event['is_typing']
        }))

    async def send_unread_messages(self):
        user = self.scope['user']
        if user.is_authenticated:
            unread_messages = await self.get_unread_messages(user.id)
            if unread_messages:
                await self.send(text_data=json.dumps({
                    'type': 'unread_messages',
                    'messages': unread_messages
                }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            is_read=False
        )
        return {
            'id': message.id,
            'timestamp': message.timestamp.isoformat(),
            'content': message.content
        }

    @database_sync_to_async
    def mark_messages_as_read(self, sender_id, receiver_id):
        Message.objects.filter(
            sender_id=sender_id,
            receiver_id=receiver_id,
            is_read=False
        ).update(is_read=True)

    @database_sync_to_async
    def get_unread_messages(self, user_id):
        messages = Message.objects.filter(
            receiver_id=user_id,
            is_read=False
        ).select_related('sender').order_by('timestamp')

        return [{
            'id': msg.id,
            'content': msg.content,
            'sender_id': msg.sender.id,
            'sender_name': msg.sender.username,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]