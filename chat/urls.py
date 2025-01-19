from django.urls import path
from .views import ChatListCreateView, MessageListView, SendMessageView, MarkMessagesAsReadView

urlpatterns = [
    path('chats/', ChatListCreateView.as_view(), name="chat-list-create"),
    path('chats/<int:chat_id>/messages/', MessageListView.as_view(), name="message-list"),
    path('messages/send/', SendMessageView.as_view(), name="send-message"),
    path('chats/<int:chat_id>/mark-read/', MarkMessagesAsReadView.as_view(), name='mark-messages-as-read'),

]
