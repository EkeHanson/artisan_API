from django.db import models

from users.models import CustomUser

class Chat(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, related_name="sent_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()
