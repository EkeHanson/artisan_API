from rest_framework import serializers
from .models import Message
from .models import CustomUser  # Import CustomUser model

# class MessageSerializer(serializers.ModelSerializer):
#     sender = serializers.UUIDField(read_only=True)  # Display UUID of sender
#     receiver = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Use PrimaryKeyRelatedField

#     class Meta:
#         model = Message
#         fields = ['id', 'sender', 'receiver', 'content', 'created_at']

#     def create(self, validated_data):
#         user = self.context['request'].user  # Get the currently authenticated user
#         validated_data['sender'] = user  # Set the sender to the authenticated user
#         return super().create(validated_data)

from rest_framework import serializers
from .models import Message
from .models import CustomUser  # Import CustomUser model

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.UUIDField(read_only=True)  # Display UUID of sender
    receiver = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())  # Use PrimaryKeyRelatedField
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False)  # Allow reply to be optional

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'created_at', 'reply_to']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the currently authenticated user
        validated_data['sender'] = user  # Set the sender to the authenticated user
        return super().create(validated_data)
