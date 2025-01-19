# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Message
# from .serializers import MessageSerializer
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Message


# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Message.objects.filter(receiver=user)

#     @action(detail=False, methods=['post'])
#     def send_message(self, request):
#         data = request.data
#         data['sender'] = request.user.unique_id  # Set sender to the current user
        
#         # Pass the 'request' context explicitly when initializing the serializer
#         serializer = MessageSerializer(data=data, context={'request': request})
        
#         if serializer.is_valid():
#             message = serializer.save()
#             # Optionally, send a notification here
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

#     @action(detail=True, methods=['post'])
#     def reply(self, request, pk=None):
#         parent_message = self.get_object()  # Get the parent message (the message being replied to)
        
#         # Prepare the data for the new reply message
#         data = request.data
#         data['sender'] = request.user.unique_id  # The sender is the currently authenticated user
#         data['receiver'] = parent_message.sender.id  # The receiver is the sender of the parent message
#         data['reply_to'] = parent_message.id  # Set the 'reply_to' to the parent message ID

#         # Pass the context and validate the new message
#         serializer = MessageSerializer(data=data, context={'request': request})  # Pass request context here
        
#         if serializer.is_valid():
#             message = serializer.save()  # Save the new reply message
#             # Optionally, send a notification for the reply
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)




# @receiver(post_save, sender=Message)
# def notify_receiver(sender, instance, created, **kwargs):
#     if created:
#         print(f"Notification: New message from {instance.sender} to {instance.receiver}")
#         # Here you can integrate with an email or push notification system.


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
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
        
        # Get all messages between the sender and receiver, including replies
        messages = Message.objects.filter(
            (Q(sender=sender_user) & Q(receiver=receiver_user)) | 
            (Q(sender=receiver_user) & Q(receiver=sender_user))
        ).order_by('created_at')  # Ensure messages are ordered by creation time

        # Serialize the messages
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        data = request.data
        data['sender'] = request.user.unique_id  # Set sender to the current user
        
        # Pass the 'request' context explicitly when initializing the serializer
        serializer = MessageSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            message = serializer.save()
            # Optionally, send a notification here
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        parent_message = self.get_object()  # Get the parent message (the message being replied to)
        
        # Prepare the data for the new reply message
        data = request.data
        data['sender'] = request.user.unique_id  # The sender is the currently authenticated user
        data['receiver'] = parent_message.sender.id  # The receiver is the sender of the parent message
        data['reply_to'] = parent_message.id  # Set the 'reply_to' to the parent message ID

        # Pass the context and validate the new message
        serializer = MessageSerializer(data=data, context={'request': request})  # Pass request context here
        
        if serializer.is_valid():
            message = serializer.save()  # Save the new reply message
            # Optionally, send a notification for the reply
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
