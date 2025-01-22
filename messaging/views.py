from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from users.models import CustomUser

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(receiver=user) | Q(sender=user))

    @action(detail=False, methods=['get'])
    def conversation(self, request):
        sender = request.query_params.get('sender', None)
        receiver = request.query_params.get('receiver', None)
        
        # Validate input
        if not sender or not receiver:
            return Response({"error": "Both sender and receiver parameters are required."}, status=400)
        
        try:
            sender_user = CustomUser.objects.get(unique_id=sender)
            receiver_user = CustomUser.objects.get(unique_id=receiver)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
        
        messages = Message.objects.filter(
            (Q(sender=sender_user) & Q(receiver=receiver_user)) | 
            (Q(sender=receiver_user) & Q(receiver=sender_user))
        ).order_by('created_at')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def send_message(self, request):
        data = request.data

        data['sender'] = request.user.unique_id

        serializer = MessageSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            message = serializer.save()
            return Response(serializer.data, status=201)
        
        print("serializer.errors")
        print(serializer.errors)
        print("serializer.errors")
        return Response(serializer.errors, status=400)


    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        parent_message = self.get_object()

        data = request.data
        data['sender'] = request.user.unique_id
        data['receiver'] = parent_message.sender.id
        data['reply_to'] = parent_message.id 

        serializer = MessageSerializer(data=data, context={'request': request}) 
        
        if serializer.is_valid():
            message = serializer.save()  
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
