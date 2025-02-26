from rest_framework import serializers
from .models import Message
from users.models import CustomUser
from uuid import UUID


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.UUIDField()
    receiver = serializers.UUIDField()

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'created_at', 'reply_to']

    def validate_sender(self, value):
        """Ensure sender is a valid UUID and exists in the database."""
        try:
            uuid_obj = UUID(str(value))
        except ValueError:
            raise serializers.ValidationError("Sender must be a valid UUID.")

        if not CustomUser.objects.filter(unique_id=uuid_obj).exists():
            raise serializers.ValidationError("User with this unique_id does not exist.")

        return uuid_obj


    def validate_receiver(self, value):
        """Ensure receiver is a valid UUID and exists in the database."""
        try:
            uuid_obj = UUID(str(value))
        except ValueError:
            raise serializers.ValidationError("Receiver must be a valid UUID.")

        if not CustomUser.objects.filter(unique_id=uuid_obj).exists():
            raise serializers.ValidationError("User with this unique_id does not exist.")

        return uuid_obj


    def create(self, validated_data):
        validated_data['sender'] = CustomUser.objects.get(unique_id=validated_data['sender'])
        validated_data['receiver'] = CustomUser.objects.get(unique_id=validated_data['receiver'])
        return super().create(validated_data)



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['unique_id', 'first_name', 'last_name', 'user_image', 'email', 'phone']  # Include fields you want to display


class MessageWithSenderSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'created_at', 'is_read']