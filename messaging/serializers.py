from rest_framework import serializers
from .models import Message
from users.models import CustomUser

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.UUIDField(read_only=True)  # Display UUID of sender
    receiver = serializers.UUIDField()  # Expect UUID for receiver in request data

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'created_at', 'reply_to']

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        # Fetch receiver using the unique_id from data
        try:
            data['receiver'] = CustomUser.objects.get(unique_id=data['receiver'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"receiver": "User with this unique_id does not exist."})

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['sender'] = user  # Set the sender to the authenticated user
        return super().create(validated_data)
