from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from django.db.models import Q
from uuid import UUID
from .models import Message
from .serializers import MessageSerializer, MessageWithSenderSerializer, UserProfileSerializer
from users.models import CustomUser


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]



    @action(detail=False, methods=['get'])
    def senders_to_user(self, request):
        """Fetch paginated list of users who have sent messages to a particular user along with message counts."""
        receiver_id = request.query_params.get('receiver_id')

        if not receiver_id:
            return Response({"error": "Receiver ID is required."}, status=400)

        try:
            receiver_uuid = UUID(receiver_id)
        except ValueError:
            return Response({"error": "Invalid receiver UUID format."}, status=400)

        # Get distinct senders who have messaged the receiver and count their messages
        senders = CustomUser.objects.filter(
            sent_chat_messages__receiver__unique_id=receiver_uuid
        ).annotate(
            message_count=Count('sent_chat_messages', filter=Q(sent_chat_messages__receiver__unique_id=receiver_uuid))
        ).distinct().order_by('id')  # Ensure ordering for pagination

        # Apply pagination
        paginator = PageNumberPagination()
        paginated_senders = paginator.paginate_queryset(senders, request)

        # Serialize paginated results and include message count
        serialized_data = UserProfileSerializer(paginated_senders, many=True).data
        for sender in serialized_data:
            sender_instance = next((s for s in paginated_senders if str(s.unique_id) == sender['unique_id']), None)
            sender['message_count'] = sender_instance.message_count if sender_instance else 0

        return paginator.get_paginated_response(serialized_data)
    
    @action(detail=False, methods=['get'])
    def conversation(self, request):
        sender_id = request.query_params.get('sender')
        receiver_id = request.query_params.get('receiver')

        if not sender_id or not receiver_id:
            return Response({"error": "Both 'sender' and 'receiver' are required."}, status=400)

        # Assuming 'Message' has sender and receiver fields
        conversation = Message.objects.filter(
            Q(sender__unique_id=sender_id, receiver__unique_id=receiver_id) |
            Q(sender__unique_id=receiver_id, receiver__unique_id=sender_id)
        ).order_by('created_at')  # Use 'created_at' instead of 'timestamp'

        serializer = MessageSerializer(conversation, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def send_message(self, request):

        # print("request.data")
        # print(request.data)
        # print("request.data")

        receiver_id = request.data.get('receiver', '').strip()
        sender_id = request.data.get('sender', '').strip()
        content = request.data.get('content').strip()

        if not sender_id or not receiver_id or not content:
            return Response(
                {"error": "'sender', 'receiver', and 'content' fields are required."},
                status=400
            )

        # Validate sender
        try:
            sender_uuid = UUID(sender_id)
            sender_user = CustomUser.objects.get(unique_id=sender_uuid)
        except ValueError:
            return Response({"error": "Invalid sender UUID format."}, status=400)
        except CustomUser.DoesNotExist:
            return Response({"error": f"Sender with ID {sender_uuid} not found."}, status=404)

        # Validate receiver
        try:
            receiver_uuid = UUID(receiver_id)
            receiver_user = CustomUser.objects.get(unique_id=receiver_uuid)
        except ValueError:
            return Response({"error": "Invalid receiver UUID format."}, status=400)
        except CustomUser.DoesNotExist:
            return Response({"error": f"Receiver with ID {receiver_uuid} not found."}, status=404)

        # Prepare data for serialization
        data = {
            'sender': sender_user.unique_id,
            'receiver': receiver_user.unique_id,
            'content': content,
        }

        # print("data")
        # print(data)
        # print("data")

        serializer = MessageSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            message = serializer.save()
            return Response(
                {"message": "Message sent successfully.", "message_data": serializer.data},
                status=201
            )

        # print("serializer.errors")
        # print(serializer.errors)
        # print("serializer.errors")

        return Response(
            {"error": f"Message failed due to validation errors: {serializer.errors}"},
            status=400
        )

    
    @action(detail=False, methods=['post'])
    def typing_indicator(self, request):
        # print("Request Data:", request.data)  # Log the request data
        
        receiver_id = request.data.get("receiver_id").strip()
        is_typing = True if request.data.get("is_typing") == "true" else False

        if not receiver_id or is_typing is None:
            return Response({"error": "'receiver_id' and 'is_typing' are required."}, status=400)

        # Validate receiver UUID
        try:
            receiver_uuid = UUID(receiver_id)
        except ValueError:
            return Response({"error": "Invalid UUID format for receiver."}, status=400)

        # Optionally, validate that receiver exists in the database
        try:
            receiver_user = CustomUser.objects.get(unique_id=receiver_uuid)
        except CustomUser.DoesNotExist:
            return Response({"error": "Receiver not found."}, status=404)

        # Handle the typing indicator logic (e.g., store in database, broadcast to other users)
        # Placeholder: You can implement your typing indicator state change logic here.

        return Response({"message": "Typing indicator received."}, status=200)


    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        message_ids = request.data.get("message_ids", [])
        # receiver_id = request.data.get("receiver_id")

        # if not message_ids or not receiver_id:
        #     return Response({"error": "Both 'message_ids' and 'receiver_id' are required."}, status=400)

        # try:
        #     receiver_uuid = UUID(receiver_id)
        # except ValueError:
        #     return Response({"error": "Invalid receiver UUID format."}, status=400)

        messages = Message.objects.filter(
            id__in=message_ids,
            # receiver__unique_id=receiver_uuid,
            # sender=request.user
        )
        updated_count = messages.update(is_read=True)

        return Response({"message": f"{updated_count} messages marked as read."}, status=200)
    

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        try:
            parent_message = self.get_object()
        except Message.DoesNotExist:
            return Response(
                {"error": "Parent message not found. Please verify the message ID."},
                status=404
            )

        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required. Please log in to reply to a message."},
                status=401
            )

        data = request.data
        data['sender'] = request.user.id
        data['receiver'] = parent_message.sender.id
        data['reply_to'] = parent_message.id

        serializer = MessageSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            message = serializer.save()
            return Response(
                {"message": "Reply sent successfully.", "message_data": serializer.data},
                status=201
            )
        
        # Provide detailed error messages if the serializer fails validation
        return Response(
            {"error": f"Failed to send reply: {serializer.errors}"},
            status=400
        )
    
    @action(detail=False, methods=['get'])
    def messages_for_artisan(self, request):
        """Fetch all messages sent to an artisan and group them by sender"""
        artisan_id = request.query_params.get('artisan_id')

        if not artisan_id:
            return Response({"error": "Artisan ID is required."}, status=400)

        try:
            artisan_uuid = UUID(artisan_id)
        except ValueError:
            return Response({"error": "Invalid artisan UUID format."}, status=400)

        # Fetch all messages sent to the artisan
        messages = Message.objects.filter(receiver__unique_id=artisan_uuid).select_related('sender').order_by('-created_at')

        # Group all messages by the sender's email (or another consistent unique identifier)
        grouped_messages = {}
        for message in messages:
            sender_email = message.sender.email  # Use email or another consistent field
            
            # If the sender doesn't exist in the dictionary, add them
            if sender_email not in grouped_messages:
                grouped_messages[sender_email] = {
                    'sender': UserProfileSerializer(message.sender).data,
                    'messages': []  # Initialize an empty list to store messages
                }

            # Append the message to the sender's list of messages
            grouped_messages[sender_email]['messages'].append(MessageWithSenderSerializer(message).data)

        # Return grouped messages
        return Response(grouped_messages, status=200)
