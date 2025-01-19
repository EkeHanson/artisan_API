from rest_framework import generics, status
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated



class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    
    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)
    
    def perform_create(self, serializer):
        participants = self.request.data.get("participants")
        chat = Chat.objects.create()
        chat.participants.set(participants)
        chat.save()
        return chat

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MarkMessagesAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        messages = Message.objects.filter(chat_id=chat_id, is_read=False).exclude(sender=request.user)
        messages.update(is_read=True)
        return Response({"status": "Messages marked as read."})
