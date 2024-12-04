# # chat/consumers.py
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#         self.chat_group_name = f'chat_{self.chat_id}'

#         await self.channel_layer.group_add(
#             self.chat_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.chat_group_name,
#             self.channel_name
#         )

# async def receive(self, text_data):
#     data = json.loads(text_data)
#     message = data['message']
#     sender = self.scope['user']

#     # Save message in the database
#     chat_id = self.chat_id
#     new_message = await database_sync_to_async(Message.objects.create)(
#         chat_id=chat_id, sender=sender, content=message
#     )

#     # Broadcast the new message
#     await self.channel_layer.group_send(
#         self.chat_group_name,
#         {
#             'type': 'chat_message',
#             'message': new_message.content,
#             'sender': sender.username,
#         }
#     )

#     # Notify other participants about the new message
#     participants = await database_sync_to_async(Chat.objects.get(id=chat_id).participants.exclude(id=sender.id))
#     for participant in participants:
#         notification_group = f'user_{participant.id}'
#         await self.channel_layer.group_send(
#             notification_group,
#             {
#                 'type': 'new_message_notification',
#                 'chat_id': chat_id,
#                 'message': message,
#                 'sender': sender.username,
#             }
#         )


#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender'],
#             'is_read': event.get('is_read', False),
#         }))


