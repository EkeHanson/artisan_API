from django.db import models
from django.conf import settings
from users.models import CustomUser

class Message(models.Model):
    sender = models.ForeignKey(CustomUser,  on_delete=models.CASCADE, related_name='sent_chat_messages', to_field='unique_id' )
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='received_chat_messages', to_field='unique_id')

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='chat_replies')

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} on {self.created_at}"
